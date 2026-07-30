#!/usr/bin/env python3
"""Validate the active Focal autonomous prompt stack."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ENTRYPOINT = Path("prompts/focal-autonomous-development.md")
OPERATING_CYCLE = Path("prompts/focal/01-operating-cycle.md")
AUTONOMY = Path("prompts/focal/02-autonomy-and-scope.md")
COORDINATION = Path("prompts/focal/03-coordination.md")
ROADMAP = Path("prompts/focal/04-roadmap.md")
ACCEPTANCE = Path("prompts/focal/07-validation-and-acceptance.md")
TERMINAL_REPORT = Path("prompts/focal/08-terminal-report.md")
MAINTENANCE = Path("prompts/focal/09-skills-maintenance.md")
COORDINATOR_REPAIR = Path("prompts/focal/10-coordinator-repair.md")
ERROR_RECOVERY = Path("prompts/focal/12-autonomous-error-recovery.md")
FLOWCHART = Path("prompts/focal/11-process-flowchart.md")
README = Path("README.md")
REQUIRED_MODULES = (
    OPERATING_CYCLE,
    AUTONOMY,
    COORDINATION,
    ROADMAP,
    Path("prompts/focal/05-iris-capability-research.md"),
    Path("prompts/focal/06-technical-requirements.md"),
    ACCEPTANCE,
    TERMINAL_REPORT,
    MAINTENANCE,
    COORDINATOR_REPAIR,
    ERROR_RECOVERY,
    FLOWCHART,
)
RETIRED_ACTIVE_FILES = (
    Path("prompts/focal-autonomous-development.base.md"),
    Path("prompts/focal-autonomous-development.autonomy.md"),
    Path("prompts/focal-autonomous-development.state.md"),
)
REQUIRED_TEXT = (
    "ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT",
    "ROADMAP_RECONCILIATION",
    "docs/ROADMAP.md",
    "docs/IRIS-CAPABILITY-MATRIX.md",
    "- [ ] ⚪ PENDIENTE",
    "- [ ] 🟡 EN PROGRESO",
    "- [x] 🟢 COMPLETADO",
    "- [ ] 🟣 REVALIDAR",
    "- [ ] 🔴 BLOQUEADO",
    "Issue: #7",
    "focal-command:v3",
    "focal-state:v3",
    "PRIMERA lectura remota de `krestosa/Focal`",
    "ÚLTIMA mutación remota del ciclo",
    "status == working",
    "runId` propio",
    "HEARTBEAT_ACCEPTED",
    "Antes de cada mutación",
    "cleanup_branches` no forma parte de un ciclo de desarrollo",
    "OPENGL_RUNTIME_HARNESS",
    "focal-gl probe",
    "focal-gl compile",
    "focal-gl render",
    "focal-gl suite",
    "GL_RENDER_READBACK",
    "campo `Iris docs`",
    "https://shaders.properties/current/reference/",
    "# ✅ PASS —",
    "# 🟡 PARTIAL —",
    "# 🔴 BLOCKED —",
    "# ⚪ NO-OP —",
    "## Cambios principales",
    "## Validación",
    "## Estado del proyecto",
    "## Riesgos y limitaciones",
    "## Próximo paso",
    "## Trazabilidad",
    "Detalles operativos y de recuperación",
    "45 segundos",
    "conector de GitHub o GitHub Actions",
    "commits de reparación alcanzables",
    "prompts/focal/11-process-flowchart.md",
    "Minimización obligatoria de procedencia",
    "Entrega resiliente de comandos",
    "workflow_dispatch",
    "schedule",
    "lease huérfana",
    "Safeguard de fallos transitorios del conector",
    "read-after-write",
    "2, 5, 10 y 20 segundos",
    "CONNECTOR_MUTATION_OUTCOME_UNKNOWN",
    "CONNECTOR_RETRY_EXHAUSTED",
    "Reintentos del conector:",
    "Safeguard de saneamiento histórico sin huellas",
    "NOOP_COMMIT",
    "EMPTY_ARTIFACT_COMMIT",
    "FAILED_TRANSPORT_COMMIT",
    "GIT_AUTHOR_DATE",
    "GIT_COMMITTER_DATE",
    "git commit-tree",
    "refs/heads/*",
    "refs/tags/*",
    "Commit o merge de limpieza presente:",
    "AUTONOMOUS_RECOVERY_LOOP",
    "UNCLASSIFIED_INTERNAL_FAILURE",
    "RECOVERY_REPAIR_IN_PLACE",
    "GARBAGE_ARTIFACT_FILE",
    "PLACEHOLDER_GARBAGE_FILE",
    "TOOL_OUTPUT_ARTIFACT_FILE",
    "ERROR_DUMP_ARTIFACT_FILE",
    "TRUNCATED_GENERATION_ARTIFACT_FILE",
    "WRONG_PATH_ARTIFACT_FILE",
    "GARBAGE_ARTIFACT_COMMIT",
    "GARBAGE_ARTIFACT_MIXED_COMMIT",
    "No pidas al usuario elegir arquitectura",
    "LOW_RISK_BULK",
    "HIGH_IMPACT_INCREMENT",
    "un commit dedicado",
    "incremento vertical",
    "checkpoint no puede ser el objetivo",
    "ciclos consecutivos",
    "código de relleno",
    "WORK_SELECTION_PROOF",
    "ROADMAP_GRANULARITY_FAILURE",
    "WORK_SELECTION_PROOF_MISSING",
    "NOOP_REASON_INVALID",
    "NOOP_REASON_REPEATED",
    "ACTIVE_RUN",
    "PROJECT_ALREADY_COMPLETE",
    "NO_AUTHORIZED_WORK",
    "ALL_REMAINING_WORK_EXTERNALLY_BLOCKED",
    "LATE_ACQUIRE_ORPHANED",
    "Estado observado UTC",
)
FORBIDDEN_ACTIVE_PATTERNS = (
    r"Ref:\s*[0-9a-f]{40}",
    r"automation/run-state\.json",
    r"rama\s+`automation/runtime-state`",
    r"issue\s+#2",
    r"issue\s+#5",
)
FORBIDDEN_OPERATIONAL_PROVENANCE = (
    r'"owner"\s*:',
    r'"executionSource"\s*:',
)
README_MARKERS = (
    "<!-- focal-autonomous-blockers:start -->",
    "<!-- focal-autonomous-blockers:end -->",
    "## Focal autonomous work blockers",
    "Evidence required",
    "Recovery procedure",
    "Resume condition",
    "## Focal adaptive execution granularity",
    "### Focal closed NO-OP contract",
)
FLOWCHART_NODES = (
    "flowchart TD",
    "SKILLS_MAINTENANCE",
    "FOCAL_CYCLE",
    "COORDINATOR_REPAIR",
    "ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT",
    "OPENGL_RUNTIME_HARNESS",
    "ROADMAP_RECONCILIATION",
    "LEASE_ACQUIRED",
    "LEASE_RELEASED",
    "BLOCKED",
    "NO-OP",
    "PARTIAL",
    "PASS",
    "CONNECTOR_RETRY",
    "READ_AFTER_WRITE",
    "RETRY_SAME_OPERATION",
    "CONNECTOR_RETRY_EXHAUSTED",
    "HISTORY_SCAN",
    "HISTORY_CLASSIFY",
    "HISTORY_REPLAY",
    "HISTORY_DATES",
    "HISTORY_FORCE_LEASE",
    "HISTORY_DELETE_REFS",
    "HISTORY_REACHABILITY",
    "AUTONOMOUS_RECOVERY",
    "ERROR_CAPTURE",
    "ERROR_CLASSIFY",
    "ERROR_UNKNOWN",
    "ERROR_ROUTE",
    "ERROR_RESUME",
    "ERROR_CHECKPOINT",
    "UNIT_RISK",
    "LOW_RISK_BULK",
    "HIGH_IMPACT_INCREMENT",
    "QUALITY_GATE",
    "PARTIAL_CAUSE",
    "RESULT_GATE",
    "WORK_SELECTION_PROOF",
    "SLICE_FOUND",
    "DECOMPOSE_VERTICAL",
    "NOOP_CAUSE",
    "ROADMAP_GRANULARITY_FAILURE",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    repo = Path.cwd()
    errors: list[str] = []

    required_paths = (ENTRYPOINT,) + REQUIRED_MODULES + (README,)
    for path in required_paths:
        if not (repo / path).is_file():
            fail(errors, f"missing required file: {path}")

    for path in RETIRED_ACTIVE_FILES:
        if (repo / path).exists():
            fail(errors, f"retired active file still exists: {path}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    prompt_paths = (ENTRYPOINT,) + REQUIRED_MODULES
    texts = {path: (repo / path).read_text(encoding="utf-8") for path in prompt_paths}
    entry = texts[ENTRYPOINT]
    operating = texts[OPERATING_CYCLE]
    autonomy = texts[AUTONOMY]
    coordination = texts[COORDINATION]
    roadmap = texts[ROADMAP]
    acceptance = texts[ACCEPTANCE]
    maintenance = texts[MAINTENANCE]
    repair = texts[COORDINATOR_REPAIR]
    recovery = texts[ERROR_RECOVERY]
    flowchart = texts[FLOWCHART]
    terminal = texts[TERMINAL_REPORT]
    readme = (repo / README).read_text(encoding="utf-8")

    for module in REQUIRED_MODULES:
        if f"`{module.as_posix()}`" not in entry:
            fail(errors, f"entrypoint does not reference: {module}")

    combined = "\n".join(texts.values())
    for required in REQUIRED_TEXT:
        if required not in combined:
            fail(errors, f"missing required contract text: {required}")

    entry_first = entry.find("PRIMERA lectura remota de `krestosa/Focal`")
    entry_roadmap = entry.find("`ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT`")
    if entry_first == -1 or entry_roadmap == -1 or entry_first > entry_roadmap:
        fail(errors, "entrypoint does not place issue acquisition before roadmap work")

    if "La **primera llamada remota contra `krestosa/Focal`**" not in operating:
        fail(errors, "operating cycle does not make issue #7 the first Focal remote call")
    if "Este comando debe ser la **última mutación remota**" not in operating:
        fail(errors, "operating cycle does not make release the final mutation")
    if "Un chat que sigue trabajando mientras el issue está `idle`" not in operating:
        fail(errors, "operating cycle does not stop unleased active chats")

    coordination_requirements = (
        "Nunca edites directamente `focal-state:v3`",
        "Mientras el issue no muestre esos valores, el ciclo sigue sin comenzar",
        "## Guardia previa a cada mutación",
        "Después de enviarlo, no vuelvas a editar el issue ni ningún otro recurso",
        "`cleanup_branches` es una operación administrativa independiente",
        "45 segundos reales",
        "`COORDINATOR_REPAIR`",
        "reenviá exactamente una vez",
        "schedule` cada cinco minutos",
        "workflow_dispatch",
        "No incluyas campos `owner`",
        "OUTCOME_UNKNOWN",
        "read-after-write",
        "cuatro intentos",
    )
    for required in coordination_requirements:
        if required not in coordination:
            fail(errors, f"coordination boundary missing: {required}")

    repair_requirements = (
        "Toda lectura y mutación de `krestosa/Focal`",
        "conector de GitHub",
        "GitHub Actions",
        "dejar en `main` commits",
        "force-with-lease",
        "árbol final validado",
        "autor",
        "committer",
        "workflow temporal",
        "fallback programado",
        "procedencia",
        "NOOP_COMMIT",
        "EMPTY_ARTIFACT_COMMIT",
        "FAILED_TRANSPORT_COMMIT",
        "GIT_AUTHOR_DATE",
        "GIT_COMMITTER_DATE",
        "git commit-tree",
        "refs/heads/*",
        "refs/tags/*",
    )
    for required in repair_requirements:
        if required not in repair:
            fail(errors, f"coordinator repair contract missing: {required}")

    for marker in FLOWCHART_NODES:
        if marker not in flowchart:
            fail(errors, f"flowchart missing required node or state: {marker}")
    recovery_requirements = (
        "AUTONOMOUS_RECOVERY_LOOP",
        "UNCLASSIFIED_INTERNAL_FAILURE",
        "RECOVERY_EXTERNAL_ESCALATION",
        "GARBAGE_ARTIFACT_FILE",
        "PLACEHOLDER_GARBAGE_FILE",
        "GARBAGE_ARTIFACT_MIXED_COMMIT",
        "GIT_AUTHOR_DATE",
        "GIT_COMMITTER_DATE",
        "Nunca se pide al usuario",
    )
    for required in recovery_requirements:
        if required not in recovery:
            fail(errors, f"autonomous recovery contract missing: {required}")

    if flowchart.count("```mermaid") != 1 or flowchart.count("```") < 2:
        fail(errors, "flowchart does not contain exactly one Mermaid block")

    for marker in README_MARKERS:
        if marker not in readme:
            fail(errors, f"README troubleshooting section missing: {marker}")
    blocker_rows = len(re.findall(r"^\| `[^`]+` \|", readme, flags=re.MULTILINE))
    if blocker_rows < 100:
        fail(errors, f"README failure matrix is incomplete: {blocker_rows} rows")
    required_readme_codes = (
        "GARBAGE_ARTIFACT_FILE",
        "PLACEHOLDER_GARBAGE_FILE",
        "TOOL_OUTPUT_ARTIFACT_FILE",
        "ERROR_DUMP_ARTIFACT_FILE",
        "TRUNCATED_GENERATION_ARTIFACT_FILE",
        "WRONG_PATH_ARTIFACT_FILE",
        "GARBAGE_ARTIFACT_MIXED_COMMIT",
        "UNCLASSIFIED_INTERNAL_FAILURE",
        "EXTERNAL_BLOCKER",
        "GLSL_COMPILE_FAILED",
        "SECRET_OR_TOKEN_DETECTED",
        "ROADMAP_GRANULARITY_FAILURE",
        "WORK_SELECTION_PROOF_MISSING",
        "NOOP_REASON_INVALID",
        "NOOP_REASON_REPEATED",
        "COORDINATOR_STATUS_STALE_REPORT",
    )
    for code in required_readme_codes:
        if not re.search(rf"^\| `{re.escape(code)}` \|", readme, flags=re.MULTILINE):
            fail(errors, f"README failure matrix missing code: {code}")

    active_without_coordination = "\n".join(
        text for path, text in texts.items() if path != COORDINATION
    )
    for pattern in FORBIDDEN_ACTIVE_PATTERNS:
        if re.search(pattern, active_without_coordination, flags=re.IGNORECASE):
            fail(errors, f"forbidden active legacy reference outside coordination: {pattern}")

    for pattern in FORBIDDEN_OPERATIONAL_PROVENANCE:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(errors, f"forbidden operational provenance in Focal prompt stack: {pattern}")

    references = set()
    for text in texts.values():
        references.update(
            match for match in re.findall(r"`(prompts/focal/[^`]+\.md)`", text)
        )
    missing_refs = sorted(ref for ref in references if not (repo / ref).is_file())
    for ref in missing_refs:
        fail(errors, f"broken prompt reference: {ref}")

    if combined.count("ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT") < 3:
        fail(errors, "initial roadmap phase is not defined, invoked, and diagrammed")
    if combined.count("ROADMAP_RECONCILIATION") < 3:
        fail(errors, "final roadmap phase is not defined, invoked, and diagrammed")
    if combined.count("OPENGL_RUNTIME_HARNESS") < 4:
        fail(errors, "OpenGL runtime harness is not defined across roadmap, technical, validation, and flowchart contracts")
    if combined.count("https://shaders.properties/current/reference/") < 2:
        fail(errors, "official Iris documentation links are not required across roadmap and research contracts")
    if combined.count("status == working") < 4:
        fail(errors, "working-state ownership is not reinforced across the prompt stack")
    if combined.count("última mutación") + combined.count("ÚLTIMA mutación") < 4:
        fail(errors, "final release boundary is not reinforced across the prompt stack")
    if combined.count("read-after-write") < 5:
        fail(errors, "connector unknown-outcome reconciliation is not reinforced across the prompt stack")
    if combined.count("cuatro intentos") + combined.count("four total attempts") < 3:
        fail(errors, "connector retry budget is not reinforced across the prompt stack")
    if combined.count("NOOP_COMMIT") < 4 or combined.count("EMPTY_ARTIFACT_COMMIT") < 4 or combined.count("FAILED_TRANSPORT_COMMIT") < 4:
        fail(errors, "history artifact classification is not reinforced across the prompt stack")
    if combined.count("GIT_AUTHOR_DATE") < 3 or combined.count("GIT_COMMITTER_DATE") < 3:
        fail(errors, "later-commit timestamp preservation is not reinforced across the prompt stack")
    if combined.count("refs/heads/*") < 3 or combined.count("refs/tags/*") < 3:
        fail(errors, "history sanitation reachability verification is not reinforced")
    if combined.count("AUTONOMOUS_RECOVERY_LOOP") < 4:
        fail(errors, "autonomous recovery loop is not reinforced across the prompt stack")
    if combined.count("UNCLASSIFIED_INTERNAL_FAILURE") < 5:
        fail(errors, "unknown internal failure route is not reinforced")
    if combined.count("GARBAGE_ARTIFACT_MIXED_COMMIT") < 5:
        fail(errors, "mixed-commit garbage sanitation is not reinforced")
    if "solo `X`" not in combined and "por ejemplo `X`" not in combined:
        fail(errors, "placeholder garbage example is not explicitly covered")
    if "mensaje" not in repair or "nunca bastan solos" not in repair:
        fail(errors, "history candidates can be classified without sufficient evidence")
    if combined.count("LOW_RISK_BULK") < 6 or combined.count("HIGH_IMPACT_INCREMENT") < 6:
        fail(errors, "adaptive work-unit lanes are not reinforced across the prompt stack")
    if combined.count("un commit dedicado") < 3:
        fail(errors, "single-file commit discipline for low-risk bulk is not reinforced")
    if combined.count("incremento vertical") < 4:
        fail(errors, "vertical functional decomposition for high-impact work is not reinforced")
    if combined.count("checkpoint") < 10 or "nunca como objetivo planificado" not in combined:
        fail(errors, "checkpoint contingency policy is incomplete")
    if combined.count("código de relleno") < 4:
        fail(errors, "implementation quality safeguards are not reinforced")
    if "segunda ejecución" not in combined and "siguiente ejecución" not in combined:
        fail(errors, "PARTIAL continuity is not enforced")
    if combined.count("WORK_SELECTION_PROOF") < 6:
        fail(errors, "mandatory work-selection proof is not reinforced across the prompt stack")
    if combined.count("ROADMAP_GRANULARITY_FAILURE") < 6:
        fail(errors, "roadmap granularity recovery is not reinforced")
    if "al menos tres candidatos" not in combined:
        fail(errors, "selection proof does not require at least three candidates")
    closed_noop_codes = (
        "ACTIVE_RUN",
        "PROJECT_ALREADY_COMPLETE",
        "NO_AUTHORIZED_WORK",
        "ALL_REMAINING_WORK_EXTERNALLY_BLOCKED",
        "LATE_ACQUIRE_ORPHANED",
    )
    for code in closed_noop_codes:
        if combined.count(code) < 3:
            fail(errors, f"closed NO-OP reason is not reinforced: {code}")
    if "no existía unidad válida" in acceptance:
        fail(errors, "acceptance still allows open-ended NO-OP for missing work units")
    if "no existe una unidad válida de trabajo" in entry:
        fail(errors, "entrypoint still treats missing unit selection as a terminal condition")
    if re.search(r"^\| `NO_VALID_WORK` \|", readme, flags=re.MULTILINE):
        fail(errors, "README still contains retired NO_VALID_WORK terminal classification")
    if "NOOP_REASON_REPEATED" not in roadmap or "NOOP_REASON_REPEATED" not in recovery:
        fail(errors, "consecutive invalid NO-OP recovery is incomplete")
    if "quince minutos reales" not in operating:
        fail(errors, "work selection has no bounded post-lease deadline")
    if "Estado observado UTC" not in terminal:
        fail(errors, "terminal report does not timestamp coordinator state snapshots")

    terminal_sections = (
        "# <icono> <RESULTADO> — <resumen concreto>",
        "## Cambios principales",
        "## Validación",
        "## Estado del proyecto",
        "## Riesgos y limitaciones",
        "## Próximo paso",
        "## Trazabilidad",
        "<details>",
        "Detalles operativos y de recuperación",
    )
    for marker in terminal_sections:
        if marker not in terminal:
            fail(errors, f"terminal report missing readable section: {marker}")
    if "```text" in terminal:
        fail(errors, "terminal report reverted to a flat text block")
    if "Resultado: PASS | PARTIAL | BLOCKED | NO-OP" in terminal:
        fail(errors, "terminal report contains the retired flat result layout")
    heading_positions = [terminal.find(marker) for marker in (
        "# <icono> <RESULTADO> — <resumen concreto>",
        "## Cambios principales",
        "## Validación",
        "## Trazabilidad",
        "<details>",
    )]
    if any(position < 0 for position in heading_positions) or heading_positions != sorted(heading_positions):
        fail(errors, "terminal report does not place summary and validation before traceability details")
    for heading in ("# ✅ PASS —", "# 🟡 PARTIAL —", "# 🔴 BLOCKED —", "# ⚪ NO-OP —"):
        if heading not in terminal:
            fail(errors, f"terminal report missing result heading contract: {heading}")


    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(prompt_paths)} active Focal prompt files and README troubleshooting.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
