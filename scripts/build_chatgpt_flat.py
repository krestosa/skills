#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "shared"
REGISTRY = ROOT / "orchestrator" / "registry.json"

parser = argparse.ArgumentParser()
parser.add_argument("--output", default=str(ROOT / "dist/chatgpt-project-flat"))
args = parser.parse_args()
out = Path(args.output)

if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)

registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
registered = {item["id"]: item for item in registry["skills"]}
cross_cutting_ids = set(registry["selectionPolicy"]["crossCuttingSkillIds"])
ordered_domain_ids = [item["id"] for item in registry["skills"] if item["id"] not in cross_cutting_ids]
ordered_cross_cutting_ids = [item["id"] for item in registry["skills"] if item["id"] in cross_cutting_ids]

shutil.copy2(ROOT / "SKILL.md", out / "00-MAIN.md")
shutil.copy2(ROOT / "orchestrator/SKILL.md", out / "01-ORCHESTRATOR.md")


def bundle(target: Path, paths: list[Path]) -> None:
    with target.open("wb") as handle:
        for path in paths:
            handle.write(path.read_bytes() + b"\n\n")


position = 2
for skill_id in ordered_domain_ids:
    item = registered[skill_id]
    shutil.copy2(ROOT / item["skillFile"], out / f"{position:02d}-SKILL-{skill_id.upper()}.md")
    position += 1

bundle(
    out / f"{position:02d}-SKILLS-CROSS-CUTTING.md",
    [ROOT / registered[skill_id]["skillFile"] for skill_id in ordered_cross_cutting_ids],
)
position += 1

bundle(
    out / f"{position:02d}-SHARED-POLICIES.md",
    [
        SHARED / "policies/gpt-5.6-sol.md",
        SHARED / "policies/repository-context-and-authorization.md",
        SHARED / "policies/network-and-transport.md",
        SHARED / "policies/github-write-safety.md",
        SHARED / "policies/connector-native-integrity.md",
    ],
)
position += 1
shutil.copy2(SHARED / "catalogs/github-read-verbatim.md", out / f"{position:02d}-GITHUB-READ-VERBATIM.md")
position += 1
shutil.copy2(SHARED / "catalogs/github-write-verbatim.md", out / f"{position:02d}-GITHUB-WRITE-VERBATIM.md")
position += 1
bundle(
    out / f"{position:02d}-SHARED-CONTRACTS.md",
    [SHARED / "contracts/authorization-envelope.schema.json", SHARED / "contracts/connector-contracts.md"],
)
position += 1
bundle(
    out / f"{position:02d}-GPT56.md",
    [SHARED / "models/gpt-5.6-sol.json", SHARED / "templates/gpt-5.6-prompt-contract.md"],
)
position += 1
(out / f"{position:02d}-PROJECT-INSTRUCTIONS.txt").write_text(
    "Load 00-MAIN.md, then 01-ORCHESTRATOR.md. The orchestrator selects only the required domain skills and "
    "auto-attaches cross-cutting control when applicable. Practical reasoning preserves Ergon and Arete while adding "
    "Eudaimonia, Telos, and Phronesis. Auto-attach local-git-workspace before local Git, parallel-execution when safe "
    "parallel work exists, and chat-recovery when delegated execution is interrupted or untrusted. Remote GitHub "
    "operations use the connector; local git is local-only. Returned delegated results use one prompt-only code block.\n",
    encoding="utf-8",
)

files = list(out.iterdir())
if len(files) > 25:
    raise SystemExit(f"flat package exceeds 25 files: {len(files)}")
print(out)
print("files:", len(files))
print("domain_skills:", len(ordered_domain_ids))
print("cross_cutting_skills:", len(ordered_cross_cutting_ids))
