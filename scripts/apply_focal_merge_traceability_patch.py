#!/usr/bin/env python3
"""Apply the one-time Focal merge PR traceability prompt migration."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one anchor in {path}, found {count}: {old[:120]!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def commit(path: str, message: str) -> None:
    run("git", "add", "--", path)
    run("git", "commit", "-m", message)


def main() -> int:
    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")

    replace_once(
        "prompts/focal/02-autonomy-and-scope.md",
        """- No uses squash como requisito universal; elegí un método de merge compatible con la política del repositorio y la trazabilidad necesaria.\n- Verificá el head exacto antes de mergear.\n""",
        """- No uses squash como requisito universal; elegí un método de merge compatible con la política del repositorio y la trazabilidad necesaria.\n- La historia visible de la rama predeterminada debe conservar la referencia al pull request que produjo cada merge.\n- Preferí el título automático de GitHub. Si la operación envía `commit_title` o cualquier título personalizado, el subject debe contener el número exacto del PR: usá `<título de la PR> (#<n>)` para squash o `Merge pull request #<n> from <head>` para merge commit.\n- No uses rebase merge cuando elimine la referencia visible `#<n>` del historial de la rama predeterminada.\n- Un título personalizado sin el número exacto del PR es inválido aunque GitHub conserve una asociación interna entre la PR y el commit.\n- Verificá el head exacto antes de mergear.\n- Después del merge, verificá conjuntamente `merged == true`, `merge_commit_sha`, el SHA observado en la rama predeterminada y que el subject del commit contenga `#<n>`.\n- Si falta la referencia visible, clasificá `MERGE_PR_REFERENCE_MISSING`; no reescribas historia publicada para maquillarlo ni declares `PASS`.\n""",
    )
    commit("prompts/focal/02-autonomy-and-scope.md", "Require visible PR references in Focal Git policy")

    replace_once(
        "prompts/focal/01-operating-cycle.md",
        """1. Ejecutá el plan de validación de `07-validation-and-acceptance.md`.\n2. Revisá el diff completo y las referencias.\n3. Abrí o actualizá una pull request con alcance, motivación, pruebas, riesgos y estado del roadmap.\n4. Inspeccioná checks del head exacto.\n5. Corregí fallos causados por el cambio cuando el tiempo lo permita.\n6. Mergeá autónomamente solo si todos los gates aplicables están aprobados, el head no cambió y no existe bloqueo de revisión.\n7. Si CI continúa o una prueba obligatoria falta, dejá la PR y el checkpoint remotos; no marques el trabajo como completado.\n""",
        """1. Ejecutá el plan de validación de `07-validation-and-acceptance.md`.\n2. Revisá el diff completo y las referencias.\n3. Abrí o actualizá una pull request con alcance, motivación, pruebas, riesgos y estado del roadmap.\n4. Inspeccioná checks del head exacto.\n5. Corregí fallos causados por el cambio cuando el tiempo lo permita.\n6. Antes del merge, resolvé el número exacto de la PR, el método de merge y el subject final esperado.\n7. Aplicá `MERGE_TITLE_POLICY`: preferí el título automático de GitHub; si la operación envía `commit_title` o un título personalizado, debe contener el PR exacto mediante `<título de la PR> (#<n>)` para squash o `Merge pull request #<n> from <head>` para merge commit.\n8. No uses rebase merge cuando el resultado no conserve `#<n>` de forma visible en el historial de la rama predeterminada.\n9. Rechazá antes de ejecutar cualquier payload de merge cuyo título personalizado no contenga el número exacto del PR.\n10. Mergeá autónomamente solo si todos los gates aplicables están aprobados, el head no cambió y no existe bloqueo de revisión.\n11. Después del merge, releé la PR, el commit y la rama predeterminada; confirmá `merged == true`, `merge_commit_sha`, el SHA incorporado y que el subject visible contenga `#<n>`.\n12. Si falla esa verificación, clasificá `MERGE_PR_REFERENCE_MISSING`, no reescribas historia publicada y no declares `PASS`; repará el procedimiento de merge para las operaciones siguientes y reportá el defecto factual.\n13. Si CI continúa o una prueba obligatoria falta, dejá la PR y el checkpoint remotos; no marques el trabajo como completado.\n""",
    )
    commit("prompts/focal/01-operating-cycle.md", "Enforce PR-numbered merge titles in Focal cycles")

    replace_once(
        "prompts/focal/07-validation-and-acceptance.md",
        """- estado remoto, base y head exactos;\n- diff y referencias internas;\n""",
        """- estado remoto, base y head exactos;\n- trazabilidad visible del PR en el subject final de merge o squash;\n- diff y referencias internas;\n""",
    )
    replace_once(
        "prompts/focal/07-validation-and-acceptance.md",
        """- la lease sigue siendo propia;\n- el head revisado no cambió;\n- la base sigue siendo válida o fue reconciliada;\n""",
        """- la lease sigue siendo propia;\n- el head revisado no cambió;\n- la base sigue siendo válida o fue reconciliada;\n- el número exacto del PR y el subject final del merge están resueltos antes de mutar;\n- el subject automático o personalizado conservará `#<n>` de forma visible; cuando exista `commit_title` personalizado, termina en `(#<n>)` o usa el título nativo `Merge pull request #<n> from <head>`;\n- no se eligió rebase merge si ese método elimina la referencia visible al PR;\n""",
    )
    replace_once(
        "prompts/focal/07-validation-and-acceptance.md",
        """No mergees para fabricar evidencia.\n""",
        """No mergees para fabricar evidencia.\n\n`MERGE_TITLE_POLICY` es un gate previo, no una corrección posterior. Rechazá un payload personalizado sin el PR exacto. Después del merge verificá la PR, `merge_commit_sha`, la rama predeterminada y el subject del commit. Si el subject no contiene `#<n>`, usá `MERGE_PR_REFERENCE_MISSING`, no reescribas la historia publicada y el ciclo no puede ser `PASS`.\n""",
    )
    commit("prompts/focal/07-validation-and-acceptance.md", "Gate Focal merge acceptance on visible PR references")

    replace_once(
        "prompts/focal/08-terminal-report.md",
        """| **PR / merge** | <link a PR y link al commit de merge, o no aplicable> |\n""",
        """| **PR / merge** | <link a PR, link al commit de merge y subject exacto que contiene `#<n>`, o no aplicable> |\n""",
    )
    replace_once(
        "prompts/focal/08-terminal-report.md",
        """| **Estado del merge** | <estado y link Markdown al commit de merge> |\n| **Estado de CI** | <link Markdown al workflow/run y conclusión> |\n""",
        """| **Estado del merge** | <estado y link Markdown al commit de merge> |\n| **Título del merge** | <subject exacto observado> |\n| **Referencia visible al PR** | <verificada: `#<n>` o defecto `MERGE_PR_REFERENCE_MISSING`> |\n| **Estado de CI** | <link Markdown al workflow/run y conclusión> |\n""",
    )
    replace_once(
        "prompts/focal/08-terminal-report.md",
        """- No declares que un archivo, prueba o merge existe si no fue observado remotamente.\n""",
        """- No declares que un archivo, prueba o merge existe si no fue observado remotamente.\n- No declares `PASS` si el subject del commit de merge o squash no contiene el número exacto del PR; mostrale al usuario `MERGE_PR_REFERENCE_MISSING` sin sugerir una reescritura retrospectiva de `main`.\n""",
    )
    commit("prompts/focal/08-terminal-report.md", "Report visible PR references for Focal merges")

    replace_once(
        "prompts/focal/12-autonomous-error-recovery.md",
        """`NO_VALID_UNIT`, `NO_BOUNDED_INCREMENT`, “no se encontró un incremento seguro” y equivalentes quedan retirados como causas terminales: son aliases de `ROADMAP_GRANULARITY_FAILURE`.\n\n## Clasificación de archivos basura generados por error\n""",
        """`NO_VALID_UNIT`, `NO_BOUNDED_INCREMENT`, “no se encontró un incremento seguro” y equivalentes quedan retirados como causas terminales: son aliases de `ROADMAP_GRANULARITY_FAILURE`.\n\n## Trazabilidad visible de merges\n\n- `MERGE_PR_REFERENCE_MISSING`: la PR figura mergeada, pero el subject publicado en la rama predeterminada no contiene su número exacto. Antes del merge, corregí `MERGE_TITLE_POLICY` y el payload: preferí el título automático de GitHub o usá un `commit_title` con `<título de la PR> (#<n>)` o `Merge pull request #<n> from <head>`.\n- Si el defecto se detecta después del merge, no reescribas historia publicada ni crees un commit vacío para simular asociación. Conservá PR, SHA y evidencia, repará el procedimiento o tooling de merge mediante `RECOVERY_REPAIR_IN_PLACE`, verificá la regla con una prueba de regresión y no declares `PASS` para ese ciclo.\n- Una asociación interna de GitHub o un `merge_commit_sha` correcto no sustituye la referencia visible `#<n>` exigida en el historial.\n\n## Clasificación de archivos basura generados por error\n""",
    )
    commit("prompts/focal/12-autonomous-error-recovery.md", "Catalog missing PR references after merge")

    replace_once(
        "prompts/focal/09-skills-maintenance.md",
        """10. Actualizá todas las referencias, el manifest, la integridad, el flowchart, los validadores y la sección de troubleshooting del README, incluidos los contratos de granularidad adaptativa, commits, calidad y presentación del reporte terminal.\n""",
        """10. Actualizá todas las referencias, el manifest, la integridad, el flowchart, los validadores y la sección de troubleshooting del README, incluidos los contratos de granularidad adaptativa, commits, calidad, `MERGE_TITLE_POLICY`, referencia visible al PR y presentación del reporte terminal.\n""",
    )
    replace_once(
        "prompts/focal/09-skills-maintenance.md",
        """- En bulk de bajo riesgo, un commit dedicado por archivo; en alto impacto, commits lógicos multarchivo cuando la atomicidad lo requiera.\n- Checkpoints exclusivamente contingentes y `PARTIAL` limitado a causas objetivas.\n""",
        """- En bulk de bajo riesgo, un commit dedicado por archivo; en alto impacto, commits lógicos multarchivo cuando la atomicidad lo requiera.\n- Todo merge autónomo conserva el PR en el historial visible: título automático de GitHub o título personalizado con `#<n>`; si existe `commit_title`, usá `<título de la PR> (#<n>)` o `Merge pull request #<n> from <head>`.\n- No uses rebase merge cuando elimine esa referencia visible y verificá el subject publicado después del merge.\n- Checkpoints exclusivamente contingentes y `PARTIAL` limitado a causas objetivas.\n""",
    )
    replace_once(
        "prompts/focal/09-skills-maintenance.md",
        """- un commit dedicado por archivo para bulk de bajo riesgo y commits lógicos atómicos para incrementos importantes;\n- prohibición de checkpoints planificados y de `PARTIAL` sin causa objetiva;\n""",
        """- un commit dedicado por archivo para bulk de bajo riesgo y commits lógicos atómicos para incrementos importantes;\n- `MERGE_TITLE_POLICY`, referencia visible `#<n>` en el subject final, rechazo de `commit_title` sin PR y recuperación `MERGE_PR_REFERENCE_MISSING`;\n- prohibición de checkpoints planificados y de `PARTIAL` sin causa objetiva;\n""",
    )
    replace_once(
        "prompts/focal/09-skills-maintenance.md",
        """- validaciones;\n- riesgos de migración.\n""",
        """- validaciones;\n- política de título de merge y referencia visible al PR;\n- riesgos de migración.\n""",
    )
    commit("prompts/focal/09-skills-maintenance.md", "Require PR traceability in prompt maintenance")

    replace_once(
        "prompts/focal/11-process-flowchart.md",
        """        SM9 -- No --> SM10[Corregir fallos causados] --> SM6\n        SM9 -- Sí --> SM11[Mergear y verificar main]\n        SM11 --> REPORT_SKILLS[Reporte terminal único]\n""",
        """        SM9 -- No --> SM10[Corregir fallos causados] --> SM6\n        SM9 -- Sí --> SM_MERGE_TITLE[MERGE_TITLE_POLICY: título automático o personalizado con número exacto de PR]\n        SM_MERGE_TITLE --> SM11[Mergear y verificar main]\n        SM11 --> SM_MERGE_REFERENCE{¿Subject publicado contiene #n y coincide con la PR?}\n        SM_MERGE_REFERENCE -- No --> SM_MERGE_REFERENCE_MISSING[MERGE_PR_REFERENCE_MISSING: no reescribir historia; reparar procedimiento] --> ERROR_CAPTURE\n        SM_MERGE_REFERENCE -- Sí --> REPORT_SKILLS[Reporte terminal único]\n""",
    )
    replace_once(
        "prompts/focal/11-process-flowchart.md",
        """        CI_RESULT -- Sí --> MERGE_GUARD[Releer issue y verificar head]\n        MERGE_GUARD --> MERGE_OK{¿Propiedad y gates válidos?}\n        MERGE_OK -- No --> LOST\n        MERGE_OK -- Sí --> MERGE[Merge autónomo]\n        MERGE --> POST_MERGE[Verificar main y CI post-merge]\n        POST_MERGE --> RECONCILE\n""",
        """        CI_RESULT -- Sí --> MERGE_GUARD[Releer issue y verificar head]\n        MERGE_GUARD --> MERGE_OK{¿Propiedad y gates válidos?}\n        MERGE_OK -- No --> LOST\n        MERGE_OK -- Sí --> MERGE_TITLE_POLICY[Resolver PR, método y subject: automático o commit_title con #n]\n        MERGE_TITLE_POLICY --> MERGE_TITLE_CHECK{¿El subject esperado conserva el PR exacto?}\n        MERGE_TITLE_CHECK -- No --> MERGE_PR_REFERENCE_MISSING[MERGE_PR_REFERENCE_MISSING: corregir antes de merge] --> ERROR_CAPTURE\n        MERGE_TITLE_CHECK -- Sí --> MERGE[Merge autónomo]\n        MERGE --> MERGE_PR_REFERENCE{¿PR mergeada, merge_commit_sha correcto y subject contiene #n?}\n        MERGE_PR_REFERENCE -- No --> MERGE_PR_REFERENCE_MISSING\n        MERGE_PR_REFERENCE -- Sí --> POST_MERGE[Verificar main y CI post-merge]\n        POST_MERGE --> RECONCILE\n""",
    )
    replace_once(
        "prompts/focal/11-process-flowchart.md",
        """- Los commits funcionales ordinarios permanecen sujetos a rama, PR, CI y merge. En `LOW_RISK_BULK` cada archivo usa un commit dedicado; en `HIGH_IMPACT_INCREMENT` los commits pueden abarcar archivos relacionados para preservar atomicidad e intención.\n""",
        """- Los commits funcionales ordinarios permanecen sujetos a rama, PR, CI y merge. En `LOW_RISK_BULK` cada archivo usa un commit dedicado; en `HIGH_IMPACT_INCREMENT` los commits pueden abarcar archivos relacionados para preservar atomicidad e intención.\n- `MERGE_TITLE_POLICY` exige que el historial visible conserve `#<n>`: se prefiere el título automático de GitHub y todo `commit_title` personalizado debe incluir el PR exacto; después del merge se verifica PR, `merge_commit_sha`, main y subject.\n""",
    )
    commit("prompts/focal/11-process-flowchart.md", "Diagram visible PR traceability gates")

    replace_once(
        "README.md",
        """A checkpoint is only a recovery mechanism for an objective contingency; it is never a planned deliverable. A following cycle resumes the same partial unit first, and a second consecutive `PARTIAL` requires new objective evidence. Quality gates reject filler code, placeholders, falsely complete stubs, dead code, avoidable duplication, speculative abstractions, silent fallbacks, untracked TODOs, opportunistic refactors, and tests that merely mirror implementation shape.\n\n<!-- focal-autonomous-blockers:start -->\n""",
        """A checkpoint is only a recovery mechanism for an objective contingency; it is never a planned deliverable. A following cycle resumes the same partial unit first, and a second consecutive `PARTIAL` requires new objective evidence. Quality gates reject filler code, placeholders, falsely complete stubs, dead code, avoidable duplication, speculative abstractions, silent fallbacks, untracked TODOs, opportunistic refactors, and tests that merely mirror implementation shape.\n\nEvery autonomous merge preserves visible pull-request traceability in the default-branch history. The process prefers GitHub's automatic title; any custom `commit_title` contains the exact PR as `<PR title> (#<n>)` or `Merge pull request #<n> from <head>`. Rebase merge is rejected when it removes the visible `#<n>`, and post-merge verification checks the PR, `merge_commit_sha`, default-branch SHA, and published subject.\n\n<!-- focal-autonomous-blockers:start -->\n""",
    )
    replace_once(
        "README.md",
        """| `MERGE_BLOCKED` | Required checks, review, permissions, branch policy, or head verification prevents merge. | PR number, head SHA, mergeability, reviews, and checks. | Correct actionable causes or leave a `PARTIAL` PR; never bypass required gates. | The exact head satisfies every merge gate. |\n| `RELEASE_NOT_PROCESSED` | The final release command does not correlate. | Release command ID, polling timeline, state, and coordinator run. | After release, perform no new mutation; continue read-only polling and report incomplete confirmation. | State shows idle, null run ID, own `lastRunId`, and `LEASE_RELEASED`. |\n""",
        """| `MERGE_BLOCKED` | Required checks, review, permissions, branch policy, or head verification prevents merge. | PR number, head SHA, mergeability, reviews, and checks. | Correct actionable causes or leave a `PARTIAL` PR; never bypass required gates. | The exact head satisfies every merge gate. |\n| `MERGE_PR_REFERENCE_MISSING` | A merged PR's published commit subject does not contain its exact `#<n>`, so the default-branch history looks like an unrelated normal commit. | PR number, `merged` state, `merge_commit_sha`, default-branch SHA, exact commit subject, merge method, and submitted `commit_title` when available. | Before merge, reject the payload and use GitHub's automatic title or a custom title ending in `(#<n>)`; after publication, do not rewrite history or add an empty linking commit—repair the merge procedure and report the traceability defect. | Future merges pass the pre-merge title gate and post-merge subject verification; the affected cycle is not reported as `PASS`. |\n| `RELEASE_NOT_PROCESSED` | The final release command does not correlate. | Release command ID, polling timeline, state, and coordinator run. | After release, perform no new mutation; continue read-only polling and report incomplete confirmation. | State shows idle, null run ID, own `lastRunId`, and `LEASE_RELEASED`. |\n""",
    )
    commit("README.md", "Document Focal merge PR traceability")

    replace_once(
        "scripts/validate_focal_prompt_stack.py",
        """    \"Run de Actions\",\n    \"Workflow:\",\n)\n""",
        """    \"Run de Actions\",\n    \"Workflow:\",\n    \"MERGE_TITLE_POLICY\",\n    \"MERGE_PR_REFERENCE_MISSING\",\n    \"commit_title\",\n    \"(#<n>)\",\n    \"referencia visible al PR\",\n)\n""",
    )
    replace_once(
        "scripts/validate_focal_prompt_stack.py",
        """    \"ROADMAP_GRANULARITY_FAILURE\",\n)\n""",
        """    \"ROADMAP_GRANULARITY_FAILURE\",\n    \"MERGE_TITLE_POLICY\",\n    \"MERGE_PR_REFERENCE\",\n    \"MERGE_PR_REFERENCE_MISSING\",\n    \"SM_MERGE_TITLE\",\n    \"SM_MERGE_REFERENCE\",\n)\n""",
    )
    replace_once(
        "scripts/validate_focal_prompt_stack.py",
        """        \"COORDINATOR_STATUS_STALE_REPORT\",\n    )\n""",
        """        \"COORDINATOR_STATUS_STALE_REPORT\",\n        \"MERGE_PR_REFERENCE_MISSING\",\n    )\n""",
    )
    replace_once(
        "scripts/validate_focal_prompt_stack.py",
        """    if combined.count(\"WORK_SELECTION_PROOF\") < 6:\n        fail(errors, \"mandatory work-selection proof is not reinforced across the prompt stack\")\n""",
        """    if combined.count(\"WORK_SELECTION_PROOF\") < 6:\n        fail(errors, \"mandatory work-selection proof is not reinforced across the prompt stack\")\n    if combined.count(\"MERGE_TITLE_POLICY\") < 4:\n        fail(errors, \"merge title policy is not reinforced across the prompt stack\")\n    if combined.count(\"MERGE_PR_REFERENCE_MISSING\") < 6:\n        fail(errors, \"missing PR reference recovery is not reinforced across the prompt stack\")\n    if \"Preferí el título automático de GitHub\" not in autonomy:\n        fail(errors, \"Git policy does not prefer GitHub's automatic PR-aware merge title\")\n    if \"No uses rebase merge\" not in autonomy:\n        fail(errors, \"Git policy does not reject rebase merges that erase visible PR traceability\")\n    if \"Referencia visible al PR\" not in terminal:\n        fail(errors, \"terminal report does not expose visible PR merge traceability\")\n""",
    )
    commit("scripts/validate_focal_prompt_stack.py", "Validate visible PR merge traceability contracts")

    run("git", "fetch", "origin", "main", "--depth=1")
    run("git", "checkout", "origin/main", "--", ".github/workflows/focal-prompt-validation.yml")
    (ROOT / "scripts/apply_focal_merge_traceability_patch.py").unlink()
    run("git", "add", "--", ".github/workflows/focal-prompt-validation.yml", "scripts/apply_focal_merge_traceability_patch.py")
    run("git", "commit", "-m", "Remove temporary merge traceability migration transport")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
