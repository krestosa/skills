#!/usr/bin/env python3
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from pathlib import Path

from repository_tooling import ToolingError, load_repository_model, validate_model_descriptor


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the registered model descriptor and linked resources.")
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()
    try:
        result = validate_model_descriptor(load_repository_model(args.root))
    except ToolingError as exc:
        print("MODEL VALIDATION: FAIL")
        print(exc.issue.render())
        return 1
    print("MODEL VALIDATION: PASS")
    print("model_profile:", result["model"])
    print("resources:", result["resources"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
