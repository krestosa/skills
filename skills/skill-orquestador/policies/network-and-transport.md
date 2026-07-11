# Network and transport policy

## Absolute GitHub rule

Every operation that reads or changes remote GitHub state must use the GitHub connector. This applies to repository metadata, refs, commits, files, branches, issues, pull requests, reviews, CI, artifacts, releases when supported, and all remote writes.

Do not use `git`, `gh`, `curl`, `wget`, PowerShell, package managers, or raw HTTP from the local runtime as a GitHub transport. Do not probe GitHub first. Go directly to the connector.

## Local Git allowance

Local `git` is permitted for working-tree and object-database operations that do not contact a remote: status, diff, add, restore, local branches, local commits, log, show, rev-parse, cat-file, hash-object, write-tree, commit-tree, apply, and diff checks.

A local commit is not automatically the same object as a connector-created remote commit. Report both identities separately.

## Non-GitHub external links

Prefer a managed web tool or a dedicated connector. When a direct local-network probe is genuinely useful, perform at most one short, non-destructive attempt per hostname. On DNS failure, timeout, TLS/proxy failure, or network-unreachable status, open `LOCAL_NETWORK_CIRCUIT_OPEN` and switch immediately to the fastest managed or offline alternative. Do not cycle through equivalent commands.

## Missing connector capability

When GitHub requires an operation that is not exposed by the active connector, stop with:

```text
BLOCKED — CONNECTOR_CAPABILITY_UNAVAILABLE
requested_operation:
missing_connector_action:
local_network_fallback: PROHIBITED
```

## Precedence

This policy overrides any example or inherited instruction that proposes remote `git`, remote `gh`, or connector-as-fallback behavior.
