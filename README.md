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
[Objetivo o contexto]

Síntesis deliberativa:
Eudaimonia: ...
Telos: ...
Ergon: ...
Grug: ...
Phronesis: ...
Arete: ...
Synthesis: ...

[Instrucciones operativas]
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
| Practical Reasoning | `practical-reasoning` | Governs purpose, function, complexity, adaptation, quality, and user benefit through Eudaimonia, Telos, Ergon, Grug, Phronesis, and Arete, followed by Synthesis. | `Use practical-reasoning to keep the work aligned with its real purpose and adapt to evidence.` | Automatically attached unless the task is trivial, exact, reversible, and mechanical. |
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

`practical-reasoning` uses six internal minds and one terminal synthesis phase:

```text
Eudaimonia → legitimate user benefit or protected interest
Telos      → observable end state and why it matters
Ergon      → required functions
Grug       → challenges accidental complexity, premature abstraction,
             unjustified dependencies, unnecessary distribution,
             speculative scope, and hard-to-debug solutions
Phronesis  → adapts tactics to current evidence
Arete      → preserves correctness, security, compatibility,
             maintainability, and proportionate validation
Synthesis  → selects the simplest complete maintainable solution
```

Synthesis is not a seventh mind. The council produces one integrated decision. Grug is active for material architecture, implementation, refactoring, testing, debugging, tooling, prompt-system, API, dependency, framework, frontend, distributed-system, concurrency, performance, observability, migration, abstraction, multi-file, validation, and rewrite decisions, or whenever valid alternatives differ materially in complexity. Trivial exact mechanical work may use the frame lightly.

Grug cannot replace Ergon or Arete: required function and the necessary quality floor remain mandatory. Technical delegated prompts include Grug beside the other active minds and carry a compact instruction to challenge accidental complexity while still delivering complete behavior, invariants, and validation.

Private deliberation remains private. Every delegated prompt includes a brief public `Síntesis deliberativa` inside its block, after the objective or context and before operational instructions. The section contains only task-specific conclusions, constraints, real material conflicts, and concise shareable justification; it never exposes chain-of-thought, dialogue, votes, scores, characters, or separate monologues. It is contextual only and cannot change authority, scope, requirements, prohibitions, validation, stop rules, or reasoning routing.

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
- Generated delegated work uses one prompt code block containing `Síntesis deliberativa`, followed by one reasoning-only directive per prompt, with no other external commentary.
- The latest available target model remains internal and is absent from the visible directive.
- Practical reasoning never grants side effects or weakens authorization, safety, evidence, or quality requirements.


## Focal adaptive execution granularity

Focal keeps the existing lease, roadmap, Iris, validation, PR, merge, reconciliation, and release workflow. Work selection now uses two explicit lanes:

- `LOW_RISK_BULK` groups independent, reversible, mechanically verifiable corrections into one cycle, branch, and PR. Every modified file receives a dedicated single-file commit, each commit is validated, and the final combined head is validated again.
- `HIGH_IMPACT_INCREMENT` decomposes architecture, shaders, runtime, compatibility, security, data, critical CI, migration, or performance-sensitive work into vertical increments that deliver an observable, testable, mergeable capability. Commits may span related files when atomicity or intent requires it.

`WORK_SELECTION_PROOF` is mandatory before a cycle can finish without functional work. It evaluates at least three roadmap candidates—or every remaining candidate when fewer exist—and records dependencies, minimum observable slice, validation, evidence, budget, and a factual rejection code. A feature that is too large must be decomposed by functional capability and acceptance; complexity, “no bounded increment”, and time uncertainty are internal granularity failures, not terminal reasons. Selection must complete within the first fifteen real minutes after lease acquisition.

### Focal closed NO-OP contract

Only five codes may produce `NO-OP`:

- `ACTIVE_RUN`;
- `PROJECT_ALREADY_COMPLETE`;
- `NO_AUTHORIZED_WORK`;
- `ALL_REMAINING_WORK_EXTERNALLY_BLOCKED`;
- `LATE_ACQUIRE_ORPHANED`.

If the roadmap still contains `PENDIENTE`, `EN PROGRESO`, or `REVALIDAR`, the process must repair granularity and execute a vertical slice. Repeating the same selection-related `NO-OP` in consecutive cycles is `NOOP_REASON_REPEATED`. Every reported coordinator status includes the exact UTC observation time because `IDLE` and `WORKING` are snapshots that may change after the read.

A checkpoint is only a recovery mechanism for an objective contingency; it is never a planned deliverable. A following cycle resumes the same partial unit first, and a second consecutive `PARTIAL` requires new objective evidence. Quality gates reject filler code, placeholders, falsely complete stubs, dead code, avoidable duplication, speculative abstractions, silent fallbacks, untracked TODOs, opportunistic refactors, and tests that merely mirror implementation shape.

<!-- focal-autonomous-blockers:start -->
## Focal autonomous work blockers

This matrix is the exhaustive registry of known failure classes in the active Focal prompt stack. An unexpected condition is `UNCLASSIFIED_INTERNAL_FAILURE` and enters the autonomous diagnostic loop; it must not become immediate `BLOCKED` or an invented success path. Internal and implementable failures are repaired autonomously. Only a proven external capability gap may become `EXTERNAL_BLOCKER`.

