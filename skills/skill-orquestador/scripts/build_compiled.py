#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "manifests/modules.json").read_text(encoding="utf-8"))
order = ["SKILL.md"] + manifest["always"]
seen = set(order)
for files in manifest["routes"].values():
    for file in files:
        if file not in seen:
            seen.add(file)
            order.append(file)

parts = []
for relative in order:
    path = ROOT / relative
    parts.append(f"\n\n<!-- MODULE: {relative} -->\n\n")
    parts.append(path.read_text(encoding="utf-8"))

out = ROOT / "dist/skill-orquestador.compiled.md"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("".join(parts).lstrip(), encoding="utf-8", newline="\n")
print(out)
