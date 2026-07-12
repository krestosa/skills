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
7. Remote GitHub operations use the GitHub connector; local `git` remains local-only.

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
- Remote GitHub reads and writes use the GitHub connector.
- Local `git` is local-only and runs after ownership preflight.
- GitHub Read and Write catalogs remain verbatim.
- No GitHub workflows are included.
- Returned or interrupted delegated work produces one prompt-only code block with no external commentary.
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
