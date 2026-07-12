# Skills

A repository-agnostic hierarchical skill system.

```text
SKILL.md                 main global directives
orchestrator/SKILL.md    the single orchestrator
skills/<name>/SKILL.md   domain and cross-cutting skills selected on demand
shared/                  canonical sources, policies, catalogs, profiles, and manifests
```

## Execution model

1. Load `SKILL.md`.
2. Load `orchestrator/SKILL.md`.
3. Resolve the user-centered human good and concrete end purpose.
4. The orchestrator selects one primary domain skill and the minimum supporting skills required for correctness.
5. Cross-cutting utilities attach automatically when their conditions apply.
6. Selected skills read only their declared routes from `shared/manifests/routes.json`.
7. Autonomous remote GitHub operations use the GitHub connector. Explicit user-invoked `publish` or `commit --push` may use guarded native Git transport.

## Model and reasoning routing

The ChatGPT Web chat acting as the orchestrator is configured by the user with the latest available model and `High` reasoning. The system cannot change the visual model or reasoning selectors itself.

For every prompt generated for another chat, the orchestrator keeps the latest available model as an internal policy and independently selects one visible reasoning level:

```text
Instant
Medium
High
```

The level is recalculated for every new prompt, continuation, correction, validation, recovery, publication, derived action, independent workstream, or material change in evidence. It is not inherited from the previous iteration and the user is not asked to choose it.

The classifier summarizes seven factors: Telos clarity, Ergon complexity, Phronesis adaptation burden, Arete validation burden, risk and reversibility, state uncertainty, and how completely the prompt closes the remaining decisions.

- `Instant` is reserved for closed, mechanical, linear, known-state, low-risk work with exact validation and no strategic choice.
- `Medium` is the default result for bounded professional work with several dependent steps, limited local decisions, known validation, and no critical trigger.
- `High` is required for architecture, cross-system work, complex migration or compatibility, unknown or interrupted state, contradictory evidence, multi-cause debugging, security or permissions, destructive action, critical release or production work, global policy or orchestrator changes, dynamic replanning, extensive validation, high risk of lost work, or an open objective.

A prompt that genuinely removes ambiguity, strategy choice, branching, undefined fallbacks, implicit success criteria, and reinterpretation may reduce the initial result by one level only: `High → Medium` or `Medium → Instant`. Hard triggers prevent a downgrade. This closes prompts before spending more reasoning and optimizes total user time, latency, quota, and corrective work.

Generated-prompt delivery uses this exact visible structure:

```text
[Prompt generado]
```
Razonamiento: Medium

The reasoning line is outside the prompt block, immediately follows it, contains no model recommendation or explanation, and is the final element of that prompt delivery. Multiple workstreams repeat the same pair independently. Direct answers that do not generate prompts do not require the line.

## How to request a skill

You may use the exact ID or describe the capability in natural language. The orchestrator remains responsible for validating the selection, resolving dependencies, and adding supporting utilities.

```text
Use the interrupted-chat recovery skill to resume the coding chat
that stalled and continue from the last verified checkpoint.
```

The operational source of truth is `orchestrator/registry.json`. This README is the human-readable catalog.

The recovery identifiers remain stable for compatibility, but their visible names are now distinct:

```text
Technical State Recovery      → recovery
Interrupted Chat Recovery     → chat-recovery
```

## Skill catalog

### Analysis and architecture

| Skill | ID | What it does | Example request | Activation |
|---|---|---|---|---|
| Repository Analysis | `repository-analysis` | Audits repository state, boundaries, dependencies, risks, and implementation implications. | `Use repository-analysis to audit the project before proposing changes.` | Explicit or selected for repository-level analysis. |
| Architecture | `architecture` | Reviews or designs modules, interfaces, runtime boundaries, security implications, and architectural tradeoffs. | `Use architecture to review these module boundaries.` | Explicit or selected for structural decisions. |

### Implementation and visual experience

| Skill | ID | What it does | Example request | Activation |
|---|---|---|---|---|
| Implementation | `implementation` | Performs authorized code, configuration, integration, repair, and refactoring work. | `Use implementation to apply the approved change without expanding scope.` | Explicit or selected when implementation is authorized. |
| Frontend Visual | `frontend-visual` | Implements and validates UI structure, visual fidelity, responsive behavior, accessibility, and browser interaction. | `Use frontend-visual to reproduce this interface and validate the result.` | Explicit or selected for frontend and visual work. |

