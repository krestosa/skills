#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"missing anchor in {path}: {old[:120]!r}")
    write(path, text.replace(old, new, 1))


ENTRY_SECTION = """## Safeguard de fallos transitorios del conector

Un error aislado del conector no es una condición terminal ni autoriza abandonar la tarea.

1. Clasificá como transitorio un timeout, desconexión, respuesta `429`, error `5xx`, indisponibilidad temporal, fallo de transporte o excepción interna sin rechazo autoritativo de GitHub.
2. Reintentá la misma tarea y la misma operación hasta cuatro intentos totales, con esperas reales de 2, 5, 10 y 20 segundos; respetá `Retry-After` cuando exista y el presupuesto temporal del ciclo.
3. Para una lectura, repetí la misma lectura desde la fuente remota canónica.
4. Para una mutación cuya llamada devolvió error, tratá el resultado como desconocido: ejecutá verificación `read-after-write` antes de decidir si debe repetirse.
5. Si el efecto remoto ya existe, considerá la mutación aplicada y continuá. Si no existe y las guardas siguen vigentes, repetí la misma operación con el mismo payload, `commandId`, SHA esperado o clave de idempotencia; no generes una mutación lógica distinta para compensar un resultado incierto.
6. Mientras se recupera el conector, no avances a una fase que dependa de la operación fallida, no liberes una lease propia por el primer error y no declares `BLOCKED`.
7. Solo podés detener el ciclo después de agotar reintentos, verificación remota y fallbacks autorizados, o cuando ya no quede tiempo seguro para preservar checkpoint, reconciliar y liberar. Clasificá ese caso como `CONNECTOR_RETRY_EXHAUSTED`.
8. Si el proceso de ejecución desaparece por completo y ya no puede hacer llamadas, la siguiente ejecución independiente debe reconstruir y reintentar la misma tarea desde el estado remoto; nunca debe iniciar una unidad funcional paralela.

"""

replace_once(
    "prompts/focal-autonomous-development.md",
    "No cargues versiones históricas de este entrypoint ni módulos retirados. El historial Git es trazabilidad, no una capa ejecutable. `11-process-flowchart.md` es una vista derivada y no puede contradecir a los módulos normativos `01` a `10`.\n\n## Gate cero obligatorio de `FOCAL_CYCLE`",
    "No cargues versiones históricas de este entrypoint ni módulos retirados. El historial Git es trazabilidad, no una capa ejecutable. `11-process-flowchart.md` es una vista derivada y no puede contradecir a los módulos normativos `01` a `10`.\n\n" + ENTRY_SECTION + "## Gate cero obligatorio de `FOCAL_CYCLE`",
)
replace_once(
    "prompts/focal-autonomous-development.md",
    "- el estado remoto necesario es ambiguo después de los fallbacks permitidos;",
    "- el estado remoto necesario es ambiguo después de agotar el safeguard de reintentos y los fallbacks permitidos;",
)

OPERATING_SECTION = """## 1.1 Safeguard transversal del conector

Este protocolo aplica a toda lectura o mutación remota del ciclo, antes y después de adquirir la lease.

1. Un primer error de transporte, timeout, `429`, `5xx`, indisponibilidad temporal o excepción interna no termina el ciclo.
2. Reintentá la misma operación hasta cuatro intentos totales con backoff real de 2, 5, 10 y 20 segundos, respetando `Retry-After` y el hard stop.
3. En lecturas, repetí la consulta contra el mismo repositorio, ref, issue, PR, run o archivo.
4. En mutaciones con respuesta de error, marcá el resultado como desconocido y hacé `read-after-write` sobre el recurso autoritativo.
5. Si el efecto ya está aplicado, continuá sin duplicarlo. Si no está aplicado y la guarda de lease, SHA o head sigue vigente, reintentá la misma mutación con el mismo payload e identificador idempotente.
6. No cambies de `commandId` por un error de transporte. Un `commandId` nuevo corresponde únicamente al reenvío posterior a una escritura confirmada pero no procesada durante la ventana de coordinación.
7. Mientras el conector no permita confirmar propiedad, pausá nuevas mutaciones funcionales, conservá el checkpoint remoto existente y seguí reintentando; no asumas que la lease se perdió ni que la mutación falló.
8. Solo emití `CONNECTOR_RETRY_EXHAUSTED` cuando se agotaron los cuatro intentos, la verificación remota y cualquier fallback aplicable, o cuando el tiempo restante ya no permite un cierre seguro.

"""
replace_once(
    "prompts/focal/01-operating-cycle.md",
    "9. No registres proveedor, modelo, aplicación, cliente, conector, actor ni plataforma de conversación. `runId` y `commandId` son las únicas identidades operativas.\n\n## 2. Adquisición obligatoria antes del análisis",
    "9. No registres proveedor, modelo, aplicación, cliente, conector, actor ni plataforma de conversación. `runId` y `commandId` son las únicas identidades operativas.\n\n" + OPERATING_SECTION + "## 2. Adquisición obligatoria antes del análisis",
)
replace_once(
    "prompts/focal/01-operating-cycle.md",
    "7. Releé el issue en modo solo lectura, con demoras reales, hasta confirmar `idle`, `runId == null`, `lastRunId` propio y `LEASE_RELEASED`, o documentá exactamente por qué no pudo confirmarse.",
    "7. Si la llamada de `release` devuelve error, no asumas que falló: aplicá `read-after-write`; si el mismo `commandId` no aparece y seguís siendo propietario, reintentá únicamente ese mismo `release` bajo el safeguard. Luego releé el issue en modo solo lectura, con demoras reales, hasta confirmar `idle`, `runId == null`, `lastRunId` propio y `LEASE_RELEASED`, o documentá exactamente por qué no pudo confirmarse.",
)

