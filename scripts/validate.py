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
INTEGRITY_PATH = SHARED / "manifests/integrity.json"
PARALLEL_REFERENCE = SHARED / "references/parallel-execution-policy-verbatim.md"
PARALLEL_REFERENCE_SHA256 = "804cc93be433bf159a7ac57d0778fbb72806c8306940343657079e8aa5db8126"
errors: list[str] = []

def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid json {path.relative_to(ROOT)}: {exc}")
        return {}

def require(path: Path) -> None:
    if not path.is_file():
        errors.append("missing " + path.relative_to(ROOT).as_posix())

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

required_controls = [
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
    PARALLEL_REFERENCE,
]
for path in required_controls:
    require(path)

# Single main, orchestrator, and README.
readmes = sorted(ROOT.rglob("README.md"))
if readmes != [ROOT / "README.md"]:
    errors.append("repository must contain exactly one README.md at root")

legacy_name = "skill" + "-orquestador"
legacy_label = "skill" + " " + "orquestador"
for forbidden in ["skills/main", "skills/orchestrator", "skills/individual", "skills/" + legacy_name]:
    if (ROOT / forbidden).exists():
        errors.append("duplicate legacy layer exists: " + forbidden)

for candidate in ROOT.rglob("*"):
    if legacy_name in candidate.as_posix():
        errors.append("legacy orchestrator path exists: " + candidate.relative_to(ROOT).as_posix())
    if (
        candidate.is_file()
        and candidate != ROOT / "scripts/validate.py"
        and candidate.suffix in {".md", ".json", ".py", ".txt"}
    ):
        text = candidate.read_text(encoding="utf-8", errors="ignore").lower()
        if legacy_name in text or legacy_label in text:
            errors.append("legacy orchestrator name in " + candidate.relative_to(ROOT).as_posix())

if (ROOT / ".github/workflows").exists():
    errors.append("GitHub workflows are prohibited")

main = (ROOT / "SKILL.md").read_text(encoding="utf-8")
orchestrator = (ROOT / "orchestrator/SKILL.md").read_text(encoding="utf-8")
if "orchestrator/SKILL.md" not in main:
    errors.append("main must load the orchestrator")
if re.search(r"skills/[a-z0-9-]+/SKILL\.md", main):
    errors.append("main must not load individual skills directly")

for marker in [
    "Select one primary skill",
    "Do not load all skills preemptively",
    "registry.json",
    "shared/manifests/routes.json",
    "Attach `parallel-execution`",
    "Cross-cutting auto-attached skills do not count",
]:
    if marker not in orchestrator:
        errors.append("orchestrator missing marker: " + marker)

routes = load_json(SHARED / "manifests/routes.json").get("routes", {})
registry = load_json(ROOT / "orchestrator/registry.json")
skills = registry.get("skills", [])
ids = [item.get("id") for item in skills]

if len(ids) != 15 or len(ids) != len(set(ids)):
    errors.append("expected 15 unique individual skills")

for item in skills:
    skill_id = item.get("id")
    expected = f"skills/{skill_id}/SKILL.md"
    if item.get("skillFile") != expected:
        errors.append(f"{skill_id} path must be {expected}")

    path = ROOT / expected
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
            errors.append(f"{skill_id} references unknown route {route}")

    for dependency in item.get("dependencies", []):
        if dependency not in ids:
            errors.append(f"{skill_id} unknown dependency {dependency}")

    for reference in item.get("referenceFiles", []):
        require(ROOT / reference)

    if not item.get("loadPolicy", {}).get("onDemand"):
        errors.append(f"{skill_id} must be on-demand")

# Cross-cutting auto-attach contract.
parallel = next((item for item in skills if item.get("id") == "parallel-execution"), None)
selection = registry.get("selectionPolicy", {})
auto_attach = selection.get("autoAttach", {}).get("parallel-execution", {})

if not parallel:
    errors.append("parallel-execution skill is missing")
else:
    if parallel.get("role") != "cross-cutting":
        errors.append("parallel-execution must be cross-cutting")
    if parallel.get("requiredRoutes") or parallel.get("optionalRoutes"):
        errors.append("parallel-execution must not duplicate shared routes")
    if parallel.get("referenceFiles") != ["shared/references/parallel-execution-policy-verbatim.md"]:
        errors.append("parallel-execution reference path mismatch")
    load_policy = parallel.get("loadPolicy", {})
    if not load_policy.get("autoAttachWhenApplicable"):
        errors.append("parallel-execution must auto-attach when applicable")
    if not load_policy.get("loadFullReferenceOnlyForAuditOrUncoveredEdgeCase"):
        errors.append("parallel reference must remain off the ordinary path")
    if any(parallel.get("capabilities", {}).values()):
        errors.append("parallel-execution must not grant read, write, or mutation capability")