### Validation, quality, and diagnostics

| Skill | ID | What it does | Example request | Activation |
|---|---|---|---|---|
| Validation Quality | `validation-quality` | Defines and executes proportionate tests, builds, lint, type checks, compatibility checks, and completion verification. | `Use validation-quality to verify every implementation claim.` | Explicit, supporting, or required by release work. |
| CI Diagnostics | `ci-diagnostics` | Inspects CI checks and logs, classifies failures, and determines the smallest corrective action. | `Use ci-diagnostics to determine why the checks are failing.` | Explicit or selected when CI evidence is material. |

### GitHub, review, publication, and release

| Skill | ID | What it does | Example request | Activation |
|---|---|---|---|---|
| GitHub Read | `github-read` | Reads repositories, files, commits, refs, PRs, issues, reviews, and CI evidence through the connector. | `Use github-read to verify the current remote branch and commit.` | Explicit or attached as a remote-read dependency. |
| GitHub Write | `github-write` | Performs specifically authorized GitHub mutations through the connector. | `Use github-write to publish the explicitly authorized branch.` | Only with matching remote-write authorization. |
| Pull Request Review and Merge | `pr-review-merge` | Creates, inspects, reviews, updates, and—when authorized—merges pull requests. | `Use pr-review-merge to prepare a draft PR and verify its checks.` | Explicit or selected for PR lifecycle work. |
| Release | `release` | Prepares release readiness, final validation, packaging, publication coordination, and release evidence. | `Use release to prepare this implementation for controlled publication.` | Explicit or selected when the requested outcome is a release. |

### Documentation, prompts, and orchestration

| Skill | ID | What it does | Example request | Activation |
|---|---|---|---|---|
| Documentation and Roadmap | `documentation-roadmap` | Creates or updates README content, technical documentation, operational guidance, status, and evidence-based roadmaps. | `Use documentation-roadmap to update the README from verified evidence.` | Explicit or selected for documentation work. |
| Prompt Engineering | `prompt-engineering` | Designs, migrates, refines, and validates prompts and structured instruction contracts. | `Use prompt-engineering to create a self-contained coding-chat prompt.` | Explicit or selected when the deliverable is a prompt. |
| Management Delegation | `management-delegation` | Decomposes work into bounded workstreams, preserves evidence across handoffs, and generates continuation prompts from returned results. | `Use management-delegation to split this project into coordinated chats.` | Explicit or selected for delegation and returned delegated results. |

### Recovery and continuity

| Skill | ID | What it does | Example request | Activation |
|---|---|---|---|---|
| Technical State Recovery | `recovery` | Repairs or reconciles partial, failed, stale, or inconsistent repository, workspace, branch, CI, publication, merge, connector, or local/remote state. | `Use technical-state recovery to restore the inconsistent repository and publication state.` | Explicit or selected for a technical incident. |
| Interrupted Chat Recovery | `chat-recovery` | Reconstructs a stalled, stopped, disconnected, timed-out, truncated, or untrusted delegated execution and produces an idempotent continuation prompt. | `Use interrupted-chat recovery to inspect the environment and resume from the last verified checkpoint.` | Explicit or automatically attached for interrupted delegated work. |

The distinction is operational:

```text
Technical State Recovery (`recovery`)
→ receives a technical incident and restores a verified state.

Interrupted Chat Recovery (`chat-recovery`)
→ receives an interrupted chat execution, reconstructs what happened,
  and creates the prompt needed to resume safely.
```

They may compose. Interrupted Chat Recovery determines what the stopped chat completed, left incomplete, or left unknown. Technical State Recovery repairs any repository, CI, publication, connector, or environment inconsistency found during that reconstruction.

### Cross-cutting utilities

Cross-cutting utilities govern or prepare domain work. They do not replace the primary skill and do not independently authorize side effects.

