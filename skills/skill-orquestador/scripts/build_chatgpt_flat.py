#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist/chatgpt-project-flat"
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
manifest = json.loads((ROOT / "manifests/modules.json").read_text(encoding="utf-8"))
files = ["SKILL.md"] + manifest["always"]
for group in manifest["routes"].values():
    files.extend(group)
unique = []
for item in files:
    if item not in unique:
        unique.append(item)
for i, relative in enumerate(unique):
    src = ROOT / relative
    name = f"ORQ-{i:02d}-{relative.replace('/', '--')}"
    shutil.copy2(src, OUT / name)
print(OUT)