COORDINATION_SECTION = """## Fallos del conector y mutaciones de resultado desconocido

Los errores del canal de herramientas no cambian por sí mismos el estado remoto.

1. Aplicá hasta cuatro intentos totales con backoff de 2, 5, 10 y 20 segundos a timeouts, desconexiones, `429`, `5xx`, indisponibilidad temporal y excepciones internas sin rechazo autoritativo.
2. Una lectura fallida se repite contra la misma fuente canónica; no se sustituye por memoria ni por una copia local.
3. Una mutación que devuelve error queda en estado `OUTCOME_UNKNOWN`. Antes de repetirla, ejecutá `read-after-write` sobre issue, archivo, ref, commit, PR, merge, check o release afectado.
4. Si el efecto remoto coincide con la intención, registrá la operación como aplicada y continuá. Si no coincide y las precondiciones siguen vigentes, reintentá exactamente la misma operación con el mismo payload e identificador idempotente.
5. Para escribir `focal-command:v3`, conservá el mismo `commandId` mientras la propia escritura no esté confirmada. Generá un `commandId` nuevo solo cuando la escritura fue observada pero el coordinador no la procesó durante la ventana definida en Entrega resiliente de comandos.
6. Durante una interrupción no confirmes ni niegues propiedad por inferencia. Pausá mutaciones funcionales y reintentá la lectura del issue hasta recuperar una observación autoritativa o agotar el presupuesto.
7. El primer error no permite liberar la lease, cerrar la PR, descartar la rama ni terminar la tarea. Si el proceso completo desaparece, la siguiente ejecución retoma desde issue, rama, PR y checkpoint remotos.
8. Solo después de agotar reintentos, `read-after-write` y fallbacks aplicables puede clasificarse `CONNECTOR_RETRY_EXHAUSTED`; si existe checkpoint útil, el resultado es `PARTIAL`, no `BLOCKED`.

"""
replace_once(
    "prompts/focal/03-coordination.md",
    "Editar el issue no equivale a adquirir o renovar. Escribir un comando sin observar la respuesta tampoco.\n\n## Preservación del cuerpo",
    "Editar el issue no equivale a adquirir o renovar. Escribir un comando sin observar la respuesta tampoco.\n\n" + COORDINATION_SECTION + "## Preservación del cuerpo",
)

SKILLS_SECTION = """## Safeguard del conector en mantenimiento

`SKILLS_MAINTENANCE` no termina ante el primer fallo del conector.

- Reintentá lecturas y mutaciones transitorias hasta cuatro intentos totales con backoff de 2, 5, 10 y 20 segundos.
- Ante una mutación con respuesta de error, ejecutá `read-after-write` sobre la rama, archivo, commit o PR antes de repetirla.
- Si el efecto existe, continuá; si no existe y el SHA o head esperado sigue vigente, repetí exactamente la misma operación.
- No abras otra rama ni otra PR para compensar una operación de resultado desconocido.
- Solo detené el mantenimiento como `CONNECTOR_RETRY_EXHAUSTED` cuando los reintentos y verificaciones fueron agotados o el presupuesto ya no permite validar y publicar con seguridad.
- Una ejecución posterior debe retomar la misma rama o PR remota incompleta en vez de duplicar el trabajo.

"""
replace_once(
    "prompts/focal/09-skills-maintenance.md",
    "- no se heredan permisos de merge, release o mantenimiento hacia otros repositorios.\n\n## Procedimiento",
    "- no se heredan permisos de merge, release o mantenimiento hacia otros repositorios.\n\n" + SKILLS_SECTION + "## Procedimiento",
)
replace_once(
    "prompts/focal/09-skills-maintenance.md",
    "- ausencia de contradicciones activas.",
    "- ausencia de contradicciones activas;\n- safeguard de reintentos, `read-after-write` y continuidad de la misma tarea ante fallos transitorios del conector.",
)