| Skill | ID | What it does | Example request | Activation |
|---|---|---|---|---|
| Practical Reasoning | `practical-reasoning` | Governs purpose, function, adaptation, quality, and user benefit through Eudaimonia, Telos, Ergon, Phronesis, and Arete. | `Use practical-reasoning to keep the work aligned with its real purpose and adapt to evidence.` | Automatically attached unless the task is trivial, exact, reversible, and mechanical. |
| Parallel Execution | `parallel-execution` | Finds independent operations, executes safe work concurrently, and serializes shared-state conflicts. | `Use parallel-execution for every independent check and serialize conflicting writes.` | Automatically attached when useful parallel work exists. |
| Local Git Workspace | `local-git-workspace` | Resolves the repository root, repairs ownership when required, and runs the mandatory preflight before local Git commands. | `Use local-git-workspace before any local Git operation.` | Automatically attached before local Git. |

`chat-recovery` is also cross-cutting internally, but it is listed under **Recovery and continuity** so every skill appears only once in this catalog.

## Quick invocation index

```text
Audit a repository                         → repository-analysis
Review system architecture                 → architecture
Implement an approved change               → implementation
Build or correct a frontend                → frontend-visual
Validate a result                          → validation-quality
Diagnose failing CI                        → ci-diagnostics
Inspect remote GitHub state                → github-read
Perform an authorized GitHub write         → github-write
Prepare, review, or merge a PR             → pr-review-merge
Prepare a release                          → release
Update documentation or roadmap            → documentation-roadmap
Create or refine a prompt                  → prompt-engineering
Coordinate multiple chats or workstreams   → management-delegation
Repair inconsistent technical state        → recovery
Resume a stalled or interrupted chat       → chat-recovery
Apply purpose and adaptive judgment        → practical-reasoning
Parallelize independent work               → parallel-execution
Prepare a repository for local Git         → local-git-workspace
```

## Practical reasoning

The system preserves its existing strengths in function and execution quality:

```text
Ergon  → what the system must do
Arete  → how well it must do it
```

The cross-cutting reasoning layer adds:

```text
Eudaimonia → the legitimate human good ultimately served
Telos      → the concrete end state and why it matters
Phronesis  → when and how to adapt under real circumstances
```

Operationally:

```text
Eudaimonia frames the user benefit.
Telos directs the work.
Ergon defines the required functions.
Phronesis adapts tactics when evidence changes.
Arete establishes and verifies the quality bar.
```

The framework is behavioral, not decorative. It prevents literal completion that misses the real purpose, rigid plans contradicted by evidence, technically excellent work that wastes or harms the user, good intentions without functional delivery, and overengineering beyond the required end.

It does not authorize paternalistic replacement of the user's goals. Explicit user values, authorization, safety, preservation, truthfulness, and prohibitions remain invariants.

## Interrupted-chat recovery

Before a resumed chat generates or changes any file, `chat-recovery` requires a system-wide inventory of every accessible filesystem entry in the execution environment. The scan starts from `/`, covers every accessible mounted filesystem, and has no date, Git, repository, workspace, owner, extension, or task-origin filter.

It inventories files inside and outside the active repository, including system files, user files, workspaces, temporary directories, caches, hidden files, generated outputs, backups, patches, manifests, locks, binaries, symlinks, build directories, and artifacts from previous runs. Kernel pseudo-filesystems and device-backed virtual trees are recorded as excluded mount types rather than traversed as persistent files.

The recovery prompt must be idempotent: preserve verified work, reuse every valid existing artifact, prohibit unnecessary generation or rewriting, validate current bases, and continue only unresolved work from the last reliable checkpoint.

## Invariants

- Exactly one main prompt and one orchestrator.
- Exactly one repository `README.md`.
- Skills live only under `skills/<name>/`.
- No repository, branch, framework, product, or organization is hardcoded.
- Autonomous remote GitHub reads and writes use the GitHub connector.
- Local `git` runs after ownership preflight; native Git network access is available only through explicit `publish` or `commit --push`.
- Publication never targets the remote default branch, never uses force, and never publishes tags or multiple branches.
- GitHub Read and Write catalogs remain verbatim.
- No GitHub workflows are included.
- Generated delegated work uses one prompt code block followed by one reasoning-only directive per prompt, with no other external commentary.
- The latest available target model remains internal and is absent from the visible directive.
- Practical reasoning never grants side effects or weakens authorization, safety, evidence, or quality requirements.

## Validate

```bash
python scripts/validate.py
```

