#!/usr/bin/env python3
"""Validate the active Focal autonomous prompt stack."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ENTRYPOINT = Path("prompts/focal-autonomous-development.md")
OPERATING_CYCLE = Path("prompts/focal/01-operating-cycle.md")
COORDINATION = Path("prompts/focal/03-coordination.md")
REQUIRED_MODULES = (
    OPERATING_CYCLE,
    Path("prompts/focal/02-autonomy-and-scope.md"),
    COORDINATION,
    Path("prompts/focal/04-roadmap.md"),
    Path("prompts/focal/05-iris-capability-research.md"),
    Path("prompts/focal/06-technical-requirements.md"),
    Path("prompts/focal/07-validation-and-acceptance.md"),
    Path("prompts/focal/08-terminal-report.md"),
    Path("prompts/focal/09-skills-maintenance.md"),
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
    "Si el issue permanece `idle`",
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
    "Resultado: PASS | PARTIAL | BLOCKED | NO-OP",
)
FORBIDDEN_ACTIVE_PATTERNS = (
    r"Ref:\s*[0-9a-f]{40}",
    r"automation/run-state\.json",
    r"rama\s+`automation/runtime-state`",
    r"issue\s+#2",
    r"issue\s+#5",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    repo = Path.cwd()
    errors: list[str] = []

    required_paths = (ENTRYPOINT,) + REQUIRED_MODULES
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

    texts = {path: (repo / path).read_text(encoding="utf-8") for path in required_paths}
    entry = texts[ENTRYPOINT]
    operating = texts[OPERATING_CYCLE]
    coordination = texts[COORDINATION]

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
    )
    for required in coordination_requirements:
        if required not in coordination:
            fail(errors, f"coordination boundary missing: {required}")

    active_without_coordination = "\n".join(
        text for path, text in texts.items() if path != COORDINATION
    )
    for pattern in FORBIDDEN_ACTIVE_PATTERNS:
        if re.search(pattern, active_without_coordination, flags=re.IGNORECASE):
            fail(errors, f"forbidden active legacy reference outside coordination: {pattern}")

    references = set()
    for text in texts.values():
        references.update(
            match
            for match in re.findall(r"`(prompts/focal/[^`]+\.md)`", text)
        )
    missing_refs = sorted(ref for ref in references if not (repo / ref).is_file())
    for ref in missing_refs:
        fail(errors, f"broken prompt reference: {ref}")

    if combined.count("ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT") < 2:
        fail(errors, "initial roadmap phase is not defined and invoked")
    if combined.count("ROADMAP_RECONCILIATION") < 2:
        fail(errors, "final roadmap phase is not defined and invoked")
    if combined.count("OPENGL_RUNTIME_HARNESS") < 3:
        fail(errors, "OpenGL runtime harness is not defined across roadmap, technical and validation contracts")
    if combined.count("https://shaders.properties/current/reference/") < 2:
        fail(errors, "official Iris documentation links are not required across roadmap and research contracts")
    if combined.count("status == working") < 4:
        fail(errors, "working-state ownership is not reinforced across the prompt stack")
    if combined.count("última mutación") + combined.count("ÚLTIMA mutación") < 4:
        fail(errors, "final release boundary is not reinforced across the prompt stack")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(required_paths)} active Focal prompt files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
