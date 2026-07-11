# Skills

A repository-agnostic hierarchical skill system.

```text
SKILL.md                 main global directives
orchestrator/SKILL.md    the single orchestrator
skills/<name>/SKILL.md   individual skills selected on demand
shared/                  canonical sources, policies, catalogs, profiles, and manifests
```

## Execution model

1. Load `SKILL.md`.
2. Load `orchestrator/SKILL.md`.
3. The orchestrator selects one primary skill and only the supporting skills needed for correctness.
4. Selected skills read their declared routes from `shared/manifests/routes.json`.
5. Canonical texts are referenced once from `shared/sources/`; they are not copied into the orchestrator or skill wrappers.

## Invariants

- Exactly one main prompt and one orchestrator.
- Exactly one repository `README.md`.
- Individual skills live only under `skills/<name>/`.
- No repository, branch, framework, product, or organization is hardcoded.
- Remote GitHub reads and writes use the GitHub connector.
- Local `git` is local-only.
- GitHub Read and Write catalogs remain verbatim.
- No GitHub workflows are included.

## Validate

```bash
python scripts/validate.py
```

## Build

```bash
python scripts/build_compiled.py
python scripts/build_chatgpt_flat.py
```
