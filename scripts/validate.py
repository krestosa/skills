#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "shared"
INTEGRITY = SHARED / "manifests/integrity.json"
errors: list[str] = []


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid json {path.relative_to(ROOT)}: {exc}")
        return {}


def require(path: Path) -> None:
    if not path.is_file():
        errors.append("missing " + path.relative_to(ROOT).as_posix())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


required = [
    ROOT / "README.md",
    ROOT / "SKILL.md",
    ROOT / "orchestrator/SKILL.md",
    ROOT / "orchestrator/registry.json",
    ROOT / "orchestrator/delegation-envelope.schema.json",
    ROOT / "scripts/build_chatgpt_flat.py",
    ROOT / "scripts/build_compiled.py",
    ROOT / "scripts/validate_gpt56.py",
    ROOT / "scripts/verify_lossless.py",
    SHARED / "manifests/routes.json",
    SHARED / "manifests/source-index.json",
    SHARED / "evals/parallel-execution.json",
    SHARED / "evals/local-git-workspace.json",
    SHARED / "evals/chat-recovery.json",
    SHARED / "references/parallel-execution-policy-verbatim.md",
    ROOT / "skills/chat-recovery/SKILL.md",
]
for path in required:
    require(path)

if sorted(ROOT.rglob("README.md")) != [ROOT / "README.md"]:
    errors.append("expected one root README.md")
for legacy in ["skills/main", "skills/orchestrator", "skills/individual", "skills/skill-orquestador"]:
    if (ROOT / legacy).exists():
        errors.append("legacy layer exists: " + legacy)
if (ROOT / ".github/workflows").exists():
    errors.append("GitHub workflows are prohibited")

main = (ROOT / "SKILL.md").read_text(encoding="utf-8")
orch = (ROOT / "orchestrator/SKILL.md").read_text(encoding="utf-8")
if "orchestrator/SKILL.md" not in main:
    errors.append("main does not load orchestrator")
if re.search(r"skills/[a-z0-9-]+/SKILL\.md", main):
    errors.append("main loads individual skill")
for marker in [
    "Select one primary skill",
    "Do not load all skills preemptively",
    "Attach `chat-recovery`",
    "Attach `local-git-workspace`",
    "Attach `parallel-execution`",
    "Cross-cutting auto-attached skills do not count",
    "## Chat recovery attachment",
    "recursively inventory every file and directory",
    "### Chat recovery",
    "emit exactly one self-contained prompt inside one code block",
    "no text before or after that code block",
]:
    if marker not in orch:
        errors.append("orchestrator missing " + marker)
for marker in [
    "delegated-result continuation mode applies",
    "exactly one self-contained continuation",
    "nothing outside it",
    "Delegated-result continuation mode overrides",
]:
    if marker not in main:
        errors.append("main delegated-return contract missing " + marker)

routes = load(SHARED / "manifests/routes.json").get("routes", {})
registry = load(ROOT / "orchestrator/registry.json")
skills = registry.get("skills", [])
ids = [item.get("id") for item in skills]
if len(ids) != 17 or len(ids) != len(set(ids)):
    errors.append("expected 17 unique skills")

for item in skills:
    skill_id = item.get("id")
    path = ROOT / f"skills/{skill_id}/SKILL.md"
    if item.get("skillFile") != f"skills/{skill_id}/SKILL.md":
        errors.append(f"{skill_id} path mismatch")
    require(path)
    text = path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""
    for heading in [
        "## Role",
        "## Personality",
        "## Collaboration style",
        "## Goal",
        "## Success criteria",
        "## Select when",
        "## Exclude when",
        "## Shared routes",
        "## Output",
        "## Stop rules",
    ]:
        if heading not in text:
            errors.append(f"{skill_id} missing {heading}")
    for route in item.get("requiredRoutes", []) + item.get("optionalRoutes", []):
        if route not in routes:
            errors.append(f"{skill_id} unknown route {route}")
    for dependency in item.get("dependencies", []):
        if dependency not in ids:
            errors.append(f"{skill_id} unknown dependency {dependency}")
    if not item.get("loadPolicy", {}).get("onDemand"):
        errors.append(f"{skill_id} not on-demand")

selection = registry.get("selectionPolicy", {})
expected_cross_cutting = ["parallel-execution", "local-git-workspace", "chat-recovery"]
if selection.get("crossCuttingSkillIds") != expected_cross_cutting:
    errors.append("cross-cutting registry mismatch")
if not selection.get("ordinaryActiveSkillTarget", {}).get("excludesCrossCutting"):
    errors.append("cross-cutting target mismatch")

