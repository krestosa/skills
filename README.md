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


<!-- focal-autonomous-blockers:start -->
## Focal autonomous work blockers

This matrix covers every blocking class defined by the active Focal prompt stack. An unexpected condition must be classified under `REMOTE_STATE_AMBIGUOUS`, `EXTERNAL_BLOCKER`, or `UNSAFE_OPERATION`; the process must not invent a new success path.

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
| `ACTIVE_LEASE` | Another run owns a future lease. | Run ID, phase, heartbeat, and expiry. | Return `NO-OP`; do not inspect functional work, wait, cancel, overwrite, or release it. | A later independent execution observes idle or a safely expired lease. |
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
| `NO_VALID_WORK` | No executable roadmap unit remains or only speculative work lacks acceptance criteria. | Audited roadmap and matrix. | Reconcile documents and finish without inventing scope. | A concrete unit with dependencies and acceptance exists. |

Result mapping: an active foreign lease is `NO-OP`; an internal implementable deficiency is `INTERNAL_WORK_REQUIRED`; preserved incomplete work is `PARTIAL`; only a genuine external or unrecoverable coordination condition is `BLOCKED`. Every recovery must be followed by a fresh remote-state read before resuming.
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