if selection.get("crossCuttingSkillIds") != ["parallel-execution"]:
    errors.append("cross-cutting skill registry mismatch")
if not selection.get("ordinaryActiveSkillTarget", {}).get("excludesCrossCutting"):
    errors.append("cross-cutting skills must not count toward ordinary target")
if auto_attach.get("default") != "attach-when-applicable":
    errors.append("parallel-execution auto-attach default mismatch")
if not auto_attach.get("doesNotAuthorizeSideEffects"):
    errors.append("parallel-execution must not authorize side effects")
if not auto_attach.get("doesNotCountTowardOrdinaryActiveSkillTarget"):
    errors.append("parallel-execution must not count toward ordinary target")
if len(auto_attach.get("attachWhenAny", [])) < 3 or len(auto_attach.get("skipWhenAny", [])) < 4:
    errors.append("parallel-execution attach/skip decision rules are incomplete")

parallel_skill_path = ROOT / "skills/parallel-execution/SKILL.md"
if parallel_skill_path.is_file():
    parallel_text = parallel_skill_path.read_text(encoding="utf-8")
    for marker in [
        "dependency-graph, concurrency, and resource-lock controller",
        "canonical full path",
        "at most one active writer",
        "Never claim parallel execution",
        "one ordered integration path",
        "create one coherent commit",
    ]:
        if marker not in parallel_text:
            errors.append("parallel-execution missing invariant: " + marker)

if PARALLEL_REFERENCE.is_file():
    if sha256(PARALLEL_REFERENCE) != PARALLEL_REFERENCE_SHA256:
        errors.append("parallel policy reference hash mismatch")
    if len(PARALLEL_REFERENCE.read_bytes()) != 12903:
        errors.append("parallel policy reference byte count mismatch")

parallel_evals = load_json(SHARED / "evals/parallel-execution.json")
eval_cases = parallel_evals.get("cases", [])
eval_ids = [case.get("id") for case in eval_cases]
if len(eval_ids) < 10 or len(eval_ids) != len(set(eval_ids)):
    errors.append("parallel-execution eval inventory invalid")
expected_results = {
    "attach",
    "skip",
    "attach-with-local-serialization",
    "attach-with-shared-resource-serialization",
    "attach-with-external-serialization",
    "attach-with-exclusive-writer-and-revalidation",
}
if not expected_results.issubset({case.get("expected") for case in eval_cases}):
    errors.append("parallel-execution eval coverage incomplete")

# Verbatim connector catalogs.
def catalog_payload(path: Path) -> bytes:
    data = path.read_bytes()
    begin = b"<!-- VERBATIM_CATALOG_BEGIN -->\n"
    end = b"<!-- VERBATIM_CATALOG_END -->\n"
    return data[data.index(begin) + len(begin):data.index(end)].rstrip(b"\n")

for rel, count, digest in [
    ("catalogs/github-read-verbatim.md", 56, "610c387f5f7c9047c65fef08734d5199696230866ca79e270700209eaab1324e"),
    ("catalogs/github-write-verbatim.md", 41, "499373638143f48b0549701bf5036725a2c2bc9b332a95d9a053a1e1ce687a3d"),
]:
    path = SHARED / rel
    require(path)
    if path.is_file():
        payload = catalog_payload(path)
        if hashlib.sha256(payload).hexdigest() != digest:
            errors.append("catalog payload hash mismatch " + rel)
        if len([part for part in payload.decode().split("\n\n") if part.strip()]) != count:
            errors.append("catalog count mismatch " + rel)

# Canonical source and model validation.
for script, label in [
    (ROOT / "scripts/verify_lossless.py", "lossless"),
    (ROOT / "scripts/validate_gpt56.py", "GPT-5.6"),
]:
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        errors.append(f"{label} validation failed:\n" + result.stdout + result.stderr)

# Active hierarchy transport boundary.
active = "\n".join(
    [main, orchestrator]
    + [(ROOT / item["skillFile"]).read_text(encoding="utf-8") for item in skills]
)
if "Remote GitHub operations use the GitHub connector" not in active:
    errors.append("connector-only GitHub boundary missing")
if re.search(
    r"(?m)^\s*(git\s+(clone|fetch|pull|push|ls-remote)|gh\s+(api|repo|pr|issue|run|workflow|release|search))\b",
    active,
):
    errors.append("remote git or gh command found in active hierarchy")

