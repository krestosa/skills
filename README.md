# Skills

A repository-agnostic hierarchical skill system.

```text
SKILL.md                 main global directives
orchestrator/SKILL.md    the single orchestrator
skills/<name>/SKILL.md   individual skills selected on demand
shared/                  canonical sources, policies, catalogs, profiles, references, and manifests
```

## Execution model

1. Load `SKILL.md`.
2. Load `orchestrator/SKILL.md`.
3. The orchestrator selects one primary skill and only the supporting skills needed for correctness.
4. When useful independent work exists, it auto-attaches `skills/parallel-execution/SKILL.md` as a cross-cutting controller.
5. Selected skills read only their declared routes from `shared/manifests/routes.json`.
6. Canonical texts are referenced once from `shared/`; they are not duplicated inside the orchestrator or skill wrappers.

`parallel-execution` does not replace the primary skill and does not authorize side effects. It constructs the dependency and resource graph, parallelizes independent work, and serializes only real dependencies, shared-resource conflicts, tool restrictions, and ordered external effects.

## Invariants

- Exactly one main prompt and one orchestrator.
- Exactly one repository `README.md`.
- Individual skills live only under `skills/<name>/`.
- Cross-cutting skills are still individual skills and are directed by the orchestrator.
- No repository, branch, framework, product, or organization is hardcoded.
- Remote GitHub reads and writes use the GitHub connector.
- Local `git` is local-only.
- GitHub Read and Write catalogs remain verbatim.
- The user-provided parallel-execution policy remains preserved verbatim under `shared/references/`.
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