REPAIR_SECTION = """## Safeguard del canal durante la reparación

Un fallo transitorio del conector durante `COORDINATOR_REPAIR` no demuestra que el coordinador esté roto ni habilita abandonar la reparación.

1. Reintentá la misma lectura o mutación hasta cuatro intentos totales con backoff de 2, 5, 10 y 20 segundos.
2. Para toda mutación con respuesta de error, hacé `read-after-write` y verificá árbol, ref, issue, PR o workflow antes de repetir.
3. Conservá el mismo payload, SHA esperado e identificador idempotente mientras el resultado sea desconocido.
4. No crees una segunda reparación paralela ni reescribas historia para compensar un error no confirmado.
5. Solo clasificá `CONNECTOR_RETRY_EXHAUSTED` después de agotar reintentos y verificaciones; preservá cualquier rama o PR recuperable y retomá desde allí en la siguiente ejecución.

"""
replace_once(
    "prompts/focal/10-coordinator-repair.md",
    "No actives este modo por latencia ordinaria, una lease ajena, un comando rechazado correctamente, un fallo funcional del proyecto ni para evitar el protocolo normal.\n\n## Canal de ejecución obligatorio",
    "No actives este modo por latencia ordinaria, una lease ajena, un comando rechazado correctamente, un fallo funcional del proyecto ni para evitar el protocolo normal.\n\n" + REPAIR_SECTION + "## Canal de ejecución obligatorio",
)

replace_once(
    "prompts/focal/08-terminal-report.md",
    "Estado de CI:\nÍtems de roadmap modificados:",
    "Estado de CI:\nReintentos del conector:\nMutaciones con resultado desconocido reconciliadas mediante read-after-write:\nPresupuesto de reintentos agotado: sí | no\nÍtems de roadmap modificados:",
)
replace_once(
    "prompts/focal/08-terminal-report.md",
    "- `PASS` requiere publicación, aceptación, reconciliación y liberación completas.",
    "- Un error transitorio aislado no justifica un resultado terminal. Informá cantidad de reintentos y cualquier `read-after-write` usado para reconciliar una mutación de resultado desconocido.\n- `PASS` requiere publicación, aceptación, reconciliación y liberación completas.",
)

FLOW_SUBGRAPH = """
    subgraph CONNECTOR_RETRY[Safeguard transversal del conector — módulos 01, 03, 09 y 10]
        CONNECTOR_ERROR{¿Llamada remota devuelve error transitorio?}
        CONNECTOR_ERROR -- No --> CONNECTOR_CONTINUE[Continuar la misma tarea]
        CONNECTOR_ERROR -- Sí, lectura --> CONNECTOR_BACKOFF[Backoff 2, 5, 10 y 20 segundos; máximo 4 intentos]
        CONNECTOR_ERROR -- Sí, mutación --> READ_AFTER_WRITE[Marcar OUTCOME_UNKNOWN y ejecutar read-after-write]
        READ_AFTER_WRITE --> EFFECT_OBSERVED{¿Efecto remoto observado?}
        EFFECT_OBSERVED -- Sí --> CONNECTOR_CONTINUE
        EFFECT_OBSERVED -- No, guardas vigentes --> RETRY_SAME_OPERATION[Reintentar la misma operación, payload e identificador idempotente]
        RETRY_SAME_OPERATION --> CONNECTOR_BACKOFF
        CONNECTOR_BACKOFF --> CONNECTOR_ERROR
        EFFECT_OBSERVED -- No, presupuesto agotado --> CONNECTOR_RETRY_EXHAUSTED[Preservar checkpoint; PARTIAL o BLOCKED según evidencia]
    end

"""
replace_once(
    "prompts/focal/11-process-flowchart.md",
    "    MODE -- SKILLS_MAINTENANCE --> SM1\n    MODE -- FOCAL_CYCLE --> FC1\n\n    subgraph SKILLS",
    "    MODE -- SKILLS_MAINTENANCE --> SM1\n    MODE -- FOCAL_CYCLE --> FC1\n    LOAD_SHA -. error transitorio .-> CONNECTOR_ERROR\n    SM4 -. error transitorio .-> CONNECTOR_ERROR\n    INSPECT -. error transitorio .-> CONNECTOR_ERROR\n    MUTATION_GUARD -. error transitorio .-> CONNECTOR_ERROR\n    RELEASE -. error transitorio .-> CONNECTOR_ERROR\n\n" + FLOW_SUBGRAPH + "    subgraph SKILLS",
)
replace_once(
    "prompts/focal/11-process-flowchart.md",
    "- Un retraso de evento no es un fallo inmediato: primero se completa polling, un reenvío y el fallback programado.",
    "- Un retraso de evento no es un fallo inmediato: primero se completa polling, un reenvío y el fallback programado.\n- Un error transitorio del conector tampoco es terminal: se reintenta la misma tarea, y toda mutación de resultado desconocido se reconcilia mediante `read-after-write` antes de repetirla.",
)

