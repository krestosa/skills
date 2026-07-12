# Network and transport policy

## Transport boundary

Remote GitHub operations executed autonomously by an agent use the GitHub connector. This includes repository metadata, refs, commits, files, branches, issues, pull requests, reviews, CI, artifacts, releases, and agent-initiated remote writes.

A user may explicitly invoke repository-local tooling that uses native Git for publication. That exception is limited to these commands:

```text
python scripts/tooling.py publish
python scripts/tooling.py commit --push ...
```

Only controlled `git fetch`, `git ls-remote`, and one non-forced `git push` of the selected branch are permitted inside that explicit workflow. The tooling must resolve and verify the GitHub remote, discover the remote default branch dynamically, reject default-branch publication, reject divergent remote branches, verify exact one-commit ancestry, sanitize diagnostics, and verify the resulting remote ref.

## Offline commands

These commands must not contact a remote:

```text
validate
build
check
refresh-integrity
suggest-commit
commit without --push
```

No validation, build, check, metadata refresh, suggestion, or ordinary commit may perform an implicit fetch, `ls-remote`, or push.

## Prohibited native Git behavior

The local publication exception does not authorize:

```text
force push
force-with-lease
mirror push
--all
--tags
default-branch push
branch deletion
tag publication
remote merge or rebase
credential or global Git configuration changes
embedded tokens or secrets
multiple-branch publication
```

Remote `gh`, raw HTTP, `curl`, `wget`, PowerShell web requests, and package-manager transport are not part of the local publication workflow.

## Local Git allowance

Local `git` remains permitted for working-tree and object-database operations: status, diff, add, restore, local branches, local commits, log, show, rev-parse, cat-file, hash-object, write-tree, commit-tree, apply, and diff checks.

A local commit is not automatically the same object as a connector-created remote commit. Report both identities separately whenever both exist.

## Failure handling

Network access occurs only after an explicit `publish` or `commit --push`. Classify failures without exposing credentials:

```text
LOCAL_GIT_AUTH_UNAVAILABLE
NETWORK_UNAVAILABLE
REMOTE_IDENTITY_MISMATCH
DEFAULT_BRANCH_PROTECTED
REMOTE_BASE_CHANGED
REMOTE_BRANCH_DIVERGED
REMOTE_PUSH_FAILED
```

Do not retry through connector inline blobs, Contents API, force updates, temporary remote branches, or per-file commits when native publication fails.

## Non-GitHub external links

Prefer a managed web tool or dedicated connector. For an explicitly authorized direct local-network probe, perform one short, non-destructive attempt per hostname. On DNS failure, timeout, TLS or proxy failure, or network-unreachable status, stop equivalent retries and switch to an offline artifact or managed alternative.

## Precedence

This policy overrides examples that either prohibit the explicit local publication workflow or broaden it beyond the narrow `publish` and `commit --push` boundary defined above.
