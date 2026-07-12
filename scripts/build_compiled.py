#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "shared"
REGISTRY = json.loads((ROOT / "orchestrator/registry.json").read_text(encoding="utf-8"))
ROUTES = json.loads((SHARED / "manifests/routes.json").read_text(encoding="utf-8"))
INDEX = json.loads((SHARED / "manifests/source-index.json").read_text(encoding="utf-8"))

sections: dict[str, bytes] = {}
for item in INDEX["sources"]:
    manifest = json.loads((SHARED / item["path"]).read_text(encoding="utf-8"))
    data = (SHARED / manifest["path"]).read_bytes()
    for section in manifest["sections"]:
        sections[section["id"]] = data[section["startByte"]:section["endByte"]]


def expand(route_name: str, seen: set[str] | None = None) -> tuple[list[str], list[str]]:
    seen = seen or set()
    if route_name in seen:
        return [], []
    seen.add(route_name)
    route = ROUTES["routes"][route_name]
    section_ids: list[str] = []
    files: list[str] = []
    for extended in route.get("extends", []):
        nested_sections, nested_files = expand(extended, seen)
        section_ids += nested_sections
        files += nested_files
    section_ids += route.get("sections", [])
    files += route.get("files", [])
    return list(dict.fromkeys(section_ids)), list(dict.fromkeys(files))


registered = {item["id"]: item for item in REGISTRY["skills"]}
default_ids = [item["id"] for item in REGISTRY["skills"]]

parser = argparse.ArgumentParser()
parser.add_argument("--skills", nargs="*", default=default_ids)
parser.add_argument("--without-parallel", action="store_true")
parser.add_argument("--without-local-git", action="store_true")
parser.add_argument("--without-chat-recovery", action="store_true")
parser.add_argument("--output", default=str(ROOT / "dist/skills.compiled.md"))
args = parser.parse_args()

selected = list(dict.fromkeys(args.skills))
for cross_cutting, disabled in [
    ("parallel-execution", args.without_parallel),
    ("local-git-workspace", args.without_local_git),
    ("chat-recovery", args.without_chat_recovery),
]:
    if disabled:
        selected = [skill_id for skill_id in selected if skill_id != cross_cutting]
    elif cross_cutting not in selected:
        selected.append(cross_cutting)

unknown = [skill_id for skill_id in selected if skill_id not in registered]
if unknown:
    raise SystemExit("unknown skills: " + ", ".join(unknown))

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

    emitted_files: set[str] = set()
    emitted_sections: set[str] = set()
    for skill_id in selected:
        item = registered[skill_id]
        handle.write((ROOT / item["skillFile"]).read_bytes() + b"\n\n")
        for reference in item.get("referenceFiles", []):
            if reference not in emitted_files:
                handle.write((ROOT / reference).read_bytes() + b"\n\n")
                emitted_files.add(reference)
        for route_name in item.get("requiredRoutes", []):
            section_ids, files = expand(route_name)
            for file_name in files:
                if file_name not in emitted_files:
                    handle.write((SHARED / file_name).read_bytes() + b"\n\n")
                    emitted_files.add(file_name)
            for section_id in section_ids:
                if section_id not in emitted_sections:
                    handle.write(sections[section_id] + b"\n\n")
                    emitted_sections.add(section_id)

print(out)
print("skills:", ", ".join(selected))