parallel = next((item for item in skills if item.get("id") == "parallel-execution"), {})
parallel_auto = selection.get("autoAttach", {}).get("parallel-execution", {})
if parallel.get("role") != "cross-cutting" or any(parallel.get("capabilities", {}).values()):
    errors.append("parallel capability boundary")
if parallel.get("requiredRoutes") or parallel.get("optionalRoutes"):
    errors.append("parallel routes must be empty")
if not parallel.get("loadPolicy", {}).get("autoAttachWhenApplicable") or parallel_auto.get("default") != "attach-when-applicable":
    errors.append("parallel auto-attach mismatch")
parallel_ref = SHARED / "references/parallel-execution-policy-verbatim.md"
if digest(parallel_ref) != "804cc93be433bf159a7ac57d0778fbb72806c8306940343657079e8aa5db8126" or len(parallel_ref.read_bytes()) != 12903:
    errors.append("parallel reference mismatch")

local_git = next((item for item in skills if item.get("id") == "local-git-workspace"), {})
local_auto = selection.get("autoAttach", {}).get("local-git-workspace", {})
if local_git.get("role") != "cross-cutting":
    errors.append("local Git role mismatch")
if local_git.get("capabilities") != {"remoteReads": False, "remoteWrites": False, "localWrites": True}:
    errors.append("local Git capability boundary")
if local_git.get("requiredRoutes") or local_git.get("optionalRoutes"):
    errors.append("local Git routes must be empty")
for key in ["autoAttachWhenApplicable", "runBeforeFirstLocalGitCommand", "onePreflightPerWorkspace"]:
    if not local_git.get("loadPolicy", {}).get(key):
        errors.append("local Git load policy " + key)
for key in [
    "requiresRootRuntime",
    "runBeforeFirstLocalGitCommand",
    "onePreflightPerWorkspace",
    "prohibitsSafeDirectoryFallback",
    "authorizedLocalMetadataRepairOnly",
    "doesNotAuthorizeRemoteWrites",
    "doesNotCountTowardOrdinaryActiveSkillTarget",
]:
    if not local_auto.get(key):
        errors.append("local Git auto-attach " + key)
if local_auto.get("default") != "attach-before-local-git":
    errors.append("local Git attach default")
if local_auto.get("ownershipCommand") != 'sudo -n chown -R "$(id -u):$(id -g)" -- "$repo_root"':
    errors.append("ownership command mismatch")
if local_auto.get("rootFallbackWhenSudoUnavailable") != 'chown -R "$(id -u):$(id -g)" -- "$repo_root"':
    errors.append("ownership fallback mismatch")

local_text = (ROOT / "skills/local-git-workspace/SKILL.md").read_text(encoding="utf-8")
for marker in [
    "realpath -e",
    'sudo -n chown -R "$(id -u):$(id -g)" -- "$repo_root"',
    "ROOT_RUNTIME_REQUIRED",
    "LOCAL_GIT_OWNERSHIP_REPAIR_FAILED",
    "git config --global --add safe.directory",
    "exclusive metadata lock",
    "Remote GitHub access remains connector-only",
]:
    if marker not in local_text:
        errors.append("local Git skill missing " + marker)

chat = next((item for item in skills if item.get("id") == "chat-recovery"), {})
chat_auto = selection.get("autoAttach", {}).get("chat-recovery", {})
if chat.get("role") != "cross-cutting":
    errors.append("chat recovery role mismatch")
if any(chat.get("capabilities", {}).values()):
    errors.append("chat recovery must not grant side effects")
if chat.get("dependencies") != ["management-delegation"]:
    errors.append("chat recovery dependency mismatch")
for key in [
    "autoAttachWhenApplicable",
    "requiresFullWorkspaceInventoryBeforeMutation",
    "requiresIdempotentContinuationPrompt",
    "promptOnlyResponse",
]:
    if not chat.get("loadPolicy", {}).get(key):
        errors.append("chat recovery load policy " + key)
for key in [
    "requiresFullWorkspaceInventoryBeforeMutation",
    "inventoryIncludesIgnoredGeneratedHiddenTemporaryAndBinary",
    "reuseExistingValidFiles",
    "prohibitsUnnecessaryRegeneration",
    "unknownStateIsNotNotStarted",
    "requiresIdempotentContinuationPrompt",
    "promptOnlyResponse",
    "doesNotAuthorizeSideEffects",
    "doesNotCountTowardOrdinaryActiveSkillTarget",
]:
    if not chat_auto.get(key):
        errors.append("chat recovery auto-attach " + key)
if chat_auto.get("default") != "attach-on-interrupted-delegated-chat":
    errors.append("chat recovery attach default")
