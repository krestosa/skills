#!/usr/bin/env python3
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from pathlib import Path

from repository_tooling import ToolingError, build_compiled, load_repository_model


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic compiled skill document.")
    parser.add_argument("--root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--skills", nargs="+")
    parser.add_argument("--include", action="append", default=[])
    parser.add_argument("--exclude", action="append", default=[])
    args = parser.parse_args()
    try:
        model = load_repository_model(args.root)
        output = args.output or model.root / "dist" / "skills.compiled.md"
        selected = build_compiled(model, output, skills=args.skills, include=args.include, exclude=args.exclude)
    except ToolingError as exc:
        print("COMPILED BUILD: FAIL")
        print(exc.issue.render())
        return 1
    print("COMPILED BUILD: PASS")
    print("output:", output.resolve())
    print("skills:", ", ".join(selected))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
