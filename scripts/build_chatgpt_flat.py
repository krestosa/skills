#!/usr/bin/env python3
from __future__ import annotations
import argparse, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "shared"

parser = argparse.ArgumentParser()
parser.add_argument("--output", default=str(ROOT / "dist/chatgpt-project-flat"))
args = parser.parse_args()
out = Path(args.output)

if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)

shutil.copy2(ROOT / "SKILL.md", out / "00-MAIN.md")
shutil.copy2(ROOT / "orchestrator/SKILL.md", out / "01-ORCHESTRATOR.md")

next_index = 2
for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
    shutil.copy2(path, out / f"{next_index:02d}-SKILL-{path.parent.name.upper()}.md")
    next_index += 1

def bundle(target: Path, paths: list[Path]) -> None:
    with target.open("wb") as handle:
        for path in paths:
            handle.write(path.read_bytes() + b"\n\n")

bundle(
    out / f"{next_index:02d}-SHARED-POLICIES.md",
    [
        SHARED / "policies/gpt-5.6-sol.md",
        SHARED / "policies/repository-context-and-authorization.md",
        SHARED / "policies/network-and-transport.md",
        SHARED / "policies/github-write-safety.md",
        SHARED / "policies/connector-native-integrity.md",
    ],
)
next_index += 1

shutil.copy2(
    SHARED / "catalogs/github-read-verbatim.md",
    out / f"{next_index:02d}-GITHUB-READ-VERBATIM.md",
)
next_index += 1
shutil.copy2(
    SHARED / "catalogs/github-write-verbatim.md",
    out / f"{next_index:02d}-GITHUB-WRITE-VERBATIM.md",
)
next_index += 1

bundle(
    out / f"{next_index:02d}-SHARED-CONTRACTS.md",
    [
        SHARED / "contracts/authorization-envelope.schema.json",
        SHARED / "contracts/connector-contracts.md",
    ],
)
next_index += 1

bundle(
    out / f"{next_index:02d}-GPT56.md",
    [
        SHARED / "models/gpt-5.6-sol.json",
        SHARED / "templates/gpt-5.6-prompt-contract.md",
    ],
)
next_index += 1

(out / f"{next_index:02d}-PROJECT-INSTRUCTIONS.txt").write_text(
    "Load 00-MAIN.md, then 01-ORCHESTRATOR.md. "
    "The orchestrator selects only the required individual skill files and auto-attaches "
    "PARALLEL-EXECUTION when safe independent work exists. "
    "Remote GitHub operations use the connector; local git is local-only.\n",
    encoding="utf-8",
)

files = list(out.iterdir())
if len(files) > 25:
    raise SystemExit("flat package exceeds 25 files")

print(out)
print("files:", len(files))
