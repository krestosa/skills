from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

CANDIDATE = Path(__file__).resolve().parents[1]
SCRIPTS = CANDIDATE / "scripts"
sys.path.insert(0, os.fspath(SCRIPTS))

import repository_tooling  # noqa: E402
from repository_tooling import (  # noqa: E402
    ToolingError,
    build_compiled,
    build_flat,
    derive_integrity,
    discover_tasks,
    git_preflight,
    load_repository_model,
    parse_github_remote_url,
    publish_branch,
    refresh_integrity,
    safe_path,
    sanitize_remote_url,
    select_skills,
    sha256_bytes,
    suggest_commit,
    tree_hash,
    validate_inventory,
    validate_model_descriptor,
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def skill_text(skill_id: str) -> str:
    return f"---\nname: {skill_id}\ndescription: fixture\n---\n\n# {skill_id}\n\n## Role\nFixture\n"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Fixture:
    def __init__(self, root: Path, *, space: bool = False):
        self.root = root / ("repo with spaces" if space else "repo")
        self.root.mkdir(parents=True)
        (self.root / "SKILL.md").write_text("# Main\n", encoding="utf-8")
        (self.root / "README.md").write_text("# Fixture\n", encoding="utf-8")
        (self.root / "orchestrator").mkdir()
        (self.root / "orchestrator/SKILL.md").write_text("# Orchestrator\n", encoding="utf-8")
        (self.root / "orchestrator/delegation-envelope.schema.json").write_text("{}\n", encoding="utf-8")
        (self.root / "scripts").mkdir()
        for name in [
            "repository_tooling.py",
            "tooling.py",
            "build_compiled.py",
            "build_chatgpt_flat.py",
            "validate.py",
            "validate_gpt56.py",
            "verify_lossless.py",
        ]:
            shutil.copy2(SCRIPTS / name, self.root / "scripts" / name)
        self.skills = [
            self._skill("alpha", role=None),
            self._skill("cross", role="cross-cutting"),
        ]
        self._source("01-source", b"alpha\nbeta\n", [0, 6, 11])
        self._model()
        self._routes()
        self._tooling(max_files=20)
        self._registry()
        self.refresh()

    def _skill(self, skill_id: str, *, role: str | None = None, dependencies: list[str] | None = None) -> dict:
        path = self.root / "skills" / skill_id / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(skill_text(skill_id), encoding="utf-8")
        item = {
            "id": skill_id,
            "skillFile": f"skills/{skill_id}/SKILL.md",
            "requiredRoutes": ["base"],
            "optionalRoutes": [],
            "dependencies": dependencies or [],
            "capabilities": {"remoteReads": False, "remoteWrites": False, "localWrites": False},
            "loadPolicy": {"onDemand": True},
        }
        if role:
            item["role"] = role
        return item

    def _source(self, name: str, data: bytes, bounds: list[int]) -> None:
        shared = self.root / "shared"
        source_rel = f"sources/{name}.md"
        manifest_rel = f"manifests/sources/{name}.json"
        source = shared / source_rel
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(data)
        sections = []
        for index, (start, end) in enumerate(zip(bounds, bounds[1:]), 1):
            chunk = data[start:end]
            sections.append({
                "id": f"{name}.{index}",
                "startByte": start,
                "endByte": end,
                "bytes": len(chunk),
                "sha256": sha256_bytes(chunk),
            })
        manifest = {
            "schemaVersion": 1,
            "path": source_rel,
            "bytes": len(data),
            "sha256": sha256_bytes(data),
            "sections": sections,
        }
        manifest_path = shared / manifest_rel
        write_json(manifest_path, manifest)
        index_path = shared / "manifests/source-index.json"
        if index_path.exists():
            index = json.loads(index_path.read_text(encoding="utf-8"))
        else:
            index = {"schemaVersion": 1, "sources": []}
        index["sources"].append({
            "path": manifest_rel,
            "canonicalPath": source_rel,
            "sha256": file_hash(manifest_path),
        })
        write_json(index_path, index)

    def _model(self) -> None:
        shared = self.root / "shared"
        resources = {
            "policyFile": "policies/model.md",
            "referenceFile": "references/model.md",
            "promptTemplateFile": "templates/model.md",
            "evalFile": "evals/model.json",
        }
        for key, rel in resources.items():
            path = shared / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if key == "evalFile":
                write_json(path, {"schemaVersion": 1, "model": "fixture-model", "cases": [{"id": "case-1", "input": {}, "expected": {}}]})
            else:
                path.write_text(f"# {key}\n", encoding="utf-8")
        descriptor = {
            "schemaVersion": 1,
            "id": "fixture-model",
            **resources,
            "prompt": {"structure": ["role", "goal"]},
            "validation": {"minimumEvalCases": 1},
            "integrity": {
                "referenceSha256": file_hash(shared / resources["referenceFile"]),
                "policySha256": file_hash(shared / resources["policyFile"]),
                "promptTemplateSha256": file_hash(shared / resources["promptTemplateFile"]),
                "evalSha256": file_hash(shared / resources["evalFile"]),
            },
        }
        write_json(shared / "models/model.json", descriptor)

    def _routes(self) -> None:
        write_json(self.root / "shared/manifests/routes.json", {
            "schemaVersion": 1,
            "skill": "orchestrator",
            "entrypoint": "orchestrator/SKILL.md",
            "alwaysFiles": [],
            "routes": {"base": {"sections": ["01-source.1"], "files": []}},
            "profiles": {},
            "sourceIndex": "manifests/source-index.json",
            "modelProfileFile": "models/model.json",
            "defaultCompiledRoutes": ["base"],
            "sourceRoot": "shared",
        })

    def _tooling(self, *, max_files: int) -> None:
        write_json(self.root / "shared/manifests/tooling.json", {
            "schemaVersion": 1,
            "scriptsRoot": "scripts",
            "testsRoot": "tests",
            "integrityFile": "shared/manifests/integrity.json",
            "integritySchemaVersion": 1,
            "ignoredDirectories": ["dist"],
            "declaredFiles": ["orchestrator/delegation-envelope.schema.json"],
            "flatBuild": {
                "maxFiles": max_files,
                "groups": [
                    {"name": "MODEL", "collections": ["models", "policies", "references", "templates", "evals"]},
                    {"name": "SOURCES", "collections": ["sources", "manifests"]},
                ],
                "instructionText": "fixture instructions",
            },
        })

    def _registry(self) -> None:
        write_json(self.root / "orchestrator/registry.json", {
            "schemaVersion": 1,
            "orchestrator": "orchestrator/SKILL.md",
            "shared": {
                "root": "shared",
                "routesManifest": "shared/manifests/routes.json",
                "modelPolicy": "shared/policies/model.md",
            },
            "selectionPolicy": {"crossCuttingSkillIds": ["cross"]},
            "skills": self.skills,
        })

    def refresh(self) -> None:
        model = load_repository_model(self.root)
        refresh_integrity(model, write=True)

    def model(self):
        return load_repository_model(self.root)


class DynamicToolingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.fixture = Fixture(Path(self.temp.name))

    def test_add_registered_skill_without_script_edit(self) -> None:
        self.fixture.skills.append(self.fixture._skill("beta"))
        self.fixture._registry()
        self.fixture.refresh()
        model = self.fixture.model()
        self.assertIn("beta", model.skills_by_id)
        self.assertEqual(len(model.skill_order), 3)

    def test_remove_skill_recalculates_counts(self) -> None:
        self.fixture.skills = [item for item in self.fixture.skills if item["id"] != "alpha"]
        shutil.rmtree(self.fixture.root / "skills/alpha")
        self.fixture._registry()
        self.fixture.refresh()
        self.assertEqual(derive_integrity(self.fixture.model())["counts"]["registeredSkills"], 1)

    def test_existing_unregistered_skill_is_extra(self) -> None:
        self.fixture._skill("orphan")
        with self.assertRaisesRegex(ToolingError, "INVENTORY_EXTRA"):
            validate_inventory(self.fixture.model())

    def test_registered_missing_skill_is_rejected(self) -> None:
        shutil.rmtree(self.fixture.root / "skills/alpha")
        with self.assertRaisesRegex(ToolingError, "MISSING_PATH"):
            self.fixture.model()

    def test_add_eval_case_is_derived(self) -> None:
        path = self.fixture.root / "shared/evals/model.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["cases"].append({"id": "case-2", "input": {}, "expected": {}})
        write_json(path, data)
        descriptor_path = self.fixture.root / "shared/models/model.json"
        descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
        descriptor["integrity"]["evalSha256"] = file_hash(path)
        write_json(descriptor_path, descriptor)
        self.fixture.refresh()
        result = validate_model_descriptor(self.fixture.model())
        self.assertEqual(result["model"], "fixture-model")
        self.assertEqual(derive_integrity(self.fixture.model())["counts"]["evalCases"]["shared/evals/model.json"], 2)

    def test_add_source_is_derived(self) -> None:
        self.fixture._source("02-source", b"gamma\n", [0, 6])
        self.fixture.refresh()
        self.assertEqual(len(self.fixture.model().canonical_sources), 2)

    def test_source_manifest_hash_mismatch(self) -> None:
        index = self.fixture.root / "shared/manifests/source-index.json"
        data = json.loads(index.read_text(encoding="utf-8"))
        data["sources"][0]["sha256"] = "0" * 64
        write_json(index, data)
        with self.assertRaisesRegex(ToolingError, "SOURCE_MANIFEST_HASH"):
            self.fixture.model()

    def _mutate_bounds(self, first_end: int, second_start: int) -> None:
        path = self.fixture.root / "shared/manifests/sources/01-source.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        source = (self.fixture.root / "shared/sources/01-source.md").read_bytes()
        data["sections"][0]["endByte"] = first_end
        first_chunk = source[data["sections"][0]["startByte"]:first_end]
        data["sections"][0]["bytes"] = len(first_chunk)
        data["sections"][0]["sha256"] = sha256_bytes(first_chunk)
        data["sections"][1]["startByte"] = second_start
        second_chunk = source[second_start:data["sections"][1]["endByte"]]
        data["sections"][1]["bytes"] = len(second_chunk)
        data["sections"][1]["sha256"] = sha256_bytes(second_chunk)
        write_json(path, data)
        index_path = self.fixture.root / "shared/manifests/source-index.json"
        index = json.loads(index_path.read_text(encoding="utf-8"))
        index["sources"][0]["sha256"] = file_hash(path)
        write_json(index_path, index)

    def test_gap_detected(self) -> None:
        self._mutate_bounds(5, 6)
        with self.assertRaisesRegex(ToolingError, "SECTION_GAP"):
            self.fixture.model()

    def test_overlap_detected(self) -> None:
        self._mutate_bounds(7, 6)
        with self.assertRaisesRegex(ToolingError, "SECTION_OVERLAP"):
            self.fixture.model()

    def test_unknown_dependency(self) -> None:
        self.fixture.skills[0]["dependencies"] = ["missing"]
        self.fixture._registry()
        with self.assertRaisesRegex(ToolingError, "UNKNOWN_DEPENDENCY"):
            self.fixture.model()

    def test_dependency_cycle(self) -> None:
        self.fixture.skills[0]["dependencies"] = ["cross"]
        self.fixture.skills[1]["dependencies"] = ["alpha"]
        self.fixture._registry()
        with self.assertRaisesRegex(ToolingError, "DEPENDENCY_CYCLE"):
            self.fixture.model()

    def test_route_cycle(self) -> None:
        path = self.fixture.root / "shared/manifests/routes.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["routes"] = {"a": {"extends": ["b"]}, "b": {"extends": ["a"]}}
        for item in self.fixture.skills:
            item["requiredRoutes"] = ["a"]
        self.fixture._registry()
        write_json(path, data)
        with self.assertRaisesRegex(ToolingError, "ROUTE_CYCLE"):
            self.fixture.model()

    def test_flat_limit_is_configuration(self) -> None:
        config = self.fixture.root / "shared/manifests/tooling.json"
        data = json.loads(config.read_text(encoding="utf-8"))
        data["flatBuild"]["maxFiles"] = 1
        write_json(config, data)
        with self.assertRaisesRegex(ToolingError, "FLAT_FILE_LIMIT"):
            build_flat(self.fixture.model(), self.fixture.root / "dist/flat")

    def test_build_outputs_are_deterministic(self) -> None:
        model = self.fixture.model()
        a = self.fixture.root / "dist/a.md"
        b = self.fixture.root / "dist/b.md"
        build_compiled(model, a)
        build_compiled(model, b)
        self.assertEqual(a.read_bytes(), b.read_bytes())
        flat_a = self.fixture.root / "dist/fa"
        flat_b = self.fixture.root / "dist/fb"
        build_flat(model, flat_a)
        build_flat(model, flat_b)
        self.assertEqual(tree_hash(flat_a), tree_hash(flat_b))

    def test_execute_from_different_cwd(self) -> None:
        result = subprocess.run(
            [sys.executable, os.fspath(self.fixture.root / "scripts/validate_gpt56.py"), "--root", os.fspath(self.fixture.root)],
            cwd=Path(self.temp.name),
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_path_with_spaces(self) -> None:
        other = Fixture(Path(self.temp.name) / "second", space=True)
        self.assertEqual(other.model().root, other.root.resolve())

    def test_path_traversal_rejected(self) -> None:
        with self.assertRaisesRegex(ToolingError, "UNSAFE_PATH"):
            safe_path(self.fixture.root, "../escape", entity="test")

    def test_dynamic_task_discovery_and_private_exclusion(self) -> None:
        for name in ["validate_new.py", "build_new.py", "_validate_helper.py"]:
            (self.fixture.root / "scripts" / name).write_text("raise SystemExit(0)\n", encoding="utf-8")
        model = self.fixture.model()
        self.assertIn("validate_new", [path.stem for path in discover_tasks(model, "validate")])
        self.assertIn("build_new", [path.stem for path in discover_tasks(model, "build")])
        self.assertNotIn("_validate_helper", [path.stem for path in discover_tasks(model, "validate")])


    def test_dependency_closure_and_generic_exclusion(self) -> None:
        self.fixture.skills[0]["dependencies"] = ["cross"]
        self.fixture._registry()
        self.fixture.refresh()
        model = self.fixture.model()
        self.assertEqual(select_skills(model, skills=["alpha"]), ["alpha", "cross"])
        with self.assertRaisesRegex(ToolingError, "EXCLUDED_DEPENDENCY"):
            select_skills(model, skills=["alpha"], exclude=["cross"])

    def test_unknown_discovered_task_is_rejected(self) -> None:
        from repository_tooling import run_tasks

        with self.assertRaisesRegex(ToolingError, "UNKNOWN_TASK"):
            run_tasks(self.fixture.model(), "validate", selected=["validate_missing"])

    def _git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(["git", "-C", os.fspath(self.fixture.root), *args], text=True, capture_output=True)
        if check and result.returncode:
            self.fail(result.stdout + result.stderr)
        return result

    def _init_git(self) -> None:
        self._git("init", "-b", "main")
        self._git("config", "user.name", "Fixture")
        self._git("config", "user.email", "fixture@example.invalid")
        self._git("add", "-A")
        self._git("commit", "-m", "baseline")

    def test_commit_suggestion_is_stable(self) -> None:
        self._init_git()
        (self.fixture.root / "scripts/new_tool.py").write_text("x = 1\n", encoding="utf-8")
        (self.fixture.root / "shared/manifests/new.json").write_text("{}\n", encoding="utf-8")
        model = self.fixture.model()
        first = suggest_commit(model)
        second = suggest_commit(model)
        self.assertEqual(first["subject"], second["subject"])
        self.assertEqual(first["subject"], "Update repository tooling and metadata")

    def test_no_changes_rejected(self) -> None:
        self._init_git()
        with self.assertRaisesRegex(ToolingError, "NO_CHANGES"):
            suggest_commit(self.fixture.model())

    def test_detached_head_rejected(self) -> None:
        self._init_git()
        self._git("checkout", "--detach", "HEAD")
        with self.assertRaisesRegex(ToolingError, "DETACHED_HEAD"):
            git_preflight(self.fixture.model())

    def test_conflicts_rejected(self) -> None:
        self._init_git()
        target = self.fixture.root / "README.md"
        self._git("checkout", "-b", "other")
        target.write_text("other\n", encoding="utf-8")
        self._git("add", "README.md")
        self._git("commit", "-m", "other")
        self._git("checkout", "main")
        target.write_text("main\n", encoding="utf-8")
        self._git("add", "README.md")
        self._git("commit", "-m", "main")
        self._git("merge", "other", check=False)
        with self.assertRaisesRegex(ToolingError, "GIT_OPERATION_IN_PROGRESS|GIT_CONFLICTS"):
            git_preflight(self.fixture.model())


    def test_real_commit_creates_one_local_commit(self) -> None:
        self._init_git()
        baseline = self._git("rev-list", "--count", "HEAD").stdout.strip()
        (self.fixture.root / "README.md").write_text("committed change\n", encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                os.fspath(self.fixture.root / "scripts/tooling.py"),
                "--root",
                os.fspath(self.fixture.root),
                "commit",
                "--auto-message",
            ],
            cwd=Path(self.temp.name),
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(int(self._git("rev-list", "--count", "HEAD").stdout.strip()), int(baseline) + 1)
        self.assertEqual(self._git("status", "--porcelain=v1").stdout, "")

    def test_commit_dry_run_preserves_git_state(self) -> None:
        self._init_git()
        (self.fixture.root / "README.md").write_text("changed\n", encoding="utf-8")
        before_head = self._git("rev-parse", "HEAD").stdout
        before_status = self._git("status", "--porcelain=v1").stdout
        result = subprocess.run(
            [
                sys.executable,
                os.fspath(self.fixture.root / "scripts/tooling.py"),
                "--root",
                os.fspath(self.fixture.root),
                "commit",
                "--dry-run",
                "--auto-message",
            ],
            cwd=Path(self.temp.name),
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before_head, self._git("rev-parse", "HEAD").stdout)
        self.assertEqual(before_status, self._git("status", "--porcelain=v1").stdout)


class PublicationToolingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.fixture = Fixture(self.base / "fixture")
        self.git_binary = shutil.which("git")
        if not self.git_binary:
            self.skipTest("git is required")

    def _git(self, *args: str, cwd: Path | None = None, check: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        root = cwd or self.fixture.root
        result = subprocess.run(
            [self.git_binary, "-C", os.fspath(root), *args],
            text=True,
            capture_output=True,
            env=env,
        )
        if check and result.returncode:
            self.fail(result.stdout + result.stderr)
        return result

    def _initialize_remote(
        self,
        *,
        default_branch: str = "trunk",
        remote_name: str = "origin",
        url_style: str = "https",
        create_feature_commit: bool = True,
    ) -> tuple[Path, str]:
        root = self.fixture.root
        self._git("init", "-b", default_branch)
        self._git("config", "user.name", "Fixture")
        self._git("config", "user.email", "fixture@example.invalid")
        self._git("add", "-A")
        self._git("commit", "-m", "baseline")
        baseline = self._git("rev-parse", "HEAD").stdout.strip()

        bare = self.base / f"{remote_name}.git"
        subprocess.run([self.git_binary, "init", "--bare", os.fspath(bare)], check=True, text=True, capture_output=True)
        subprocess.run(
            [self.git_binary, "--git-dir", os.fspath(bare), "symbolic-ref", "HEAD", f"refs/heads/{default_branch}"],
            check=True,
            text=True,
            capture_output=True,
        )
        if url_style == "https":
            logical_url = f"https://github.com/fixture/{remote_name}-repo.git"
        elif url_style == "ssh":
            logical_url = f"git@github.com:fixture/{remote_name}-repo.git"
        elif url_style == "ssh-url":
            logical_url = f"ssh://git@github.com/fixture/{remote_name}-repo.git"
        else:
            raise AssertionError(url_style)
        self._git("config", f"url.{bare.resolve().as_uri()}.insteadOf", logical_url)
        self._git("remote", "add", remote_name, logical_url)
        self._git("push", remote_name, f"HEAD:refs/heads/{default_branch}")
        self._git("fetch", "--prune", remote_name)
        self._git("remote", "set-head", remote_name, "-a")
        if create_feature_commit:
            self._git("checkout", "-b", "tooling/test")
            (root / "README.md").write_text("published change\n", encoding="utf-8")
            self._git("add", "README.md")
            self._git("commit", "-m", "feature")
        return bare, baseline

    def _remote_sha(self, bare: Path, branch: str) -> str | None:
        result = subprocess.run(
            [self.git_binary, "--git-dir", os.fspath(bare), "rev-parse", "--verify", f"refs/heads/{branch}"],
            text=True,
            capture_output=True,
        )
        return result.stdout.strip() if result.returncode == 0 else None

    def _cli(self, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, os.fspath(self.fixture.root / "scripts/tooling.py"), "--root", os.fspath(self.fixture.root), *args],
            cwd=self.base,
            text=True,
            capture_output=True,
            env=env,
        )

    def _network_guard(self) -> tuple[dict[str, str], Path]:
        bin_dir = self.base / "guard-bin"
        bin_dir.mkdir(exist_ok=True)
        log = self.base / "network.log"
        wrapper = bin_dir / "git"
        wrapper.write_text(
            "#!/bin/sh\n"
            "for arg in \"$@\"; do\n"
            "  case \"$arg\" in fetch|push|ls-remote) printf '%s\\n' \"$*\" >> \"$NETWORK_LOG\"; exit 97;; esac\n"
            "done\n"
            f"exec {self.git_binary} \"$@\"\n",
            encoding="utf-8",
        )
        wrapper.chmod(0o755)
        env = dict(os.environ)
        env["PATH"] = os.fspath(bin_dir) + os.pathsep + env.get("PATH", "")
        env["NETWORK_LOG"] = os.fspath(log)
        return env, log

    def test_publish_new_branch_and_upstream(self) -> None:
        bare, _ = self._initialize_remote()
        result = publish_branch(self.fixture.model())
        head = self._git("rev-parse", "HEAD").stdout.strip()
        self.assertTrue(result["pushed"])
        self.assertEqual(self._remote_sha(bare, "tooling/test"), head)
        self.assertEqual(self._git("rev-parse", "--abbrev-ref", "@{upstream}").stdout.strip(), "origin/tooling/test")

    def test_publish_idempotent(self) -> None:
        bare, _ = self._initialize_remote()
        first = publish_branch(self.fixture.model())
        second = publish_branch(self.fixture.model())
        self.assertTrue(first["pushed"])
        self.assertFalse(second["pushed"])
        self.assertTrue(second["idempotent"])
        self.assertEqual(second["collision"], "EXACT")
        self.assertEqual(self._remote_sha(bare, "tooling/test"), self._git("rev-parse", "HEAD").stdout.strip())

    def test_reject_divergent_remote_branch(self) -> None:
        bare, baseline = self._initialize_remote()
        subprocess.run([self.git_binary, "--git-dir", os.fspath(bare), "update-ref", "refs/heads/tooling/test", baseline], check=True)
        with self.assertRaisesRegex(ToolingError, "REMOTE_BRANCH_DIVERGED"):
            publish_branch(self.fixture.model())

    def test_reject_default_branch(self) -> None:
        self._initialize_remote(create_feature_commit=False)
        with self.assertRaisesRegex(ToolingError, "DEFAULT_BRANCH_PROTECTED"):
            publish_branch(self.fixture.model())

    def test_reject_dirty_worktree(self) -> None:
        self._initialize_remote()
        (self.fixture.root / "README.md").write_text("dirty\n", encoding="utf-8")
        with self.assertRaisesRegex(ToolingError, "WORKTREE_DIRTY"):
            publish_branch(self.fixture.model())

    def test_reject_dirty_index(self) -> None:
        self._initialize_remote()
        (self.fixture.root / "README.md").write_text("staged\n", encoding="utf-8")
        self._git("add", "README.md")
        with self.assertRaisesRegex(ToolingError, "INDEX_DIRTY"):
            publish_branch(self.fixture.model())

    def test_reject_detached_head(self) -> None:
        self._initialize_remote()
        self._git("checkout", "--detach", "HEAD")
        with self.assertRaisesRegex(ToolingError, "DETACHED_HEAD"):
            publish_branch(self.fixture.model())

    def test_reject_conflicts(self) -> None:
        self._initialize_remote()
        root = self.fixture.root
        self._git("checkout", "-b", "other", "origin/trunk")
        (root / "README.md").write_text("other\n", encoding="utf-8")
        self._git("add", "README.md")
        self._git("commit", "-m", "other")
        self._git("checkout", "tooling/test")
        self._git("merge", "other", check=False)
        with self.assertRaisesRegex(ToolingError, "GIT_OPERATION_IN_PROGRESS|GIT_CONFLICTS"):
            publish_branch(self.fixture.model())

    def test_reject_operation_in_progress(self) -> None:
        self._initialize_remote()
        git_dir = Path(self._git("rev-parse", "--git-dir").stdout.strip())
        if not git_dir.is_absolute():
            git_dir = self.fixture.root / git_dir
        (git_dir / "REVERT_HEAD").write_text(self._git("rev-parse", "HEAD").stdout.strip() + "\n", encoding="ascii")
        with self.assertRaisesRegex(ToolingError, "GIT_OPERATION_IN_PROGRESS"):
            publish_branch(self.fixture.model())

    def test_resolve_trunk_via_ls_remote(self) -> None:
        self._initialize_remote(default_branch="trunk")
        self._git("symbolic-ref", "-d", "refs/remotes/origin/HEAD", check=False)
        result = publish_branch(self.fixture.model(), dry_run=True)
        self.assertEqual(result["defaultBranch"], "trunk")
        self.assertEqual(result["defaultBranchSource"], "ls-remote-symref")

    def test_non_origin_remote(self) -> None:
        bare, _ = self._initialize_remote(remote_name="upstream")
        result = publish_branch(self.fixture.model(), remote="upstream")
        self.assertEqual(result["remote"], "upstream")
        self.assertEqual(self._remote_sha(bare, "tooling/test"), self._git("rev-parse", "HEAD").stdout.strip())

    def test_accept_https_url(self) -> None:
        self.assertEqual(parse_github_remote_url("https://github.com/owner/repo.git"), ("owner", "repo"))

    def test_accept_ssh_urls(self) -> None:
        self.assertEqual(parse_github_remote_url("git@github.com:owner/repo.git"), ("owner", "repo"))
        self.assertEqual(parse_github_remote_url("ssh://git@github.com/owner/repo.git"), ("owner", "repo"))

    def test_sanitize_credentials(self) -> None:
        secret = "github_pat_secretvalue"
        sanitized = sanitize_remote_url(f"https://user:{secret}@github.com/owner/repo.git")
        self.assertNotIn(secret, sanitized)
        self.assertIn("***@github.com", sanitized)

    def test_validate_build_check_do_not_use_network(self) -> None:
        env, log = self._network_guard()
        for command in (("validate",), ("build", "--temporary"), ("check",)):
            result = self._cli(*command, env=env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(log.exists(), log.read_text() if log.exists() else "")

    def test_commit_without_push_does_not_use_network(self) -> None:
        self._initialize_remote(create_feature_commit=False)
        self._git("checkout", "-b", "tooling/test")
        (self.fixture.root / "README.md").write_text("commit only\n", encoding="utf-8")
        env, log = self._network_guard()
        result = self._cli("commit", "--auto-message", env=env)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(log.exists(), log.read_text() if log.exists() else "")

    def test_commit_with_push_publishes_after_commit(self) -> None:
        bare, _ = self._initialize_remote(create_feature_commit=False)
        self._git("checkout", "-b", "tooling/test")
        (self.fixture.root / "README.md").write_text("commit and push\n", encoding="utf-8")
        before = self._git("rev-parse", "HEAD").stdout.strip()
        result = self._cli("commit", "--auto-message", "--push")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        after = self._git("rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(before, after)
        self.assertEqual(self._remote_sha(bare, "tooling/test"), after)

    def test_push_failure_preserves_local_commit(self) -> None:
        bare, _ = self._initialize_remote(create_feature_commit=False)
        hook = bare / "hooks/pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        hook.chmod(0o755)
        self._git("checkout", "-b", "tooling/test")
        (self.fixture.root / "README.md").write_text("preserved commit\n", encoding="utf-8")
        before = self._git("rev-parse", "HEAD").stdout.strip()
        result = self._cli("commit", "--auto-message", "--push")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        after = self._git("rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(before, after)
        self.assertIsNone(self._remote_sha(bare, "tooling/test"))
        self.assertIn("LOCALCOMMIT", result.stdout.replace("_", "").upper())
        self.assertIn("REMOTEPUBLICATION", result.stdout.replace("_", "").upper())

    def test_publish_dry_run_has_no_mutations(self) -> None:
        bare, _ = self._initialize_remote()
        before_head = self._git("rev-parse", "HEAD").stdout
        before_status = self._git("status", "--porcelain=v1").stdout
        before_refs = self._git("show-ref").stdout
        before_config = self._git("config", "--local", "--list").stdout
        before_remote = self._remote_sha(bare, "tooling/test")
        result = publish_branch(self.fixture.model(), dry_run=True)
        self.assertTrue(result["wouldPush"])
        self.assertEqual(before_head, self._git("rev-parse", "HEAD").stdout)
        self.assertEqual(before_status, self._git("status", "--porcelain=v1").stdout)
        self.assertEqual(before_refs, self._git("show-ref").stdout)
        self.assertEqual(before_config, self._git("config", "--local", "--list").stdout)
        self.assertEqual(before_remote, self._remote_sha(bare, "tooling/test"))

    def test_publish_json_output(self) -> None:
        self._initialize_remote()
        result = self._cli("--json", "publish", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["collision"], "ABSENT")
        self.assertFalse(payload["force"])

    def test_commit_dry_run_push_has_no_mutations(self) -> None:
        self._initialize_remote(create_feature_commit=False)
        self._git("checkout", "-b", "tooling/test")
        (self.fixture.root / "README.md").write_text("pending\n", encoding="utf-8")
        before_head = self._git("rev-parse", "HEAD").stdout
        before_status = self._git("status", "--porcelain=v1").stdout
        before_refs = self._git("show-ref").stdout
        result = self._cli("commit", "--dry-run", "--auto-message", "--push")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before_head, self._git("rev-parse", "HEAD").stdout)
        self.assertEqual(before_status, self._git("status", "--porcelain=v1").stdout)
        self.assertEqual(before_refs, self._git("show-ref").stdout)

    def test_push_command_never_contains_force(self) -> None:
        bare, _ = self._initialize_remote()
        calls: list[tuple[str, ...]] = []
        original_remote_git = repository_tooling.remote_git

        def recording_remote_git(model, *args: str, **kwargs):
            calls.append(tuple(args))
            return original_remote_git(model, *args, **kwargs)

        with mock.patch.object(
            repository_tooling,
            "remote_git",
            side_effect=recording_remote_git,
        ):
            result = publish_branch(self.fixture.model())

        self.assertTrue(result["pushed"])
        push_calls = [arguments for arguments in calls if arguments and arguments[0] == "push"]
        self.assertEqual(len(push_calls), 1, calls)
        arguments = push_calls[0]
        self.assertNotIn("--force", arguments)
        self.assertNotIn("--force-with-lease", arguments)
        self.assertNotIn("--mirror", arguments)
        self.assertNotIn("--all", arguments)
        self.assertNotIn("--tags", arguments)
        self.assertEqual(self._remote_sha(bare, "tooling/test"), self._git("rev-parse", "HEAD").stdout.strip())


if __name__ == "__main__":
    unittest.main()
