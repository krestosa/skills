#!/usr/bin/env python3
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from pathlib import Path

from repository_tooling import ToolingError, build_flat, load_repository_model


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the deterministic flat ChatGPT package.")
    parser.add_argument("--root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        model = load_repository_model(args.root)
        output = args.output or model.root / "dist" / "chatgpt-project-flat"
        hashes = build_flat(model, output)
    except ToolingError as exc:
        print("FLAT BUILD: FAIL")
        print(exc.issue.render())
        return 1
    print("FLAT BUILD: PASS")
    print("output:", output.resolve())
    print("files:", len(hashes))
    print("domain_skills:", len(model.skill_order) - len(model.cross_cutting_ids))
    print("cross_cutting_skills:", len(model.cross_cutting_ids))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