README_ANCHOR = "| `GITHUB_SERVICE_UNAVAILABLE` | GitHub API, Actions, or repository service is unavailable. | Time, endpoint or operation, and service error. | Preserve remote state already created and stop as `PARTIAL` or `BLOCKED`; never simulate results. | The service is reachable and state can be revalidated. |"
README_ROWS = """| `CONNECTOR_TRANSIENT_FAILURE` | A connector read or write returns a timeout, disconnect, `429`, `5xx`, temporary-unavailable response, transport failure, or internal exception without an authoritative rejection. | Operation, attempt number, UTC timestamps, error class, and any `Retry-After` value. | Retry the same task and operation up to four total attempts with 2, 5, 10, and 20 second backoff. Do not terminate on the first error. | The same remote operation succeeds or an authoritative remote read determines its outcome. |
| `CONNECTOR_MUTATION_OUTCOME_UNKNOWN` | A mutating call returns an error, so it is unknown whether GitHub applied it. | Intended payload, idempotency identifier or expected SHA, error, and authoritative resource to verify. | Perform `read-after-write`. If the effect exists, continue without duplication; otherwise retry the exact same operation while its guards remain valid. | The intended effect is observed or the unchanged authoritative state proves a safe retry. |
| `CONNECTOR_RETRY_EXHAUSTED` | Four attempts, `read-after-write`, and applicable fallbacks are exhausted, or the remaining runtime cannot support a safe retry and closure. | Attempt timeline, last authoritative state, lease status, branch/PR/checkpoint evidence, and remaining budget. | Preserve remote checkpoints and return `PARTIAL` when useful work exists; use `BLOCKED` only when no recoverable evidence exists. The next independent execution resumes the same remote task. | A later execution restores connector access and resumes from the recorded remote state. |
| `GITHUB_SERVICE_UNAVAILABLE` | GitHub API, Actions, or repository service remains unavailable after the connector retry safeguard is exhausted. | Time, endpoint or operation, attempt timeline, and service error. | Preserve remote state already created and stop as `PARTIAL` or `BLOCKED`; never simulate results. | The service is reachable and state can be revalidated. |"""
replace_once("README.md", README_ANCHOR, README_ROWS)

replace_once(
    "scripts/validate_focal_prompt_stack.py",
    '    "lease huérfana",\n)',
    '    "lease huérfana",\n    "Safeguard de fallos transitorios del conector",\n    "read-after-write",\n    "2, 5, 10 y 20 segundos",\n    "CONNECTOR_MUTATION_OUTCOME_UNKNOWN",\n    "CONNECTOR_RETRY_EXHAUSTED",\n    "Reintentos del conector:",\n)',
)
replace_once(
    "scripts/validate_focal_prompt_stack.py",
    '    "PASS",\n)',
    '    "PASS",\n    "CONNECTOR_RETRY",\n    "READ_AFTER_WRITE",\n    "RETRY_SAME_OPERATION",\n    "CONNECTOR_RETRY_EXHAUSTED",\n)',
)
replace_once(
    "scripts/validate_focal_prompt_stack.py",
    '        "No incluyas campos `owner`",\n    )',
    '        "No incluyas campos `owner`",\n        "OUTCOME_UNKNOWN",\n        "read-after-write",\n        "cuatro intentos",\n    )',
)
replace_once(
    "scripts/validate_focal_prompt_stack.py",
    '    if combined.count("última mutación") + combined.count("ÚLTIMA mutación") < 4:\n        fail(errors, "final release boundary is not reinforced across the prompt stack")',
    '    if combined.count("última mutación") + combined.count("ÚLTIMA mutación") < 4:\n        fail(errors, "final release boundary is not reinforced across the prompt stack")\n    if combined.count("read-after-write") < 5:\n        fail(errors, "connector unknown-outcome reconciliation is not reinforced across the prompt stack")\n    if combined.count("cuatro intentos") + combined.count("four total attempts") < 3:\n        fail(errors, "connector retry budget is not reinforced across the prompt stack")',
)

print("Applied connector retry safeguard to the Focal prompt stack.")
