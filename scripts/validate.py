#!/usr/bin/env python3
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from pathlib import Path

from repository_tooling import ToolingError, load_repository_model, validate_inventory, verify_integrity


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate repository structure and generated integrity metadata.")
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()
    try:
        model = load_repository_model(args.root)
        validate_inventory(model)
        verify_integrity(model)
    except ToolingError as exc:
        print("VALIDATION: FAIL")
        print(exc.issue.render())
        return 1
    print("VALIDATION: PASS")
    print("individual_skills:", len(model.skill_order))
    print("cross_cutting_skills:", len(model.cross_cutting_ids))
    print("canonical_sources:", len(model.canonical_sources), "lossless")
    print("github_remote: connector-for-agents; explicit-local-publish-native-git")
    print("github_workflows: absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
