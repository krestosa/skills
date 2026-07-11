#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "shared"
REGISTRY = json.loads((ROOT / "orchestrator/registry.json").read_text(encoding="utf-8"))
ROUTES = json.loads((SHARED / "manifests/routes.json").read_text(encoding="utf-8"))
SOURCE_INDEX = json.loads((SHARED / "manifests/source-index.json").read_text(encoding="utf-8"))

sections: dict[str, bytes] = {}
for item in SOURCE_INDEX["sources"]:
    manifest = json.loads((SHARED / item["path"]).read_text(encoding="utf-8"))
    source = (SHARED / manifest["path"]).read_bytes()
    for section in manifest["sections"]:
        sections[section["id"]] = source[section["startByte"]:section["endByte"]]

def expand(route_name: str, seen: set[str] | None = None) -> tuple[list[str], list[str]]:
    seen = seen or set()
    if route_name in seen:
        return [], []
    seen.add(route_name)
    route = ROUTES["routes"][route_name]
    section_ids: list[str] = []
    files: list[str] = []
    for parent in route.get("extends", []):
        inherited_sections, inherited_files = expand(parent, seen)
        section_ids += inherited_sections
        files += inherited_files
    section_ids += route.get("sections", [])
    files += route.get("files", [])
    return list(dict.fromkeys(section_ids)), list(dict.fromkeys(files))

parser = argparse.ArgumentParser()
parser.add_argument("--skills", nargs="*")
parser.add_argument("--without-parallel", action="store_true")
parser.add_argument("--output", default=str(ROOT / "dist/skills.compiled.md"))
args = parser.parse_args()

skill_ids = args.skills or [item["id"] for item in REGISTRY["skills"]]
if not args.without_parallel and "parallel-execution" not in skill_ids:
    skill_ids.append("parallel-execution")

out = Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)

with out.open("wb") as handle:
    for path in [
        ROOT / "SKILL.md",
        ROOT / "orchestrator/SKILL.md",
        SHARED / "policies/gpt-5.6-sol.md",
        SHARED / "policies/repository-context-and-authorization.md",
        SHARED / "policies/network-and-transport.md",
    ]:
        handle.write(path.read_bytes() + b"\n\n")

    for skill_id in skill_ids:
        item = next(entry for entry in REGISTRY["skills"] if entry["id"] == skill_id)
        handle.write((ROOT / item["skillFile"]).read_bytes() + b"\n\n")
        for route_name in item.get("requiredRoutes", []):
            section_ids, files = expand(route_name)
            for file in files:
                handle.write((SHARED / file).read_bytes() + b"\n\n")
            for section_id in section_ids:
                handle.write(sections[section_id] + b"\n\n")

print(out)