# Exact inventory from control files, registry, and source manifests.
expected_inventory = {
    "README.md",
    "SKILL.md",
    "orchestrator/SKILL.md",
    "orchestrator/registry.json",
    "orchestrator/delegation-envelope.schema.json",
    "scripts/build_chatgpt_flat.py",
    "scripts/build_compiled.py",
    "scripts/validate.py",
    "scripts/validate_gpt56.py",
    "scripts/verify_lossless.py",
    "shared/catalogs/github-read-verbatim.md",
    "shared/catalogs/github-write-verbatim.md",
    "shared/contracts/authorization-envelope.schema.json",
    "shared/contracts/connector-contracts.md",
    "shared/core/identity.md",
    "shared/core/project-authority-and-roles.md",
    "shared/core/states-and-approval.md",
    "shared/evals/gpt-5.6-sol.json",
    "shared/evals/parallel-execution.json",
    "shared/manifests/routes.json",
    "shared/manifests/source-index.json",
    "shared/models/gpt-5.6-sol.json",
    "shared/policies/connector-native-integrity.md",
    "shared/policies/github-write-safety.md",
    "shared/policies/gpt-5.6-sol.md",
    "shared/policies/network-and-transport.md",
    "shared/policies/repository-context-and-authorization.md",
    "shared/profiles/electron.json",
    "shared/profiles/generic.json",
    "shared/profiles/node.json",
    "shared/profiles/rust.json",
    "shared/profiles/typescript.json",
    "shared/references/gpt-5.6-sol-prompting-guidance.md",
    "shared/references/parallel-execution-policy-verbatim.md",
    "shared/templates/gpt-5.6-prompt-contract.md",
    "shared/templates/prompts.md",
}
expected_inventory.update(item["skillFile"] for item in skills)

source_index = load_json(SHARED / "manifests/source-index.json")
for item in source_index.get("sources", []):
    manifest_path = "shared/" + item["path"]
    expected_inventory.add(manifest_path)
    manifest = load_json(ROOT / manifest_path)
    if manifest.get("path"):
        expected_inventory.add("shared/" + manifest["path"])

actual_inventory = {
    path.relative_to(ROOT).as_posix()
    for path in ROOT.rglob("*")
    if path.is_file()
    and path != INTEGRITY_PATH
    and "dist" not in path.parts
    and "__pycache__" not in path.parts
    and ".git" not in path.parts
}
if actual_inventory != expected_inventory:
    missing = sorted(expected_inventory - actual_inventory)
    extra = sorted(actual_inventory - expected_inventory)
    if missing:
        errors.append("inventory missing: " + ", ".join(missing))
    if extra:
        errors.append("inventory extra: " + ", ".join(extra))

integrity = load_json(INTEGRITY_PATH)
inventory_text = "\n".join(sorted(expected_inventory)) + "\n"
if integrity.get("inventory", {}).get("count") != len(expected_inventory):
    errors.append("integrity inventory count mismatch")
if integrity.get("inventory", {}).get("sha256") != hashlib.sha256(inventory_text.encode()).hexdigest():
    errors.append("integrity inventory hash mismatch")
if integrity.get("individualSkillCount") != 15:
    errors.append("integrity skill count mismatch")
if integrity.get("crossCuttingSkillCount") != 1:
    errors.append("integrity cross-cutting count mismatch")
parallel_integrity = integrity.get("parallelExecution", {})
if parallel_integrity.get("referenceSha256") != PARALLEL_REFERENCE_SHA256:
    errors.append("integrity parallel reference hash mismatch")
if not parallel_integrity.get("autoAttachWhenApplicable"):
    errors.append("integrity parallel auto-attach mismatch")

for item in integrity.get("protectedFiles", []):
    path = ROOT / item["path"]
    require(path)
    if path.is_file():
        if sha256(path) != item["sha256"] or len(path.read_bytes()) != item["bytes"]:
            errors.append("protected file mismatch " + item["path"])

# Build determinism and flat-project limit.
with tempfile.TemporaryDirectory() as temp_dir:
    first = Path(temp_dir) / "a.md"
    second = Path(temp_dir) / "b.md"
    for output in [first, second]:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build_compiled.py"), "--output", str(output)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode:
            errors.append("compiled build failed: " + result.stdout + result.stderr)
    if first.exists() and second.exists() and first.read_bytes() != second.read_bytes():
        errors.append("compiled build is not deterministic")

    flat = Path(temp_dir) / "flat"
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
print("main: root SKILL.md")
print("orchestrators: 1")
print("individual_skills:", len(ids))
print("cross_cutting_skills: 1")
print("parallel_execution: auto-attach-when-applicable")
print("parallel_policy_reference: verbatim")
print("readmes: 1")
print("canonical_sources: 15 lossless")
print("github_read_entries: 56")
print("github_write_entries: 41")
print("github_remote: connector-only")
print("github_workflows: absent")
