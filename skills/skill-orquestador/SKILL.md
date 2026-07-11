---
name: skill-orquestador
description: Senior software delivery orchestration for arbitrary repositories. Resolves repository context dynamically, uses local tools for local work, and uses the GitHub connector for every remote GitHub operation.
---

# skill-orquestador

This is the entrypoint. It contains no built-in repository or product.

## Mandatory load order

Always load:

1. `policies/repository-context-and-authorization.md`
2. `policies/network-and-transport.md`
3. `core/identity.md`
4. `core/project-authority-and-roles.md`
5. `core/states-and-approval.md`

Then load the route-specific modules from `manifests/modules.json`.

For every GitHub task also load the exact connector catalogs. For every remote write also load `policies/github-write-safety.md`.

## Non-negotiable transport boundary

Remote GitHub reads and writes use the GitHub connector from the start. Local `git` is limited to local working-tree, local branch, local object, commit, diff, and validation operations. Remote `git` and remote `gh` are prohibited.

## Repository variables

Resolve `{{repository_full_name}}`, `{{default_branch}}`, `{{base_sha}}`, and `{{branch}}` per task. Never fall back to a repository remembered from another task.

## Routes

- analysis/planning: research, architecture, security
- implementation: baseline, implementation, runtime, validation
- GitHub Read: connector playbook + Read catalog
- GitHub Write/publication: connector playbook + both catalogs + write safety + connector-native integrity
- CI: publication/CI playbook + connector playbook + Read catalog
- PR/review/merge: PR/review playbook + connector playbook + both catalogs
- recovery: recovery, workspace, connector, and integrity modules
- delegation/management: management, workspace, automation modules

## Conflict precedence

```text
current user instruction and authorization
→ repository context policy
→ network and transport policy
→ GitHub write safety
→ this router
→ route-specific module
→ template or example
```