if chat_auto.get("inventoryBoundary") != "active-workspace-only":
    errors.append("chat recovery inventory boundary")

chat_text = (ROOT / "skills/chat-recovery/SKILL.md").read_text(encoding="utf-8")
for marker in [
    "recursively inventory every file and directory",
    "tracked, untracked, ignored, generated, temporary, hidden, binary",
    "Existing files are evidence",
    "hash lazily",
    "avoid repeatedly rescanning unchanged paths",
    "requires a complete active-workspace inventory",
    "idempotent",
    "exactly one self-contained recovery or continuation prompt",
]:
    if marker not in chat_text:
        errors.append("chat recovery skill missing " + marker)

management_text = (ROOT / "skills/management-delegation/SKILL.md").read_text(encoding="utf-8")
for marker in [
    "## Returned-result procedure",
    "## Interrupted-chat procedure",
    "Attach `chat-recovery`",
    "scan every file and directory",
    "return exactly one prompt inside one code block and nothing else",
    "stop immediately after the closing fence",
]:
    if marker not in management_text:
        errors.append("delegation recovery contract missing " + marker)

parallel_cases = load(SHARED / "evals/parallel-execution.json").get("cases", [])
local_cases = load(SHARED / "evals/local-git-workspace.json").get("cases", [])
chat_cases = load(SHARED / "evals/chat-recovery.json").get("cases", [])
if len({item.get("id") for item in parallel_cases}) < 10:
    errors.append("parallel eval coverage")
if len({item.get("id") for item in local_cases}) < 10:
    errors.append("local Git eval coverage")
if len({item.get("id") for item in chat_cases}) < 12:
    errors.append("chat recovery eval coverage")


def catalog_payload(path: Path) -> bytes:
    data = path.read_bytes()
    begin = b"<!-- VERBATIM_CATALOG_BEGIN -->\n"
    end = b"<!-- VERBATIM_CATALOG_END -->\n"
    return data[data.index(begin) + len(begin):data.index(end)].rstrip(b"\n")


for rel, count, expected_hash in [
    ("catalogs/github-read-verbatim.md", 56, "610c387f5f7c9047c65fef08734d5199696230866ca79e270700209eaab1324e"),
    ("catalogs/github-write-verbatim.md", 41, "499373638143f48b0549701bf5036725a2c2bc9b332a95d9a053a1e1ce687a3d"),
]:
    path = SHARED / rel
    require(path)
    if path.is_file():
        payload = catalog_payload(path)
        if hashlib.sha256(payload).hexdigest() != expected_hash:
            errors.append(rel + " hash mismatch")
        if len([part for part in payload.decode().split("\n\n") if part.strip()]) != count:
            errors.append(rel + " count mismatch")