| Code | Blocking condition | Evidence required | Recovery procedure | Resume condition |
|---|---|---|---|---|
| `PROMPT_FILE_MISSING` | The entrypoint or a required module does not exist. | Repository, SHA, exact path, and 404 or missing-file result. | Do not touch Focal. Restore the file in `krestosa/skills` through `SKILLS_MAINTENANCE`, update references and integrity, then validate. | Every module listed by the entrypoint exists at one stable SHA. |
| `PROMPT_FILE_EMPTY` | A required prompt file is empty. | Path, SHA, and observed zero-length content. | Restore canonical content through `SKILLS_MAINTENANCE`; never use a remembered copy. | The complete file is readable and validation passes. |
| `PROMPT_READ_INCOMPLETE` | A file cannot be read through its last line. | Last confirmed line, path, SHA, and connector error. | Retry the connector read once; if still incomplete, stop and repair the retrieval route or file. | All files are read completely from the same SHA. |
| `PROMPT_SHA_CHANGED` | `krestosa/skills` changes during loading. | Initial SHA, changed SHA, and timestamps. | Restart loading once from the new SHA. Stop if it changes again. | One complete load finishes against one stable SHA. |
| `PROMPT_REFERENCE_BROKEN` | The entrypoint or a module references a missing active module. | Referencing path, target path, and validation output. | Correct the reference or restore the target; update manifest, flowchart, and integrity. | No broken prompt references remain. |
| `PROMPT_CONTRADICTION` | Two active modules impose incompatible rules. | Exact paths and conflicting passages. | Use `SKILLS_MAINTENANCE`; remove the contradiction rather than relying on precedence permanently. | Validators and manual review confirm one rule per concept. |
| `ISSUE_7_MISSING` | The canonical coordination issue does not exist. | Repository and issue lookup result. | Enter `COORDINATOR_REPAIR` only when no active execution evidence exists; recreate the exact issue contract through the connector. | Issue #7 exists with the expected title and both v3 blocks. |
| `ISSUE_TITLE_MISMATCH` | Issue #7 has the wrong title. | Observed and expected titles. | Correct only the title while preserving both blocks and body content. | The exact canonical title is observed. |
| `COMMAND_BLOCK_INVALID` | `focal-command:v3` is missing, duplicated, malformed, or not a JSON object. | Full issue body and parser error. | Repair the command block through the connector without altering valid state data. | Exactly one valid command block with schema version 3 exists. |
| `STATE_BLOCK_INVALID` | `focal-state:v3` is missing, duplicated, malformed, or not a JSON object. | Full issue body and parser error. | Repair coordinator infrastructure; do not manually invent an active lease. | Exactly one valid state block exists and the coordinator can update it. |
| `STATE_SCHEMA_UNSUPPORTED` | Either block uses an unsupported schema version. | Observed schema versions. | Migrate the coordinator and issue contract together under `COORDINATOR_REPAIR`. | Both blocks use the active schema and tests pass. |
| `STATE_REPOSITORY_MISMATCH` | The state names a repository other than `krestosa/Focal`. | Observed repository field. | Repair the state contract through the coordinator; do not continue functional work. | The repository field matches exactly. |
| `STATE_INVALID_COMBINATION` | State fields are internally inconsistent, such as `idle` with a run owner or `working` without expiry. | Full state block and violated invariant. | Diagnose coordinator or stale-state failure; use repair or watchdog logic without discarding remote work. | State satisfies all idle or working invariants. |
| `INSPECT_LATENCY_NOT_OBSERVED` | The run declares failure before 45 seconds of real polling. | Command write time and read timestamps. | Continue polling every 5–10 seconds; do not diagnose a coordinator fault from immediate reads. | `STATE_OBSERVED` arrives or a terminal failed run is proven. |
| `INSPECT_NOT_PROCESSED` | A new inspect command remains uncorrelated after the full window. | Command ID, 45-second timeline, state reads, and associated runs. | Enter `COORDINATOR_REPAIR` only if the issue is idle and no active work exists. | A fresh inspect returns `STATE_OBSERVED`. |
| `COMMAND_DELIVERY_DELAYED` | A valid command remains uncorrelated because issue-edit delivery is delayed or lost. | Command ID, write time, both 45-second polling windows, issue state, and workflow runs. | Reissue the operation once with a new command ID and recalculated timestamps, then observe the scheduled five-minute fallback for up to six minutes when the budget allows. | The command correlates, or retry and fallback are exhausted with factual evidence. |
| `LATE_ACQUIRE_ORPHANED` | Acquire is accepted after the caller already emitted a terminal result. | Acquire command ID, run ID, caller end time, and `lastCommandProcessedAt`. | Do not resume work retrospectively. Release the same run ID immediately with a neutral factual note. | State returns to idle with `LEASE_RELEASED` for the late run ID. |
| `OPERATIONAL_PROVENANCE_PRESENT` | Issue state, commands, logs, notes, branches, commits, PRs, reports, or artifacts identify the execution client or provider. | Exact controlled path or field containing the provenance value. | Remove prohibited fields, reject them in new commands, scrub legacy state on the next valid transition, and keep only opaque command and run IDs. | Controlled repository artifacts contain no execution-client provenance and regression validation passes. |
| `COORDINATOR_RUN_FAILED` | The coordinator workflow or job ends in failure or cancellation. | Run ID, job ID, failing step, and logs. | Repair the smallest verified cause through connector or Actions; test the real invocation path. | A new run succeeds and correlates the command. |
| `COORDINATOR_WORKFLOW_MISSING` | `.github/workflows/automation-state.yml` is absent or unreadable. | Default-branch SHA and missing path. | Restore it under `COORDINATOR_REPAIR`, validate, clean temporary history, then smoke-test. | The workflow exists on main and processes inspect. |
| `COORDINATOR_PERMISSION_DENIED` | The workflow cannot read or update issue #7 or required refs. | Workflow permissions and API error. | Grant only the repository permissions declared by the workflow; never modify secrets or protections without authorization. | The coordinator updates state successfully with least privilege. |
| `COORDINATOR_SENDER_REJECTED` | An authorized GitHub App edit is discarded by a fixed sender allowlist. | Event sender and rejection path or logs. | Remove fixed login gating; rely on issue scope, permissions, schema, command correlation, lease invariants, concurrency, and idempotence. | Connector-issued inspect succeeds. |
| `COORDINATOR_IMPORT_FAILED` | Python cannot import the coordinator or a dependency. | Traceback, checkout path, command, and `PYTHONPATH`. | Execute as an importable module and set repository-root `PYTHONPATH`; add a workflow contract test. | The exact workflow invocation imports and runs. |
| `COORDINATOR_RECURSION` | The workflow repeatedly processes its own issue edit. | Repeated runs and unchanged command IDs. | Enforce idempotence when `lastCommandId == commandId` and serialized concurrency. | One command causes one effective state transition. |
| `ACTIVE_LEASE` | Another run owns a future lease. | Run ID, phase, heartbeat, expiry, and exact observation UTC. | Return `NO-OP` with code `ACTIVE_RUN`; do not inspect functional work, wait, cancel, overwrite, or release it. | A later independent execution observes idle or a safely expired lease. |
| `COORDINATOR_STATUS_STALE_REPORT` | A report presents `IDLE` or `WORKING` without the exact observation time or implies the snapshot is still current. | Report text, issue read timestamp, and later state transition when available. | Add `Estado observado UTC`, describe the value as a snapshot, and never claim it cannot change after the read. | Every coordinator status in the terminal report carries an exact UTC observation timestamp. |
| `EXPIRED_LEASE_WITH_ACTIVE_WORK` | Lease time passed but workflows, branch, or PR activity shows the owner may still be active. | Expiry, workflow status, and recent remote activity. | Preserve ownership; do not recover until positive activity is absent under the configured grace rules. | Expired lease plus no active mutating workflow or recent branch/PR activity. |
| `ACQUIRE_REJECTED` | Acquire is processed but does not return `LEASE_ACQUIRED`. | Command ID, reason, state, and expiry. | Re-read state; classify active lease, invalid command, or coordinator fault. Never assume ownership. | State confirms working, own run ID, accepted command, expected reason, and future expiry. |
| `RECOVER_REJECTED` | Recover is processed but does not return `LEASE_RECOVERED`. | Command ID, prior state, remote activity evidence, and reason. | Preserve prior work, correct recovery preconditions, or stop. | Recovery is explicitly accepted for the new run ID. |
| `HEARTBEAT_REJECTED` | Heartbeat returns `NOT_LEASE_OWNER`, error, or remains unprocessed. | Command ID, run ID, state, expiry, and workflow evidence. | Stop mutations immediately; do not fabricate or reacquire retrospectively. | Ownership is safely re-established by a new valid cycle, not by continuing the old one. |
| `LEASE_MARGIN_UNSAFE` | Less than five minutes remain before a mutation. | Current UTC and `leaseExpiresAt`. | Send heartbeat and wait for `HEARTBEAT_ACCEPTED` before mutating. | A future lease with at least five minutes of margin is confirmed. |
| `LEASE_OWNERSHIP_LOST` | State becomes idle, changes run ID, or expires unsafely during work. | Last owned state and first conflicting state. | Stop reads and writes, preserve existing remote evidence, and report `PARTIAL` or `BLOCKED`. | A new independent cycle acquires or recovers the lease. |
| `REMOTE_HEAD_CHANGED` | Main changes after the baseline or before merge. | Old and new SHAs and compare result. | Rebase or reconstruct from the new remote state without force; repeat relevant validation. | Branch and acceptance evidence target the current main. |
| `REMOTE_STATE_AMBIGUOUS` | Available refs, PRs, checks, or issue data do not determine a safe next action. | Conflicting observations and unavailable evidence. | Use allowed fallbacks once; preserve work and stop rather than guess. | One authoritative remote state is verified. |
| `RECOVERY_REF_MISSING` | The state points to a branch, PR, or checkpoint that no longer exists. | State fields and missing-ref results. | Search remaining remote refs and PR history; mark affected roadmap items `REVALIDAR`. | A valid remote checkpoint is found or the missing work is explicitly re-planned. |
| `BRANCH_DIVERGED` | Work branch no longer has a safe, known relationship to main. | Compare metadata and head SHAs. | Preserve the branch, create a reconciled branch from current main, and port only verified changes. | The new branch has a reviewed diff and valid baseline. |
| `PR_HEAD_CHANGED` | The PR head changes after validation. | Expected and observed head SHA. | Re-run diff review and all invalidated checks; never merge stale evidence. | CI and review apply to the exact current head. |
| `CI_PENDING` | Required checks are queued, waiting, or in progress. | Check names, run IDs, statuses, and head SHA. | Preserve checkpoint and PR; do not merge or mark complete. | Every required check reaches an accepted terminal state. |
| `CI_FAILED` | A required check fails. | Failing check, logs, and head SHA. | Fix failures caused by the change; classify unrelated infrastructure failure separately. | Required checks pass on the corrected exact head. |
| `CI_UNAVAILABLE` | Actions, logs, or checks cannot be queried or started. | Connector error and affected run/check. | Use another authorized read route or preserve a `PARTIAL` checkpoint; do not claim validation. | CI evidence becomes observable or an explicitly approved equivalent gate exists. |
| `VALIDATION_HARNESS_MISSING` | A required validator, fixture, schema, or script is absent. | Required contract and missing path. | Classify as `INTERNAL_WORK_REQUIRED`; implement it as a bounded unit. | The harness exists and proves the acceptance criteria. |
| `OPENGL_RUNTIME_UNAVAILABLE` | `focal-gl` cannot create a context, compile, render, or read back. | Probe output, platform, GL version, driver, and failing command. | Repair the runtime harness or use a documented compatible backend; do not mark graphical work complete. | `probe`, `compile`, `render`, and `suite` pass as required. |
| `OPENGL_DRIVER_UNSTABLE` | The driver crashes, resets, hangs, or produces unsafe behavior. | Exit status, logs, driver/GPU data, and reproducible minimal case. | Stop dangerous loads, reduce to a safe diagnostic, document the external limitation, and avoid repeated stress. | A safe supported environment completes required validation. |
| `IRIS_PRIMARY_DOCS_UNAVAILABLE` | Primary Iris documentation required for a capability decision cannot be accessed. | Exact documentation URL and retrieval failure. | Keep the capability pending or `REVALIDAR`; do not substitute memory or secondary claims as proof. | Primary evidence is available and recorded in the matrix. |
| `ROADMAP_MISSING` | `docs/ROADMAP.md` is absent. | Main SHA and missing path. | Create it during `ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT` before feature selection. | Roadmap exists with canonical states, dependencies, acceptance, evidence, and Iris links. |
| `IRIS_MATRIX_MISSING` | `docs/IRIS-CAPABILITY-MATRIX.md` is absent. | Main SHA and missing path. | Create it and link it bidirectionally with the roadmap. | The matrix covers the decisions needed for the cycle. |
| `ROADMAP_EVIDENCE_INSUFFICIENT` | An item is marked complete without proof in main and accepted checks. | Item, claimed evidence, and missing proof. | Downgrade to `REVALIDAR`, `EN PROGRESO`, or `PENDIENTE`; collect evidence. | Completion criteria and evidence are both satisfied. |
| `TIME_BUDGET_EXHAUSTED` | Remaining time cannot cover implementation, validation, publication, reconciliation, and release. | Elapsed time and remaining mandatory phases. | Stop new work, publish a recoverable checkpoint, reconcile documentation, and release if owned. | A future cycle starts from the remote checkpoint with a fresh budget. |
| `CHECKPOINT_NOT_PUBLISHED` | Relevant work exists only locally or in an unreferenced state. | Missing remote branch, commit, PR, or checkpoint SHA. | Publish a coherent remote checkpoint before waiting, soft stop, CI, or merge. | The state issue references a valid remote checkpoint. |
| `MERGE_BLOCKED` | Required checks, review, permissions, branch policy, or head verification prevents merge. | PR number, head SHA, mergeability, reviews, and checks. | Correct actionable causes or leave a `PARTIAL` PR; never bypass required gates. | The exact head satisfies every merge gate. |
| `RELEASE_NOT_PROCESSED` | The final release command does not correlate. | Release command ID, polling timeline, state, and coordinator run. | After release, perform no new mutation; continue read-only polling and report incomplete confirmation. | State shows idle, null run ID, own `lastRunId`, and `LEASE_RELEASED`. |
| `STALE_LEASE` | A working lease is expired and no owner activity remains. | Expiry, command correlation, workflows, branch activity, and PR activity. | Use the watchdog or `recover` path while preserving checkpoint and abandonment audit fields. | The state is safely idle or `LEASE_RECOVERED` by a new run. |
| `NOOP_COMMIT_REACHABLE` | A single-parent commit has the same tree as its parent and remains reachable from a controlled branch. | Candidate SHA, parent SHA, both tree SHAs, refs containing it, and proof that it is not signed, tagged, released, protected, or required by another PR. | Use the GitHub Actions history sanitizer to omit it and replay later commits with original metadata. Never classify by message alone. | The candidate is absent from controlled heads and tags, later diffs are equivalent, and the final tree is validated. |
| `EMPTY_ARTIFACT_COMMIT_REACHABLE` | A commit containing only zero-byte transport files remains reachable. | Candidate diff, file sizes, modes, paths, refs, and final-tree proof. | Sanitize only when the diff has no functional content, rename, mode, submodule, or semantic effect; replay later commits and preserve their original timestamps. | No candidate SHA or zero-byte transport artifact is reachable from controlled heads or tags. |
| `FAILED_TRANSPORT_COMMIT_REACHABLE` | A failed automation attempt left a transport-only commit or branch. | Correlated failed run, candidate diff, expected head, refs, and replay proof. | Run the sanitizer through GitHub Actions, update with force-with-lease, remove the temporary workflow, and delete every transport branch or tag. | The validated tree is published with no cleanup commit and no transport ref remains. |
| `HISTORY_SANITATION_TIMESTAMP_MISMATCH` | A replayed later commit received the cleanup time or different author/committer metadata. | Old/new commit mapping, author and committer names/emails, authorDate, committerDate, timezone, message, and parent mapping. | Rebuild the affected chain with commit-tree while setting exact original GIT_AUTHOR_DATE and GIT_COMMITTER_DATE; abort before ref update on any mismatch. | Every replayed commit preserves its exact original metadata and semantic diff. |
| `HISTORY_SANITATION_REF_REMAINS` | Candidate commits, cleanup workflows, branches, or tags remain reachable after sanitation. | refs/heads and refs/tags reachability output, workflow path, branch list, and candidate SHAs. | Delete sanitizer-created refs in the same Action, remove workflow/script from the final tree, and verify again. Do not add a cleanup commit. | No candidate or temporary artifact is reachable from controlled heads or tags and no cleanup commit exists. |
| `TEMP_REPAIR_HISTORY_PRESENT` | Coordinator repair commits or merges remain reachable from main. | Main ancestry and temporary SHAs. | Use the approved GitHub Actions tree-preserving rewrite; never clean it from a local clone or chat force push. | Main has the validated tree and no temporary repair commit is reachable. |
| `TEMP_WORKFLOW_PRESENT` | A workflow used only to perform repair or history cleanup remains in the final tree. | Final tree and workflow path. | Rebuild the final tree without the workflow and re-verify before smoke testing. | The temporary workflow path is absent from main. |
| `TREE_MISMATCH_AFTER_REWRITE` | The rewritten main tree differs from the validated repair tree. | Both tree SHAs and diff. | Abort or restore the expected ref; rebuild the commit with the exact validated tree. | Tree SHAs are identical and the diff is empty. |
| `METADATA_MISMATCH_AFTER_REWRITE` | Parent, author, committer, dates, or message changed unexpectedly. | Old and new commit metadata. | Recreate the commit through Actions with exact preserved metadata and verify each field. | Every required metadata field matches exactly. |
| `AUTHORIZATION_MISSING` | The requested mutation exceeds the current repository or mode authorization. | Requested action and active authorization boundary. | Stop and request only the indispensable authorization. | Explicit authorization covers the exact action and repository. |
| `CREDENTIAL_MISSING` | A required GitHub permission or credential is unavailable and no connector route works. | Failed operation and permission error without secrets. | Use the installed connector or Actions token; request intervention only when no authorized alternative exists. | The required least-privilege operation succeeds. |
| `CONNECTOR_TRANSIENT_FAILURE` | A connector read or write returns a timeout, disconnect, `429`, `5xx`, temporary-unavailable response, transport failure, or internal exception without an authoritative rejection. | Operation, attempt number, UTC timestamps, error class, and any `Retry-After` value. | Retry the same task and operation up to four total attempts with 2, 5, 10, and 20 second backoff. Do not terminate on the first error. | The same remote operation succeeds or an authoritative remote read determines its outcome. |
| `CONNECTOR_MUTATION_OUTCOME_UNKNOWN` | A mutating call returns an error, so it is unknown whether GitHub applied it. | Intended payload, idempotency identifier or expected SHA, error, and authoritative resource to verify. | Perform `read-after-write`. If the effect exists, continue without duplication; otherwise retry the exact same operation while its guards remain valid. | The intended effect is observed or the unchanged authoritative state proves a safe retry. |
| `CONNECTOR_RETRY_EXHAUSTED` | Four attempts, `read-after-write`, and applicable fallbacks are exhausted, or the remaining runtime cannot support a safe retry and closure. | Attempt timeline, last authoritative state, lease status, branch/PR/checkpoint evidence, and remaining budget. | Preserve remote checkpoints and return `PARTIAL` when useful work exists; use `BLOCKED` only when no recoverable evidence exists. The next independent execution resumes the same remote task. | A later execution restores connector access and resumes from the recorded remote state. |
| `GITHUB_SERVICE_UNAVAILABLE` | GitHub API, Actions, or repository service remains unavailable after the connector retry safeguard is exhausted. | Time, endpoint or operation, attempt timeline, and service error. | Preserve remote state already created and stop as `PARTIAL` or `BLOCKED`; never simulate results. | The service is reachable and state can be revalidated. |
| `UNSAFE_OPERATION` | Completion would require unauthorized secrets, destructive local force push, dangerous GPU load, or illegal action. | Required operation and violated safety rule. | Refuse that path and use a safe authorized alternative; otherwise stop. | A safe legal route satisfies the same acceptance criteria. |
| `ROADMAP_GRANULARITY_FAILURE` | Active roadmap work exists but no vertical, observable, mergeable increment was selected. | `WORK_SELECTION_PROOF`, active items, rejected candidates, elapsed selection time, and missing slice. | Repair the first priority item, define its minimum functional increment, update acceptance, and execute that increment in the same cycle. | A bounded slice is selected and implementation begins. |
| `WORK_SELECTION_PROOF_MISSING` | The cycle tries to stop without evaluating at least three candidates or all remaining candidates. | Candidate record, roadmap state, dependencies, validation, budget, and rejection codes. | Return to selection and complete the proof before any terminal classification. | The proof contains the required candidates and one selected slice or a closed NO-OP cause. |
| `NOOP_REASON_INVALID` | A cycle uses `NO-OP` for complexity, time uncertainty, “no bounded increment”, or any reason outside the closed set. | Release note, roadmap state, and missing allowed code. | Reclassify as recovery, granularity repair, `PARTIAL`, or exact blocker; do not preserve the invalid reason. | The result uses one allowed code with evidence. |
| `NOOP_REASON_REPEATED` | Consecutive cycles repeat a selection-related `NO-OP` while active roadmap work remains. | Last two run results, notes, roadmap states, and candidate proofs. | Change hypothesis, decompose the first priority, and execute the smallest vertical slice. | The next cycle publishes functional progress or a new objective external blocker. |