## Build

```bash
python scripts/build_compiled.py
python scripts/build_chatgpt_flat.py
```

## Repository tooling

The repository tooling derives skills, routes, source manifests, model resources, inventories, counts, hashes, build inputs, and conventional tasks from the registered repository model. It uses only the Python standard library. Git is required for local status, suggestion, commit, and explicitly requested publication.

Autonomous agent operations continue to use the GitHub connector. Native Git contacts a remote only when the user explicitly runs `publish` or supplies `--push` to `commit`.

Requirements: Python 3.11 or later, plus Git. No third-party Python package is required.

Global options such as `--root`, `--json`, and `--debug` precede the subcommand.

```bash
python scripts/tooling.py validate
python scripts/tooling.py build --temporary
python scripts/tooling.py build --output-base dist/tooling-builds
python scripts/tooling.py check
python scripts/tooling.py refresh-integrity --dry-run
python scripts/tooling.py refresh-integrity
python scripts/tooling.py tasks
python scripts/tooling.py suggest-commit
python scripts/tooling.py --json suggest-commit
python scripts/tooling.py commit --dry-run --auto-message
python scripts/tooling.py commit --auto-message
python scripts/tooling.py commit --message "Explicit imperative subject"
python scripts/tooling.py publish --dry-run
python scripts/tooling.py publish --remote origin --branch feature/example --expected-base <sha>
python scripts/tooling.py commit --auto-message --push --remote origin --branch feature/example
```

`validate`, `check`, `build --temporary`, `refresh-integrity --dry-run`, `suggest-commit`, and `commit --dry-run` do not modify tracked files, the index, or `HEAD`. Persistent `build` output is restricted to a configured ignored output directory. `refresh-integrity` atomically updates only `shared/manifests/integrity.json`.

`commit` refreshes derived metadata, validates, builds twice in temporary directories, checks determinism, stages the authorized repository changes, generates or accepts a message, and creates one local commit. Without `--push`, it performs no network operation.

`publish` is the only standalone networked command. It verifies a clean attached branch, resolves and validates the GitHub remote, discovers the remote default branch, fetches explicitly, requires exactly one local commit over the remote base, classifies the target branch as `ABSENT`, `EXACT`, or `DIVERGED`, pushes one explicit refspec without force, and verifies the remote SHA. `EXACT` is an idempotent success; `DIVERGED` is blocked.

`commit --push` combines the local commit flow with `publish`. Publication starts only after the local commit succeeds. A publication failure does not remove or rewrite the local commit and is reported separately as `LOCAL_COMMIT` and `REMOTE_PUBLICATION`.

`publish --dry-run` and `commit --dry-run --push` may read remote refs but do not fetch, push, change upstream configuration, update refs, write integrity metadata, or alter `HEAD`, index, or working tree.

The existing scripts remain independently executable:

```bash
python scripts/validate.py
python scripts/validate_gpt56.py
python scripts/verify_lossless.py
python scripts/build_compiled.py
python scripts/build_compiled.py --skills implementation validation-quality
python scripts/build_compiled.py --include practical-reasoning --exclude chat-recovery
python scripts/build_chatgpt_flat.py
```

### Discovery and configuration

The centralized bootstrap anchors are `SKILL.md`, `orchestrator/SKILL.md`, `orchestrator/registry.json`, `shared/manifests/routes.json`, and `shared/manifests/tooling.json`. Other files are derived from registry entries, route references, the source index, source manifests, model descriptors, profile maps, configured shared collections, and these task conventions:

```text
build_*.py
validate_*.py
verify_*.py
```

Private helpers, `__pycache__`, the unified CLI itself, and files outside `scripts/` are not executable tasks.

Derived metadata includes current skill and cross-cutting counts, source and evaluation counts, catalog counts, inventory, file hashes and sizes, dependency and route closure, build order, output counts, task inventory, and commit statistics. Explicit policy remains in `shared/manifests/tooling.json` or the relevant model descriptor. The flat-package maximum is an explicit policy rather than a derived count.

Local `commit` ends with a local commit unless `--push` is explicitly supplied. `publish` and `commit --push` use native Git only within the guarded local-tooling boundary; PR creation, merge, CI, issues, releases, and autonomous remote operations remain connector-native.