for script, label in [
    (ROOT / "scripts/verify_lossless.py", "lossless"),
    (ROOT / "scripts/validate_gpt56.py", "GPT-5.6"),
]:
    result = subprocess.run([sys.executable, str(script)], cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        errors.append(label + " validation failed:\n" + result.stdout + result.stderr)

active = "\n".join([main, orch] + [(ROOT / item["skillFile"]).read_text(encoding="utf-8") for item in skills])
if "Remote GitHub operations use the GitHub connector" not in active:
    errors.append("connector boundary missing")
if re.search(r"(?m)^\s*(git\s+(clone|fetch|pull|push|ls-remote)|gh\s+(api|repo|pr|issue|run|workflow|release|search))\b", active):
    errors.append("remote git/gh command in active hierarchy")

static = {
    "README.md", "SKILL.md", "orchestrator/SKILL.md", "orchestrator/registry.json", "orchestrator/delegation-envelope.schema.json",
    "scripts/build_chatgpt_flat.py", "scripts/build_compiled.py", "scripts/validate.py", "scripts/validate_gpt56.py", "scripts/verify_lossless.py",
    "shared/catalogs/github-read-verbatim.md", "shared/catalogs/github-write-verbatim.md",
    "shared/contracts/authorization-envelope.schema.json", "shared/contracts/connector-contracts.md",
    "shared/core/identity.md", "shared/core/project-authority-and-roles.md", "shared/core/states-and-approval.md",
    "shared/evals/gpt-5.6-sol.json", "shared/evals/parallel-execution.json", "shared/evals/local-git-workspace.json", "shared/evals/chat-recovery.json",
    "shared/manifests/routes.json", "shared/manifests/source-index.json", "shared/models/gpt-5.6-sol.json",
    "shared/policies/connector-native-integrity.md", "shared/policies/github-write-safety.md", "shared/policies/gpt-5.6-sol.md",
    "shared/policies/network-and-transport.md", "shared/policies/repository-context-and-authorization.md",
    "shared/profiles/electron.json", "shared/profiles/generic.json", "shared/profiles/node.json", "shared/profiles/rust.json", "shared/profiles/typescript.json",
    "shared/references/gpt-5.6-sol-prompting-guidance.md", "shared/references/parallel-execution-policy-verbatim.md",
    "shared/templates/gpt-5.6-prompt-contract.md", "shared/templates/prompts.md",
}
expected = static | {item["skillFile"] for item in skills}
for item in load(SHARED / "manifests/source-index.json").get("sources", []):
    manifest_path = "shared/" + item["path"]
    expected.add(manifest_path)
    manifest = load(ROOT / manifest_path)
    if manifest.get("path"):
        expected.add("shared/" + manifest["path"])

actual = {
    path.relative_to(ROOT).as_posix()
    for path in ROOT.rglob("*")
    if path.is_file()
    and path != INTEGRITY
    and "dist" not in path.parts
    and "__pycache__" not in path.parts
    and ".git" not in path.parts
}
if actual != expected:
    if expected - actual:
        errors.append("inventory missing: " + ", ".join(sorted(expected - actual)))
    if actual - expected:
        errors.append("inventory extra: " + ", ".join(sorted(actual - expected)))

integrity = load(INTEGRITY)
inventory_text = "\n".join(sorted(expected)) + "\n"
if integrity.get("inventory", {}).get("count") != len(expected):
    errors.append("integrity inventory count")
if integrity.get("inventory", {}).get("sha256") != hashlib.sha256(inventory_text.encode()).hexdigest():
    errors.append("integrity inventory hash")
if integrity.get("individualSkillCount") != 17 or integrity.get("crossCuttingSkillCount") != 3:
    errors.append("integrity skill counts")

chat_integrity = integrity.get("chatRecovery", {})
for key in [
    "autoAttachOnInterruptedDelegatedChat",
    "fullWorkspaceInventoryBeforeMutation",
    "includesAllWorkspaceFiles",
    "reuseExistingValidFiles",
    "prohibitsUnnecessaryRegeneration",
    "unknownStateIsNotNotStarted",
    "idempotentContinuationPrompt",
    "promptOnlyResponse",
]:
    if not chat_integrity.get(key):
        errors.append("integrity chat recovery " + key)
if chat_integrity.get("inventoryBoundary") != "active-workspace-only":
    errors.append("integrity chat recovery boundary")

local_integrity = integrity.get("localGitWorkspace", {})
for key in ["autoAttachBeforeLocalGit", "requiresRootRuntime", "prohibitsSafeDirectoryFallback"]:
    if not local_integrity.get(key):
        errors.append("integrity local Git " + key)

delegated_integrity = integrity.get("delegatedResultContinuation", {})
for key in ["promptOnly", "singleCodeBlock", "noTextOutsidePrompt", "additionalDetailInsidePrompt", "preserveCompletedWork"]:
    if not delegated_integrity.get(key):
        errors.append("integrity delegated-return " + key)

for item in integrity.get("protectedFiles", []):
    path = ROOT / item["path"]
    require(path)
    if path.is_file() and (digest(path) != item["sha256"] or len(path.read_bytes()) != item["bytes"]):
        errors.append("protected file mismatch " + item["path"])

with tempfile.TemporaryDirectory() as directory:
    compiled_a = Path(directory) / "a.md"
    compiled_b = Path(directory) / "b.md"
    for output in [compiled_a, compiled_b]:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build_compiled.py"), "--output", str(output)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode:
            errors.append("compiled build failed: " + result.stdout + result.stderr)
    if compiled_a.exists() and compiled_b.exists() and compiled_a.read_bytes() != compiled_b.read_bytes():
        errors.append("compiled build nondeterministic")

    flat = Path(directory) / "flat"
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_chatgpt_flat.py"), "--output", str(flat)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        errors.append("flat build failed: " + result.stdout + result.stderr)
    elif len(list(flat.iterdir())) > 25:
        errors.append("flat build exceeds 25 files")

if errors:
    print("VALIDATION: FAIL")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("VALIDATION: PASS")
print("individual_skills:", len(ids))
print("cross_cutting_skills: 3")
print("chat_recovery: full-workspace-inventory-before-mutation")
print("chat_recovery_evals:", len(chat_cases))
print("delegated_result_continuation: prompt-only")
print("local_git_workspace: preflight-before-local-git")
print("parallel_execution: auto-attach-when-applicable")
print("canonical_sources: 15 lossless")
print("github_read_entries: 56")
print("github_write_entries: 41")
print("github_remote: connector-only")
print("github_workflows: absent")