| `PROMPT_ENCODING_INVALID` | A required prompt is not valid UTF-8 or contains undecodable bytes. | Path, blob SHA, failing byte range, and read error. | Recover the authoritative blob, restore valid UTF-8 in `SKILLS_MAINTENANCE`, refresh integrity, and reload every module from one SHA. | The file decodes completely and prompt validation passes. |
| `PROMPT_PARSE_FAILED` | Markdown structure, fenced data, or a required prompt contract cannot be parsed. | Path, SHA, parser output, and malformed range. | Repair the smallest malformed region, validate references and derived flowchart, then restart prompt loading. | Parsing and stack validation pass at one stable SHA. |
| `PROMPT_INTEGRITY_STALE` | Integrity metadata does not match the active prompt tree. | Expected and observed hashes, inventory, and changed paths. | Recompute integrity only after validating intended changes; never accept stale metadata as evidence. | Integrity regeneration is deterministic and repository checks pass. |
| `PROMPT_VALIDATOR_FAILED` | The prompt stack validator rejects current content. | Exact validator command, exit code, and every diagnostic. | Treat each diagnostic as internal work, repair causes, add regression assertions, and rerun the full validator. | Validator and repository checks pass on the exact head. |
| `CONNECTOR_RATE_LIMITED` | API operations receive rate or abuse limits. | Status, headers, Retry-After, operation, and attempt timeline. | Respect Retry-After, back off, reduce duplicate reads, use batched or alternate authorized routes, and continue the same task. | An authoritative operation succeeds without exceeding limits. |
| `CONNECTOR_AUTH_EXPIRED` | The active connector session or token is no longer accepted. | Sanitized authentication error and failed operation. | Retry session refresh and authorized alternate routes; preserve checkpoint. Escalate only when no connector or Actions permission can perform the exact operation. | The least-privilege operation succeeds. |
| `CONNECTOR_PERMISSION_SCOPE` | The available token lacks a required repository permission. | Endpoint, required permission, observed permission, and error. | Use an existing authorized route or reduce the operation to available scope. Request only the missing permission when no safe route exists. | The exact operation succeeds with least privilege. |
| `CONNECTOR_PAGINATION_INCOMPLETE` | A list or search result is truncated or a cursor is missing. | Page metadata, cursor, counts, and query. | Continue only with returned cursors, increase bounded limits, or use an authoritative targeted lookup; never infer absence from a partial page. | The relevant result set or target object is conclusively resolved. |
| `CONNECTOR_RESPONSE_MALFORMED` | A tool response is truncated, structurally invalid, or lacks required fields. | Raw sanitized response shape, operation, and expected schema. | Retry the read, use a narrower endpoint, and validate the authoritative object before acting. | A complete schema-valid response is observed. |
| `REMOTE_OBJECT_TEMPORARILY_MISSING` | An expected issue, ref, file, run, or PR returns a transient 404 or indexing delay. | Object identity, prior evidence, timestamps, and repeated lookups. | Re-read by exact identifier, verify parent repository and ref, allow propagation delay, and use alternate authoritative endpoints. | Existence or permanent absence is proven. |
| `LOCAL_PROCESS_CRASHED` | A controlled local compiler, test, renderer, or helper exits unexpectedly. | Command, environment, exit status, stderr, and last checkpoint. | Minimize the reproducer, repair the process or inputs, terminate orphan children, and rerun under timeout. | The exact command completes and dependent validation passes. |
| `LOCAL_PROCESS_TIMEOUT` | A controlled subprocess exceeds its bounded timeout. | Command, timeout, partial output, resource data, and phase. | Kill the process tree, reduce the case, distinguish hang from slow work, repair, and rerun with a justified bound. | The operation completes within the documented limit. |
| `LOCAL_PROCESS_OOM` | A process is killed or fails because memory is exhausted. | Exit signal, memory evidence, command, input size, and environment. | Reduce memory pressure, stream or shard work, fix leaks, lower safe workload, and rerun; never repeat an unsafe load unchanged. | The required validation completes within resource limits. |
| `DISK_SPACE_EXHAUSTED` | Checkout, build, artifact, or cache creation fails for lack of disk. | Filesystem usage, failing path, and operation. | Remove only reproducible caches and temporary outputs, use bounded artifacts, and rerun without deleting remote checkpoints. | Adequate space exists and the operation succeeds. |
| `FILESYSTEM_PERMISSION_DENIED` | A local path cannot be read, written, executed, or removed. | Path, mode, owner, operation, and error. | Use a workspace-owned path, correct repository file mode when intended, or choose an authorized execution route. | Required access succeeds without broad permission escalation. |
| `PATH_CASE_MISMATCH` | A path differs by case, separator, normalization, or platform convention. | Referencing and actual paths plus platform. | Normalize canonical relative paths, update all references, and add cross-platform validation. | Every reference resolves on supported platforms. |
| `DEPENDENCY_UNAVAILABLE` | A required dependency cannot be fetched, resolved, or invoked. | Dependency, version constraint, source, and error. | Use pinned existing caches or an authorized compatible source, implement an internal substitute when in scope, or checkpoint until the external source returns. | The dependency or approved substitute is reproducibly available. |
| `DEPENDENCY_VERSION_MISMATCH` | Installed or resolved versions violate compatibility constraints. | Expected range, observed versions, lock data, and failing test. | Resolve the latest mutually compatible pinned set from primary evidence, update locks and tests, and rerun compatibility validation. | All version constraints and acceptance tests pass. |
| `CACHE_CORRUPTED` | A build, dependency, shader, or workflow cache produces inconsistent results. | Cache key, clean-run comparison, hashes, and failure. | Invalidate only the affected reproducible cache, rebuild from authoritative inputs, and verify determinism. | Clean and cached runs produce equivalent accepted results. |
| `SOURCE_FILE_TRUNCATED` | A source or document ends prematurely or loses required sections. | Path, blob SHA, parser error, prior valid evidence, and expected structure. | Restore from the latest authoritative functional version or reconstruct from specs and tests, then validate the complete file. | Structure, references, and tests prove completeness. |
| `SOURCE_ENCODING_INVALID` | A project file uses an unsupported encoding or invalid byte sequence. | Path, detected bytes, expected encoding, and consumer error. | Convert from verified source to the canonical encoding without semantic loss and add an encoding check. | All consumers parse the exact file consistently. |
| `STRUCTURED_FILE_INVALID` | JSON, YAML, TOML, properties, XML, or another structured file is invalid. | Parser output, path, SHA, and schema when available. | Repair syntax and schema, preserve unknown valid fields, and rerun every consumer. | Parser, schema, and integration tests pass. |
| `BROKEN_INTERNAL_REFERENCE` | An import, include, link, path, manifest entry, shader include, or workflow reference is broken. | Source path, target, resolver output, and ref. | Restore or correct the target, update all derived indexes, and add a reference validator. | Every internal reference resolves from the exact tree. |
| `ACCIDENTAL_FILE_DELETION` | A required file is removed unintentionally. | Deleting commit, prior blob, consumers, and failing checks. | Restore the authoritative prior blob or reconstruct the intended version, preserve later valid changes, and validate consumers. | The required file and all dependent behavior are restored. |
| `GARBAGE_ARTIFACT_FILE` | A file created by mistake has no build, runtime, test, documentation, packaging, or coordination role. | Introducing commit and run, content, references search, conventions, and deletion validation. | Remove it through history sanitation when required, preserving functional changes and later metadata. | The file is absent from controlled refs and all affected validation passes. |
| `PLACEHOLDER_GARBAGE_FILE` | A mistaken file contains only one or a few non-semantic tokens such as `X` or a placeholder marker. | Normalized content, path semantics, introducing run, no-reference proof, and legitimate-minimal-file checks. | Remove only after proving it is not a marker, module, fixture, sentinel, license, or valid minimal format; sanitize mixed commits path-selectively. | No placeholder artifact remains and functional behavior is unchanged. |
| `TOOL_OUTPUT_ARTIFACT_FILE` | Tool arguments, payloads, responses, IDs, or serialized output were committed as a project file. | Content classification, introducing operation, path, references, and expected file contract. | Remove the accidental path or restore intended content, sanitize history, and add a check against tool-output shapes. | The tree contains only intended project content. |
| `ERROR_DUMP_ARTIFACT_FILE` | A traceback, error page, Not Found response, or temporary diagnostic was committed unintentionally. | File content, failed run correlation, fixture search, and consumer analysis. | Preserve intentional fixtures; otherwise remove the dump, reconstruct any intended file, and sanitize history. | No accidental error dump is reachable and tests pass. |
| `TRUNCATED_GENERATION_ARTIFACT_FILE` | A generated file is cut off mid-syntax or mid-content because creation failed. | Parser failure, abrupt ending, generation run, expected structure, and prior version. | Regenerate or reconstruct atomically, validate completeness, and remove the truncated history artifact. | The complete file passes parser and consumer checks. |
| `WRONG_PATH_ARTIFACT_FILE` | Content was written to an accidental name, extension, duplicate, or unused directory. | Intended and observed paths, references, packaging rules, and duplicate comparison. | Move or reconstruct the content at the canonical path, update references, and remove the accidental path through sanitation. | One canonical path remains and every consumer resolves it. |
| `GARBAGE_ARTIFACT_COMMIT_REACHABLE` | A commit changes the tree only by adding or modifying proven garbage artifacts. | Candidate SHA, path classifications, diff, refs, run, and expected tree proof. | Omit the commit through GitHub Actions, replay later commits with exact metadata, and delete temporary refs. | Candidate and garbage paths are unreachable from controlled heads and tags. |
| `GARBAGE_ARTIFACT_MIXED_COMMIT` | A commit combines valid work with accidental garbage files. | Per-path classification, functional diff, candidate tree, and replay plan. | Rebuild that commit tree without garbage paths while preserving every functional change and original metadata, then replay later commits. | Functional diff is equivalent, garbage is absent, and timestamps are exact. |
| `BINARY_ARTIFACT_CORRUPTED` | A binary asset or generated artifact has invalid bytes, checksum, format, or size. | Path, expected and actual checksum, parser or decoder output, and source. | Restore or regenerate from authoritative inputs, verify deterministic checksum where applicable, and rerun consumers. | Format, checksum, and integration validation pass. |
| `UNEXPECTED_MODE_CHANGE` | A file mode or executable bit changes without functional intent. | Old and new modes, commit, platform, and consumers. | Restore the intended mode, preserve content, and add cross-platform mode validation when relevant. | Modes match repository policy and checks pass. |
| `NON_FAST_FORWARD` | A branch update is rejected because the remote head moved. | Expected and observed heads plus compare data. | Re-read remote state, reconcile or replay verified changes onto the new head, revalidate, and retry without blind force. | The update targets the current head with valid evidence. |
| `MERGE_CONFLICT` | Verified changes conflict with current main or another required branch. | Conflict paths, base and heads, semantic intent, and tests. | Resolve from current authoritative content, preserve both required intents, rerun invalidated tests, and update the PR. | Conflicts are absent and exact-head validation passes. |
| `BRANCH_MISSING` | A required work or recovery branch no longer exists. | Expected branch, state reference, PR data, commits, and lookup results. | Recover from PR head, commit SHA, artifacts, or create a reconciled branch from main and port verified diffs. | A remote branch references a coherent checkpoint. |
| `PR_MISSING` | State references a PR that does not exist. | PR number, branch, commit, and state evidence. | Search exact head and recent PRs, then open a replacement PR only when no existing one represents the same work. | One canonical PR points to the current checkpoint. |
| `PR_CLOSED_UNMERGED` | The task PR was closed without merge while work remains valid. | PR state, head, comments, checks, and close reason. | Determine whether closure was supersession or error, recover the head, address causes, and reopen or create one replacement PR. | A single active PR represents the verified work or roadmap records abandonment. |
| `CHECK_RUN_STALE` | CI evidence belongs to an older head or tree. | Check SHA, current head, timestamps, and invalidated paths. | Discard stale acceptance evidence and rerun all affected checks on the exact head. | Required checks reference the current head. |
| `CI_CANCELLED` | A required workflow or job is cancelled. | Run, job, actor-neutral reason, head, and logs. | Determine transient versus intentional cancellation, rerun safely, and fix deterministic cancellation causes. | The required job reaches an accepted terminal result. |
| `CI_SKIPPED` | A required job is skipped because conditions or paths are wrong. | Workflow expression, event, changed paths, and job result. | Correct conditions or trigger an authorized equivalent run; add a contract test for the expected path. | The required validation actually executes on the exact head. |
| `WORKFLOW_SYNTAX_INVALID` | A workflow cannot load because YAML or expressions are invalid. | Workflow path, parser or platform diagnostic, and commit. | Repair syntax and expressions, validate locally or with a parser, and rerun the real event path. | The workflow is accepted and jobs start. |
| `ACTION_VERSION_UNAVAILABLE` | A referenced action, commit, runtime, or runner component is unavailable. | Action ref, error, and supported alternatives. | Pin a verified supported commit or replace with a minimal native step, then rerun supply-chain and workflow checks. | The workflow resolves only approved available components. |
| `RUNNER_UNAVAILABLE` | No compatible CI runner starts the job. | Labels, queue time, platform status, and required environment. | Retry boundedly, use another declared compatible runner, or preserve checkpoint until capacity returns. | A compatible runner completes the required job. |
| `WORKFLOW_ARTIFACT_MISSING` | A required CI artifact was not uploaded, expired, or cannot be fetched. | Run, artifact name, upload step, retention, and consumer. | Rerun the producer, fix paths and retention, verify checksums, and consume the artifact from the same head. | The expected artifact is available and validated. |
| `TEST_FLAKY` | A test alternates pass and fail without code changes. | Repeated runs, seeds, environment, timing, and failure signature. | Reproduce deterministically, remove races or nondeterminism, fix the test or product cause, and never accept retries alone as proof. | Repeated clean runs are stable. |
| `TEST_TIMEOUT` | A test exceeds its justified time bound. | Test, duration, logs, resource use, and last progress. | Isolate the hang or performance issue, fix it, and set a documented realistic bound. | The test completes reliably within the bound. |
| `GLSL_PARSE_FAILED` | Shader source cannot be lexed or parsed. | Stage, file, line, preprocessed source, and compiler diagnostic. | Fix syntax or preprocessing, validate includes and profile constraints, and compile the exact variant. | Parsing succeeds for every required profile. |
| `GLSL_COMPILE_FAILED` | A shader stage fails compilation. | Stage, defines, profile, driver/compiler, source, and full log. | Reduce the failure, repair types, interfaces, extensions or generated code, then run compile and render suites. | Required variants compile on supported targets. |
| `GLSL_LINK_FAILED` | Compiled shader stages fail program linkage. | Stage interfaces, outputs, bindings, compiler log, and variant. | Reconcile interfaces and bindings, validate all program combinations, and rerun render readback. | Every required program links and renders. |
| `IRIS_DIRECTIVE_INVALID` | An Iris property, directive, target, buffer, or stage contract is invalid. | File, directive, primary documentation, and runtime diagnostic. | Correct against current primary Iris documentation, update the capability matrix, and test in the real harness. | Iris accepts the pack and the documented feature behaves correctly. |
| `UNSUPPORTED_GL_CAPABILITY` | Required GL version, extension, format, or limit is absent. | Context version, extensions, limits, target profile, and requirement. | Use a documented compatible fallback, gate the feature by profile, or keep it pending; never invoke unsupported behavior. | All enabled paths use supported capabilities and pass. |
| `RENDER_OUTPUT_INVALID` | Rendering completes but output is blank, corrupt, dimensionally wrong, or semantically invalid. | Input scene, buffers, readback, expected invariants, and image statistics. | Trace pipeline stages, validate attachments and transforms, repair, and add deterministic readback assertions. | Render output satisfies numeric and visual invariants. |
| `RENDER_NAN_OR_INF` | Shader output or intermediate buffers contain NaN or infinity. | Stage, buffer, pixel samples, inputs, and reproducer. | Guard domains and divisions, stabilize temporal state, add finite-value checks, and rerun representative scenes. | No required buffer contains non-finite values. |
| `VISUAL_REGRESSION` | Output changes outside approved tolerances. | Baseline and candidate images, metrics, scene, profile, and intentional-change evidence. | Determine intended versus defect, repair the pipeline or update baseline only with justified acceptance evidence. | Required scenes pass approved visual thresholds. |
| `PERFORMANCE_REGRESSION` | CPU, GPU, memory, frame time, or compilation cost exceeds budget. | Baseline, candidate metrics, hardware/profile, variance, and workload. | Profile, remove the regression, tune scalable paths, and rerun statistically meaningful benchmarks. | Budgets pass without violating visual or stability criteria. |
| `DRIVER_OR_GAME_CRASH` | The driver, game, JVM, or host resets, hangs, or crashes during validation. | Crash log, driver and hardware, minimal case, workload, and safety data. | Stop unsafe repetition, minimize the case, disable only the proven hazardous path, implement a safe fallback, and validate on supported environments. | Required validation completes without instability. |
| `COMPATIBILITY_MATRIX_STALE` | Version or capability evidence no longer matches current supported components. | Matrix row, cited source, observed versions, and date. | Revalidate with primary sources, update constraints and roadmap links, and rerun affected compatibility tests. | Matrix and implementation describe the same verified support set. |
| `ROADMAP_STATE_CONFLICT` | Roadmap state disagrees with main, PR, CI, or evidence. | Item, claimed state, actual refs, checks, and acceptance criteria. | Reconcile to observed reality, downgrade unsupported completion, and preserve links to evidence. | Roadmap state is justified by current remote evidence. |
| `ROADMAP_DEPENDENCY_CYCLE` | Roadmap items form a dependency cycle that prevents selection. | Cycle path and affected acceptance criteria. | Break the cycle by extracting a foundation unit or correcting invalid dependencies, then revalidate ordering. | At least one coherent executable unit is unblocked. |
| `ACCEPTANCE_EVIDENCE_STALE` | Tests, benchmarks, docs, or screenshots no longer apply to the current head. | Evidence SHA, current head, changed paths, and invalidation analysis. | Rerun or regenerate every invalidated proof and update links. | Acceptance evidence targets the exact final head. |
| `RELEASE_ASSET_FAILED` | Release packaging, upload, checksum, or attachment fails. | Release/tag, asset, checksum, logs, and expected contents. | Repair packaging or upload, verify reproducibility and checksums, and never publish a partial misleading release. | All required assets and metadata are present and validated. |
| `RELEASE_ALREADY_EXISTS` | A tag or release conflicts with the intended version. | Existing tag/release, target commit, assets, and version policy. | Reconcile whether it is identical, superseded, or erroneous; update only through authorized non-destructive release policy. | One canonical release maps to the intended validated commit. |
| `SECRET_OR_TOKEN_DETECTED` | A secret, token, credential, or private value appears in controlled content or logs. | Sanitized location, detector output, exposure scope, and introducing commit. | Stop publication, remove from tree and reachable history using the authorized sanitation path, rotate externally when required, and add prevention checks. | No secret remains in controlled refs or artifacts and required rotation is confirmed. |
| `SENSITIVE_LOG_DETECTED` | Logs or artifacts expose private operational or user data. | Sanitized path, fields, retention, and access scope. | Redact or regenerate artifacts, minimize logging, remove reachable copies when authorized, and validate privacy guards. | Controlled outputs contain only necessary neutral data. |
| `SCOPE_ESCAPE_ATTEMPT` | A proposed operation would mutate an unauthorized repository, secret, protection, or external system. | Requested operation and active authorization envelope. | Reject that path, choose an in-scope technical alternative, and continue the original goal when possible. | The goal proceeds entirely within authorized scope or becomes an exact external authorization request. |
| `UNCLASSIFIED_INTERNAL_FAILURE` | An observed failure does not match a known code. | Minimal reproducer, operation, remote state, logs, inputs, outputs, and hypothesis. | Run `AUTONOMOUS_RECOVERY_LOOP`: isolate, test, repair, validate, reclassify or add a new catalog code, then resume the original task. Do not ask the user for diagnosis. | The cause is fixed and classified, or a recoverable checkpoint exists for the next execution. |
| `EXTERNAL_BLOCKER` | Every authorized internal route is exhausted and one exact external capability is indispensable. | Attempted recovery ladder, checkpoint, missing permission, credential, legal decision, physical access, or mandatory service. | Preserve all work and request only the minimal external capability; do not ask for technical decisions already derivable. | The exact capability becomes available and the same task resumes. |

Result mapping: `NO-OP` is limited to `ACTIVE_RUN`, `PROJECT_ALREADY_COMPLETE`, `NO_AUTHORIZED_WORK`, `ALL_REMAINING_WORK_EXTERNALLY_BLOCKED`, or `LATE_ACQUIRE_ORPHANED`; an internal implementable deficiency, selection failure, or unknown failure enters `AUTONOMOUS_RECOVERY_LOOP`; preserved incomplete work is `PARTIAL`; only a proven `EXTERNAL_BLOCKER` or irrecoverable coordination condition after the full ladder is `BLOCKED`. Every recovery must be followed by a fresh remote-state read before resuming.
<!-- focal-autonomous-blockers:end -->

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
