# Skills

A repository-agnostic hierarchical skill system.

```text
SKILL.md                 main global directives
orchestrator/SKILL.md    the single orchestrator
skills/<name>/SKILL.md   individual and cross-cutting skills selected on demand
shared/                  canonical sources, policies, catalogs, profiles, and manifests
```

## Execution model

1. Load `SKILL.md`.
2. Load `orchestrator/SKILL.md`.
3. The orchestrator selects one primary skill and only the supporting skills needed for correctness.
4. Cross-cutting skills attach automatically when applicable:
   - `parallel-execution` for safe concurrent work;
   - `local-git-workspace` before local Git;
   - `chat-recovery` when a delegated chat stalls, is stopped, disconnects, truncates its response, or leaves uncertain execution state.
5. Selected skills read their declared routes from `shared/manifests/routes.json`.
6. Canonical texts are referenced once from `shared/sources/`; they are not copied into the orchestrator or skill wrappers.

## Interrupted-chat recovery

Before a resumed chat generates or changes files, `chat-recovery` requires a recursive inventory of every file and directory inside the active workspace. Existing tracked, untracked, ignored, hidden, generated, temporary, binary, backup, patch, manifest, lock, and output files are inspected and reused when valid. Missing output from the interrupted chat is not treated as proof that work was not written to disk.

The recovery prompt must be idempotent: preserve verified work, prohibit unnecessary regeneration or rewriting, validate current bases, and continue only unresolved work from the last reliable checkpoint.

## Invariants

- Exactly one main prompt and one orchestrator.
- Exactly one repository `README.md`.
- Individual and cross-cutting skills live only under `skills/<name>/`.
- No repository, branch, framework, product, or organization is hardcoded.
- Remote GitHub reads and writes use the GitHub connector.
- Local `git` is local-only and runs after ownership preflight.
- GitHub Read and Write catalogs remain verbatim.
- No GitHub workflows are included.
- Returned or interrupted delegated work produces one prompt-only code block with no external commentary.

## Validate

```bash
python scripts/validate.py
```

## Build

```bash
python scripts/build_compiled.py
python scripts/build_chatgpt_flat.py
```
