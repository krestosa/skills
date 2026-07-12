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
    ROOT / "README.md", ROOT / "SKILL.md", ROOT / "orchestrator/SKILL.md",
    ROOT / "orchestrator/registry.json", ROOT / "orchestrator/delegation-envelope.schema.json",
    ROOT / "scripts/build_chatgpt_flat.py", ROOT / "scripts/build_compiled.py",
    ROOT / "scripts/validate_gpt56.py", ROOT / "scripts/verify_lossless.py",
    SHARED / "manifests/routes.json", SHARED / "manifests/source-index.json",
    SHARED / "evals/parallel-execution.json", SHARED / "evals/local-git-workspace.json",
    SHARED / "evals/chat-recovery.json", SHARED / "references/parallel-execution-policy-verbatim.md",
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
    "Select one primary skill", "Do not load all skills preemptively",
    "Attach `chat-recovery`", "Attach `local-git-workspace`", "Attach `parallel-execution`",
    "inventory every accessible filesystem entry", "begin from `/`",
    "no date, Git, repository, workspace, owner, extension, or task-origin filter",
    "emit exactly one self-contained prompt inside one code block",
]:
    if marker not in orch:
        errors.append("orchestrator missing " + marker)

routes = load(SHARED / "manifests/routes.json").get("routes", {})
registry = load(ROOT / "orchestrator/registry.json")
skills = registry.get("skills", [])
ids = [item.get("id") for item in skills]
if len(ids) != 17 or len(ids) != len(set(ids)):
    errors.append("expected 17 unique skills")

headings = [
    "## Role", "## Personality", "## Collaboration style", "## Goal",
    "## Success criteria", "## Select when", "## Exclude when",
    "## Shared routes", "## Output", "## Stop rules",
]
for item in skills:
    skill_id = item.get("id")
    path = ROOT / f"skills/{skill_id}/SKILL.md"
    require(path)
    if item.get("skillFile") != f"skills/{skill_id}/SKILL.md":
        errors.append(f"{skill_id} path mismatch")
    text = path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""
    for heading in headings:
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
if selection.get("crossCuttingSkillIds") != ["parallel-execution", "local-git-workspace", "chat-recovery"]:
    errors.append("cross-cutting registry mismatch")
if not selection.get("ordinaryActiveSkillTarget", {}).get("excludesCrossCutting"):
    errors.append("cross-cutting target mismatch")

chat = next((item for item in skills if item.get("id") == "chat-recovery"), {})
chat_auto = selection.get("autoAttach", {}).get("chat-recovery", {})
if chat.get("role") != "cross-cutting" or any(chat.get("capabilities", {}).values()):
    errors.append("chat recovery capability boundary")
if chat.get("dependencies") != ["management-delegation"]:
    errors.append("chat recovery dependency mismatch")
for key in [
    "autoAttachWhenApplicable", "requiresFullEnvironmentInventoryBeforeMutation",
    "requiresIdempotentContinuationPrompt", "promptOnlyResponse",
]:
    if not chat.get("loadPolicy", {}).get(key):
        errors.append("chat recovery load policy " + key)
for key in [
    "requiresFullEnvironmentInventoryBeforeMutation", "discoversAllMountedFilesystems",
    "noDateFilter", "noGitRepositoryOrWorkspaceFilter",
    "inventoryIncludesAllAccessibleFilesystemEntries",
    "inventoryIncludesSystemUserWorkspaceTemporaryCacheGeneratedHiddenBinarySymlinkAndOutsideRepositoryFiles",
    "recordsExcludedVirtualFilesystems", "recordsInaccessiblePaths",
    "doesNotFollowSymlinksRecursively", "reuseExistingValidFiles",
    "prohibitsUnnecessaryGenerationAndRegeneration", "unknownStateIsNotNotStarted",
    "requiresIdempotentContinuationPrompt", "promptOnlyResponse",
    "doesNotAuthorizeSideEffects", "doesNotCountTowardOrdinaryActiveSkillTarget",
]:
    if not chat_auto.get(key):
        errors.append("chat recovery auto-attach " + key)
if chat_auto.get("inventoryBoundary") != "accessible-runtime-filesystem":
    errors.append("chat recovery inventory boundary")
if chat_auto.get("inventoryStartsAt") != "/":
    errors.append("chat recovery inventory start")

chat_text = (ROOT / "skills/chat-recovery/SKILL.md").read_text(encoding="utf-8")
for marker in [
    "every accessible filesystem entry", "execution environment root `/`",
    "Apply no date filter", "Apply no Git filter", "outside-repository",
    "Do not follow symlinks recursively", "Record inaccessible paths",
    "procfs, sysfs, devtmpfs", "complete accessible runtime filesystem",
    "Existing files are evidence", "hash lazily",
    "exactly one self-contained recovery or continuation prompt",
]:
    if marker not in chat_text:
        errors.append("chat recovery skill missing " + marker)

