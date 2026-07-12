#!/usr/bin/env python3
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from repository_tooling import (
    ToolingError,
    check_repository,
    discover_tasks,
    ensure_staged_paths_allowed,
    git,
    git_preflight,
    load_repository_model,
    porcelain_status,
    publish_branch,
    refresh_integrity,
    run_tasks,
    suggest_commit,
    validate_inventory,
    validate_model_descriptor,
    verify_integrity,
)


def emit(payload: dict[str, Any], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    for key, value in payload.items():
        if isinstance(value, (dict, list)):
            print(f"{key.upper()}:")
            print(json.dumps(value, indent=2, ensure_ascii=False))
        else:
            print(f"{key.upper()}: {value}")


def validate_command(args: argparse.Namespace) -> dict[str, Any]:
    model = load_repository_model(args.root)
    validate_inventory(model)
    verify_integrity(model)
    validate_model_descriptor(model)
    tasks = run_tasks(model, "validate", selected=args.task)
    return {
        "status": "PASS",
        "command": "validate",
        "tasks": [item["task"] for item in tasks],
        "skills": len(model.skill_order),
        "crossCuttingSkills": len(model.cross_cutting_ids),
        "canonicalSources": len(model.canonical_sources),
    }


def build_command(args: argparse.Namespace) -> dict[str, Any]:
    model = load_repository_model(args.root)
    if args.temporary:
        with tempfile.TemporaryDirectory(prefix="skills-build-") as directory:
            output_base = Path(directory)
            tasks = run_tasks(model, "build", selected=args.task, output_base=output_base)
            outputs = [
                {"task": item["task"], "sha256": item.get("sha256")}
                for item in tasks
            ]
        return {
            "status": "PASS",
            "command": "build",
            "temporary": True,
            "outputs": outputs,
        }
    output_base = (args.output_base or model.root / "dist" / "tooling-builds").resolve(strict=False)
    tasks = run_tasks(model, "build", selected=args.task, output_base=output_base)
    return {
        "status": "PASS",
        "command": "build",
        "temporary": False,
        "outputBase": os.fspath(output_base),
        "outputs": [
            {"task": item["task"], "output": item.get("output"), "sha256": item.get("sha256")}
            for item in tasks
        ],
    }


def check_command(args: argparse.Namespace) -> dict[str, Any]:
    model = load_repository_model(args.root)
    result = check_repository(model)
    return {"status": "PASS", "command": "check", **result}


def refresh_command(args: argparse.Namespace) -> dict[str, Any]:
    model = load_repository_model(args.root)
    changed, data = refresh_integrity(model, write=not args.dry_run)
    return {
        "status": "PASS",
        "command": "refresh-integrity",
        "changed": changed,
        "written": changed and not args.dry_run,
        "bytes": len(data),
    }


def suggest_command(args: argparse.Namespace) -> dict[str, Any]:
    model = load_repository_model(args.root)
    git_preflight(model)
    suggestion = suggest_commit(
        model,
        staged=args.staged,
        include_untracked=args.untracked,
    )
    if not args.json:
        print("COMMIT_SUGGESTION:")
        print(suggestion["subject"])
        if suggestion.get("body"):
            print()
            print(suggestion["body"])
        print()
    return {"status": "PASS", "command": "suggest-commit", **suggestion}


def _message(args: argparse.Namespace, suggestion: dict[str, Any]) -> tuple[str, str]:
    if args.message:
        subject = args.message.strip().splitlines()[0].strip()
        body = "\n".join(args.message.strip().splitlines()[1:]).strip()
    elif args.auto_message:
        subject = suggestion["subject"]
        body = suggestion.get("body", "")
    else:
        raise ToolingError(
            suggestion_issue(
                "COMMIT_MESSAGE_REQUIRED",
                "commit",
                "message",
                "none",
                "pass --auto-message or --message",
            )
        )
    if not subject:
        raise ToolingError(suggestion_issue("EMPTY_COMMIT_MESSAGE", "commit", "subject", subject, "non-empty subject required"))
    if subject.endswith("."):
        subject = subject[:-1]
    return subject[:72], body


def suggestion_issue(code: str, file: str, entity: str, received: Any, rule: str):
    from repository_tooling import ToolingIssue

    return ToolingIssue(code=code, file=file, entity=entity, received=str(received), rule=rule)


def _publication_kwargs(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "remote": args.remote,
        "branch": args.branch,
        "dry_run": args.dry_run,
        "set_upstream": args.set_upstream,
        "fetch": args.fetch,
        "expected_base": args.expected_base,
        "default_branch": args.default_branch,
    }


def publish_command(args: argparse.Namespace) -> dict[str, Any]:
    model = load_repository_model(args.root)
    return publish_branch(model, **_publication_kwargs(args))


def commit_command(args: argparse.Namespace) -> dict[str, Any]:
    model = load_repository_model(args.root)
    initial = git_preflight(model)
    initial_status = porcelain_status(model)
    if not initial_status:
        raise ToolingError(suggestion_issue("NO_CHANGES", os.fspath(model.root), "git-status", "clean", "commit requires changes"))

    suggestion = suggest_commit(model, staged=False, include_untracked=True)
    if args.dry_run:
        subject, body = _message(args, suggestion)
        _, integrity_data = refresh_integrity(model, write=False)
        check_result = check_repository(model, integrity_override=integrity_data)
        publication: dict[str, Any] | None = None
        if args.push:
            publication_args = _publication_kwargs(args)
            publication_args["prospective_commit"] = True
            publication = publish_branch(model, **publication_args)
        final = git_preflight(model)
        final_status = porcelain_status(model)
        if final != initial or final_status != initial_status:
            raise ToolingError(
                suggestion_issue(
                    "DRY_RUN_MUTATION",
                    os.fspath(model.root),
                    "git-state",
                    {"before": initial, "after": final},
                    "dry-run must not change HEAD, branch, index, or working tree",
                )
            )
        return {
            "status": "PASS",
            "command": "commit",
            "dryRun": True,
            "localCommit": {
                "status": "PASS",
                "created": False,
                "branch": initial["branch"],
                "head": initial["head"],
                "subject": subject,
                "body": body,
                "checks": check_result,
                "files": initial_status,
            },
            "remotePublication": publication if args.push else {"status": "SKIPPED", "reason": "--push not supplied"},
        }

    changed, _ = refresh_integrity(model, write=True)
    check_result = check_repository(load_repository_model(model.root))
    git(model, "add", "-A")
    ensure_staged_paths_allowed(model)
    staged = git(model, "diff", "--cached", "--name-only").stdout.splitlines()
    if not staged:
        raise ToolingError(suggestion_issue("NO_STAGED_CHANGES", os.fspath(model.root), "index", "empty", "commit requires staged changes"))
    staged_suggestion = suggest_commit(model, staged=True, include_untracked=False)
    subject, body = _message(args, staged_suggestion)
    command = ["commit", "-m", subject]
    if body:
        command += ["-m", body]
    git(model, *command)
    commit_sha = git(model, "rev-parse", "HEAD").stdout.strip()
    branch = git(model, "symbolic-ref", "--short", "HEAD").stdout.strip()
    final_status = porcelain_status(model)
    local_result = {
        "status": "PASS",
        "created": True,
        "integrityChanged": changed,
        "branch": branch,
        "sha": commit_sha,
        "subject": subject,
        "body": body,
        "files": staged,
        "checks": check_result,
        "workingTreeClean": not final_status,
    }
    if not args.push:
        return {
            "status": "PASS",
            "command": "commit",
            "dryRun": False,
            "localCommit": local_result,
            "remotePublication": {"status": "SKIPPED", "reason": "--push not supplied"},
        }
    try:
        publication_args = _publication_kwargs(args)
        publication_args["dry_run"] = False
        publication = publish_branch(load_repository_model(model.root), **publication_args)
    except ToolingError as exc:
        return {
            "status": "FAIL",
            "command": "commit",
            "dryRun": False,
            "localCommit": local_result,
            "remotePublication": {"status": "FAIL", "error": exc.issue.__dict__},
        }
    return {
        "status": "PASS",
        "command": "commit",
        "dryRun": False,
        "localCommit": local_result,
        "remotePublication": publication,
    }


def tasks_command(args: argparse.Namespace) -> dict[str, Any]:
    model = load_repository_model(args.root)
    return {
        "status": "PASS",
        "command": "tasks",
        "build": [path.stem for path in discover_tasks(model, "build")],
        "validate": [path.stem for path in discover_tasks(model, "validate")],
    }


def _add_publication_options(command: argparse.ArgumentParser, *, include_dry_run: bool) -> None:
    if include_dry_run:
        command.add_argument("--dry-run", action="store_true", help="Verify publication without fetch, push, ref, or upstream mutation.")
    command.add_argument("--remote", default="origin", help="Configured remote name; defaults to origin.")
    command.add_argument("--branch", help="Remote branch name; defaults to the current local branch.")
    command.add_argument("--expected-base", help="Require the remote default branch to remain at this commit SHA.")
    command.add_argument("--default-branch", help="Explicit fallback only when the remote HEAD symref cannot be resolved.")
    command.add_argument("--set-upstream", action=argparse.BooleanOptionalAction, default=True, help="Set tracking configuration after successful publication.")
    command.add_argument("--fetch", action=argparse.BooleanOptionalAction, default=True, help="Fetch and prune the selected remote before a real push.")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Manifest-driven repository tooling.")
    root.add_argument("--root", type=Path, help="Repository root override.")
    root.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    root.add_argument("--debug", action="store_true", help="Show unexpected tracebacks.")
    subparsers = root.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Run structural and discovered validators without modifying files.")
    validate.add_argument("--task", action="append", help="Run only a named discovered validator.")
    validate.set_defaults(handler=validate_command)

    build = subparsers.add_parser("build", help="Run discovered builds.")
    build.add_argument("--task", action="append", help="Run only a named discovered build.")
    build.add_argument("--output-base", type=Path, help="Base directory for persistent build outputs.")
    build.add_argument("--temporary", action="store_true", help="Build in a temporary directory and retain only hashes.")
    build.set_defaults(handler=build_command)

    check = subparsers.add_parser("check", help="Validate, build twice in temporary directories, and verify determinism.")
    check.set_defaults(handler=check_command)

    refresh = subparsers.add_parser("refresh-integrity", help="Regenerate derived integrity metadata atomically.")
    refresh.add_argument("--dry-run", action="store_true", help="Compute changes without writing.")
    refresh.set_defaults(handler=refresh_command)

    suggest = subparsers.add_parser("suggest-commit", help="Generate a commit message from real Git changes.")
    suggest.add_argument("--staged", action="store_true", help="Use only staged changes.")
    suggest.add_argument("--untracked", action=argparse.BooleanOptionalAction, default=True)
    suggest.set_defaults(handler=suggest_command)

    commit = subparsers.add_parser("commit", help="Refresh, validate, build, stage, and create one local commit.")
    commit.add_argument("--dry-run", action="store_true", help="Run all checks without modifying files, index, HEAD, refs, or upstream configuration.")
    group = commit.add_mutually_exclusive_group(required=True)
    group.add_argument("--message", help="Explicit commit message; first line is the subject.")
    group.add_argument("--auto-message", action="store_true", help="Use the generated commit suggestion.")
    commit.add_argument("--push", action="store_true", help="Publish only after the local commit succeeds.")
    _add_publication_options(commit, include_dry_run=False)
    commit.set_defaults(handler=commit_command)

    publish = subparsers.add_parser("publish", help="Publish exactly one validated non-default branch with native Git.")
    _add_publication_options(publish, include_dry_run=True)
    publish.set_defaults(handler=publish_command)

    tasks = subparsers.add_parser("tasks", help="List conventionally discovered tasks.")
    tasks.set_defaults(handler=tasks_command)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        payload = args.handler(args)
    except ToolingError as exc:
        payload = {"status": "FAIL", "command": args.command, "error": exc.issue.__dict__}
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(f"{args.command.upper()}: FAIL")
            print(exc.issue.render())
        return 1
    except Exception as exc:  # unexpected failures only
        if args.debug:
            raise
        payload = {
            "status": "FAIL",
            "command": args.command,
            "error": {
                "code": "UNEXPECTED_ERROR",
                "file": "runtime",
                "entity": type(exc).__name__,
                "received": str(exc),
                "rule": "rerun with --debug for traceback",
            },
        }
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(f"{args.command.upper()}: FAIL")
            print(payload["error"])
        return 1
    if args.command != "suggest-commit" or args.json:
        emit(payload, as_json=args.json)
    return 0 if payload.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
