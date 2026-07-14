#!/usr/bin/env python3
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from pathlib import Path

from repository_tooling import ToolingError, load_repository_model


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify canonical sources byte-for-byte.")
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()
    try:
        model = load_repository_model(args.root, verify_sources=True)
    except ToolingError as exc:
        print("LOSSLESS: FAIL")
        print(exc.issue.render())
        return 1
    print("LOSSLESS: PASS")
    print("sources:", len(model.canonical_sources))
    print("text_mutations: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