management = (ROOT / "skills/management-delegation/SKILL.md").read_text(encoding="utf-8")
for marker in [
    "## Interrupted-chat procedure", "Attach `chat-recovery`",
    "inventory every accessible filesystem entry",
    "Apply no date, Git, repository, workspace, owner, extension, or task-origin filter",
    "return exactly one prompt inside one code block and nothing else",
]:
    if marker not in management:
        errors.append("delegation recovery contract missing " + marker)

chat_cases = load(SHARED / "evals/chat-recovery.json").get("cases", [])
case_ids = {item.get("id") for item in chat_cases}
for required_case in [
    "outside-workspace-artifact", "old-artifact-no-date-filter",
    "git-independent-coverage", "virtual-filesystems",
    "symlink-loop", "inaccessible-path",
]:
    if required_case not in case_ids:
        errors.append("missing chat recovery case " + required_case)
if len(case_ids) < 18:
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
    "README.md", "SKILL.md", "orchestrator/SKILL.md", "orchestrator/registry.json",
    "orchestrator/delegation-envelope.schema.json", "scripts/build_chatgpt_flat.py",
    "scripts/build_compiled.py", "scripts/validate.py", "scripts/validate_gpt56.py",
    "scripts/verify_lossless.py", "shared/catalogs/github-read-verbatim.md",
    "shared/catalogs/github-write-verbatim.md", "shared/contracts/authorization-envelope.schema.json",
    "shared/contracts/connector-contracts.md", "shared/core/identity.md",
    "shared/core/project-authority-and-roles.md", "shared/core/states-and-approval.md",
    "shared/evals/gpt-5.6-sol.json", "shared/evals/parallel-execution.json",
    "shared/evals/local-git-workspace.json", "shared/evals/chat-recovery.json",
    "shared/manifests/routes.json", "shared/manifests/source-index.json",
    "shared/models/gpt-5.6-sol.json", "shared/policies/connector-native-integrity.md",
    "shared/policies/github-write-safety.md", "shared/policies/gpt-5.6-sol.md",
    "shared/policies/network-and-transport.md",
    "shared/policies/repository-context-and-authorization.md",
    "shared/profiles/electron.json", "shared/profiles/generic.json",
    "shared/profiles/node.json", "shared/profiles/rust.json",
    "shared/profiles/typescript.json",
    "shared/references/gpt-5.6-sol-prompting-guidance.md",
    "shared/references/parallel-execution-policy-verbatim.md",
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
    if path.is_file() and path != INTEGRITY
    and "dist" not in path.parts and "__pycache__" not in path.parts
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
    "autoAttachOnInterruptedDelegatedChat", "fullEnvironmentInventoryBeforeMutation",
    "discoversAllMountedFilesystems", "noDateFilter",
    "noGitRepositoryOrWorkspaceFilter", "includesAllAccessibleFilesystemEntries",
    "recordsExcludedVirtualFilesystems", "recordsInaccessiblePaths",
    "reuseExistingValidFiles", "prohibitsUnnecessaryGenerationAndRegeneration",
    "unknownStateIsNotNotStarted", "idempotentContinuationPrompt", "promptOnlyResponse",
]:
    if not chat_integrity.get(key):
        errors.append("integrity chat recovery " + key)
if chat_integrity.get("inventoryBoundary") != "accessible-runtime-filesystem":
    errors.append("integrity chat recovery boundary")
if chat_integrity.get("inventoryStartsAt") != "/":
    errors.append("integrity chat recovery start")
if chat_integrity.get("evalCaseCount") != len(chat_cases):
    errors.append("integrity chat recovery eval count")

for item in integrity.get("protectedFiles", []):
    path = ROOT / item["path"]
    require(path)
    if path.is_file() and (digest(path) != item["sha256"] or len(path.read_bytes()) != item["bytes"]):
        errors.append("protected file mismatch " + item["path"])

with tempfile.TemporaryDirectory() as directory:
    a, b = Path(directory) / "a.md", Path(directory) / "b.md"
    for output in [a, b]:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build_compiled.py"), "--output", str(output)],
            cwd=ROOT, text=True, capture_output=True,
        )
        if result.returncode:
            errors.append("compiled build failed: " + result.stdout + result.stderr)
    if a.exists() and b.exists() and a.read_bytes() != b.read_bytes():
        errors.append("compiled build nondeterministic")
    flat = Path(directory) / "flat"
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_chatgpt_flat.py"), "--output", str(flat)],
        cwd=ROOT, text=True, capture_output=True,
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
print("chat_recovery: system-wide-inventory-before-mutation")
print("chat_recovery_evals:", len(chat_cases))
print("canonical_sources: 15 lossless")
print("github_read_entries: 56")
print("github_write_entries: 41")
print("github_remote: connector-only")
print("github_workflows: absent")
