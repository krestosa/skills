#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
required = [
    "SKILL.md",
    "policies/repository-context-and-authorization.md",
    "policies/network-and-transport.md",
    "policies/github-write-safety.md",
    "catalogs/github-read-verbatim.md",
    "catalogs/github-write-verbatim.md",
    "manifests/modules.json",
    "contracts/authorization-envelope.schema.json",
]
for rel in required:
    if not (ROOT / rel).is_file():
        errors.append(f"missing: {rel}")

source_files = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in {".md", ".json"} and "catalogs" not in p.parts]
all_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in source_files)
if re.search(r"(?m)^\s*repository_full_name\s*[:=]\s*(?!\{\{)[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\s*$", all_text):
    errors.append("hardcoded repository_full_name value")
if "{{repository_full_name}}" not in all_text or "{{default_branch}}" not in all_text:
    errors.append("runtime repository placeholders are missing")

if (ROOT.parents[1] / ".github/workflows").exists():
    errors.append("GitHub workflows directory is prohibited in this repository")

BEGIN = "<!-- VERBATIM_CATALOG_BEGIN -->\n"
END = "\n<!-- VERBATIM_CATALOG_END -->"
expected = {
    "catalogs/github-read-verbatim.md": (56, "610c387f5f7c9047c65fef08734d5199696230866ca79e270700209eaab1324e"),
    "catalogs/github-write-verbatim.md": (41, "499373638143f48b0549701bf5036725a2c2bc9b332a95d9a053a1e1ce687a3d"),
}
for rel, (count, digest) in expected.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        errors.append(f"catalog markers missing: {rel}")
        continue
    payload = text.split(BEGIN, 1)[1].split(END, 1)[0].encode("utf-8")
    actual_count = len([p for p in payload.decode().split("\n\n") if p.strip()])
    actual_digest = hashlib.sha256(payload).hexdigest()
    if actual_count != count:
        errors.append(f"catalog count {rel}: {actual_count} != {count}")
    if actual_digest != digest:
        errors.append(f"catalog sha {rel}: {actual_digest} != {digest}")

manifest = json.loads((ROOT / "manifests/modules.json").read_text(encoding="utf-8"))
for rel in manifest["always"]:
    if not (ROOT / rel).is_file():
        errors.append(f"manifest target missing: {rel}")
for route, files in manifest["routes"].items():
    for rel in files:
        if not (ROOT / rel).is_file():
            errors.append(f"route {route} target missing: {rel}")

# Remote GitHub commands must not be executable instructions outside the transport policy and catalogs.
remote_cmd = re.compile(r"(?m)^\s*(git\s+(clone|fetch|pull|push|ls-remote)|gh\s+(api|repo|pr|issue|run|workflow|release|search))\b")
for path in ROOT.rglob("*.md"):
    rel = path.relative_to(ROOT).as_posix()
    if rel in {"policies/network-and-transport.md", "catalogs/github-read-verbatim.md", "catalogs/github-write-verbatim.md"}:
        continue
    for match in remote_cmd.finditer(path.read_text(encoding="utf-8")):
        errors.append(f"remote command instruction in {rel}: {match.group(0).strip()}")

if errors:
    print("VALIDATION: FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)
print("VALIDATION: PASS")
print("github_read_entries: 56")
print("github_write_entries: 41")
print("repository_hardcoding: none")
print("github_workflows: absent")
