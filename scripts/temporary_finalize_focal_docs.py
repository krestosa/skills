#!/usr/bin/env python3
from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"expected text missing in {path}: {old[:80]}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    Path("scripts/validate_focal_prompt_stack.py"),
    '        "no debe conservar commits",',
    '        "dejar en `main` commits",',
)

old_tail = """    LOST --> PARTIAL_LOST[PARTIAL o BLOCKED según exista checkpoint remoto útil] --> RPT0
    LOST_NO_RELEASE --> RPT0
    RELEASE_UNKNOWN --> RPT0
    REPORT --> END([Fin])
    REPORT_SKILLS --> END
    NOOP --> RPT0[Emitir reporte terminal único]
    BLOCKED_PROMPT --> RPT0
    BLOCKED_LOCK --> RPT0
    BLOCKED_COORD --> RPT0
    PARTIAL_CP --> RECONCILE
    RPT0 --> END
"""
new_tail = """    LOST --> EVIDENCE_RESULT{¿Existe checkpoint remoto útil?}
    LOST_NO_RELEASE --> EVIDENCE_RESULT
    RELEASE_UNKNOWN --> EVIDENCE_RESULT
    EVIDENCE_RESULT -- Sí --> PARTIAL_RESULT([PARTIAL])
    EVIDENCE_RESULT -- No --> BLOCKED_RESULT([BLOCKED])
    REPORT --> PASS_RESULT([PASS])
    REPORT_SKILLS --> PASS_RESULT
    NOOP --> NOOP_RESULT([NO-OP])
    BLOCKED_PROMPT --> BLOCKED_RESULT
    BLOCKED_LOCK --> BLOCKED_RESULT
    BLOCKED_COORD --> BLOCKED_RESULT
    PARTIAL_CP --> RECONCILE
    PASS_RESULT --> END([Fin])
    PARTIAL_RESULT --> END
    BLOCKED_RESULT --> END
    NOOP_RESULT --> END
"""
replace_once(Path("prompts/focal/11-process-flowchart.md"), old_tail, new_tail)
