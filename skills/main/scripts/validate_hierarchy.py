#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MAIN = ROOT / "skills" / "main"
ORCH = ROOT / "skills" / "orchestrator"
INDIVIDUAL = ROOT / "skills" / "individual"
ENGINE = ROOT / "skills" / "skill-orquestador"

errors: list[str] = []

def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid json {path.relative_to(ROOT)}: {exc}")
        return {}

def require(path: Path) -> None:
    if not path.is_file():
        errors.append(f"missing file {path.relative_to(ROOT)}")

required = [
    ROOT / "SKILL.md",
    ROOT / "README.md",
    MAIN / "SKILL.md",
    MAIN / "manifests" / "skill-graph.json",
    MAIN / "manifests" / "integrity.json",
    MAIN / "evals" / "routing.json",
    ORCH / "SKILL.md",
    ORCH / "manifests" / "registry.json",
    ORCH / "manifests" / "delegation-envelope.schema.json",
    INDIVIDUAL / "README.md",
    ENGINE / "SKILL.md",
    ENGINE / "manifests" / "modules.json",
]
for path in required:
    require(path)

graph = load_json(MAIN / "manifests" / "skill-graph.json")
registry = load_json(ORCH / "manifests" / "registry.json")
engine_routes = load_json(ENGINE / "manifests" / "modules.json").get("routes", {})

if graph.get("root") != "main":
    errors.append("graph root must be main")

nodes = graph.get("nodes", {})
if nodes.get("main", {}).get("children") != ["orchestrator"]:
    errors.append("main must have exactly one child: orchestrator")

registered = registry.get("skills", [])
ids = [item.get("id") for item in registered]
if not ids or len(ids) != len(set(ids)):
    errors.append("individual skill ids must be present and unique")

expected_children = [f"individual/{skill_id}" for skill_id in ids]
if nodes.get("orchestrator", {}).get("children") != expected_children:
    errors.append("graph children must match registry order")

for item in registered:
    skill_id = item.get("id")
    skill_path = ROOT / item.get("skillFile", "")
    require(skill_path)
    text = skill_path.read_text(encoding="utf-8", errors="ignore") if skill_path.is_file() else ""

    for heading in ["## Role", "## Personality", "## Collaboration style", "## Goal", "## Success criteria", "## Output", "## Stop rules"]:
        if heading not in text:
            errors.append(f"{skill_id} missing {heading}")

    if item.get("personality") != "embedded" or item.get("collaboration") != "embedded":
        errors.append(f"{skill_id} personality/collaboration must be embedded")

    if not item.get("loadPolicy", {}).get("onDemand"):
        errors.append(f"{skill_id} must be on-demand")

    for route in item.get("canonicalRoutes", []) + item.get("optionalRoutes", []):
        if route not in engine_routes:
            errors.append(f"{skill_id} references unknown route {route}")

    for dependency in item.get("dependencies", []):
        if dependency not in ids:
            errors.append(f"{skill_id} has unknown dependency {dependency}")

main_text = (MAIN / "SKILL.md").read_text(encoding="utf-8")
if "skills/orchestrator/SKILL.md" not in main_text:
    errors.append("main does not load orchestrator")
if re.search(r"skills/individual/[a-z0-9-]+", main_text):
    errors.append("main must not directly load an individual skill")

orchestrator_text = (ORCH / "SKILL.md").read_text(encoding="utf-8")
for marker in [
    "Do not load all individual skills preemptively.",
    "Select the smallest complete set",
    "one primary skill",
    "manifests/registry.json",
]:
    if marker not in orchestrator_text:
        errors.append(f"orchestrator missing marker: {marker}")

hierarchy_text = "\n".join([
    (ROOT / "SKILL.md").read_text(encoding="utf-8"),
    main_text,
    orchestrator_text,
])
if "Remote GitHub operations use the GitHub connector" not in hierarchy_text:
    errors.append("connector-only GitHub boundary missing")
if re.search(r"(?m)^\s*(git\s+(clone|fetch|pull|push|ls-remote)|gh\s+(api|repo|pr|issue|run|workflow|release|search))\b", hierarchy_text):
    errors.append("remote git or gh command found in active hierarchy")

needle = "krestosa/" + "Crystal"
for root in [ROOT / "SKILL.md", ROOT / "README.md", MAIN, ORCH, INDIVIDUAL]:
    candidates = [root] if root.is_file() else root.rglob("*")
    for candidate in candidates:
        if candidate.is_file() and candidate.suffix in {".md", ".json", ".py", ".txt"}:
            if needle in candidate.read_text(encoding="utf-8", errors="ignore"):
                errors.append(f"hardcoded repository in {candidate.relative_to(ROOT)}")

if (ROOT / ".github" / "workflows").exists():
    errors.append("GitHub workflows are prohibited")

integrity_path = MAIN / "manifests" / "integrity.json"
integrity = load_json(integrity_path)
expected_files = integrity.get("files", [])
actual_files = []
for tracked in [ROOT / "SKILL.md", ROOT / "README.md", MAIN, ORCH, INDIVIDUAL]:
    candidates = [tracked] if tracked.is_file() else tracked.rglob("*")
    for candidate in candidates:
        if not candidate.is_file() or candidate == integrity_path:
            continue
        data = candidate.read_bytes()
        actual_files.append({
            "path": candidate.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
        })
actual_files.sort(key=lambda item: item["path"])
if actual_files != expected_files:
    errors.append("hierarchy integrity mismatch")

engine_validator = ENGINE / "scripts" / "validate_skill.py"
if engine_validator.is_file():
    result = subprocess.run(
        [sys.executable, str(engine_validator)],
        cwd=ENGINE,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        errors.append("canonical engine validation failed:\n" + result.stdout + result.stderr)

if errors:
    print("HIERARCHY VALIDATION: FAIL")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("HIERARCHY VALIDATION: PASS")
print("root: main")
print("orchestrator: present")
print("individual_skills:", len(ids))
print("personality_embedded: yes")
print("collaboration_embedded: yes")
print("minimal_loading: enforced")
print("canonical_engine: referenced")
print("github_remote: connector-only")
print("github_workflows: absent")
