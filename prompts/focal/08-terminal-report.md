# Focal — Reporte terminal único

Emití una sola plantilla. Omití secciones narrativas duplicadas y no repitas el resumen.

```text
Resultado: PASS | PARTIAL | BLOCKED | NO-OP
Modo: FOCAL_CYCLE | SKILLS_MAINTENANCE
Ruta excepcional: no aplicable | COORDINATOR_REPAIR
Inicio UTC:
Fin UTC:
Runtime guard:
SHA remoto inicial:
SHA remoto final observado:
Objetivo seleccionado:
Alcance realizado:
Archivos creados, modificados, movidos o eliminados:
Pruebas ejecutadas:
Pruebas aprobadas:
Pruebas fallidas:
Pruebas no ejecutadas y motivo:
Commit(s) funcionales:
Commits temporales de reparación:
Historia final de Focal: no aplicable | limpia, sin commits temporales alcanzables | pendiente de limpieza
Candidatos saneados: NOOP_COMMIT | EMPTY_ARTIFACT_COMMIT | FAILED_TRANSPORT_COMMIT | GARBAGE_ARTIFACT_COMMIT | GARBAGE_ARTIFACT_MIXED_COMMIT | ninguno
Paths basura retirados y clasificación:
Fallos autónomamente recuperados:
Ruta de recuperación aplicada:
Fallos no clasificados convertidos en diagnóstico: ninguno | detalle
SHAs excluidos y evidencia:
Commits posteriores reconstruidos:
Timestamps posteriores preservados: authorDate y committerDate exactos | no aplicable | no verificado
Refs temporales eliminadas:
Candidatos alcanzables desde refs/heads o refs/tags: ninguno | detalle
Commit o merge de limpieza presente: no | sí | no aplicable
Árbol final verificado:
Parent y metadata preservados:
Workflow temporal ausente: sí | no | no aplicable
Rama:
Pull request:
Estado del merge:
Estado de CI:
Reintentos del conector:
Mutaciones con resultado desconocido reconciliadas mediante read-after-write:
Presupuesto de reintentos agotado: sí | no
Ítems de roadmap modificados:
Estados finales de esos ítems:
Capacidades de Iris verificadas o actualizadas:
Roadmap path: docs/ROADMAP.md
Iris matrix path: docs/IRIS-CAPABILITY-MATRIX.md
Flowchart path: prompts/focal/11-process-flowchart.md | no aplicable
Checkpoint remoto:
Bloqueos:
Siguiente acción recomendada:
Coordinador: issue #7 / focal-state:v3
Run ID:
Command ID de adquisición:
Último heartbeat confirmado:
Command ID de liberación:
Lock liberado: sí | no | no adquirido
Estado final observado: idle | working | desconocido
Limitaciones reales:
```

Reglas:

- Usá SHA, números de PR, runs y rutas verificables.
- No declares que un archivo o cambio existe si no fue observado remotamente.
- No incluyas nombres de proveedor, modelo, aplicación, cliente, conector, actor, producto o plataforma de conversación. No reproduzcas campos legacy `owner`, `executionSource` ni logins del emisor.
- `runId` y `commandId` son identificadores opacos; no intentes derivar ni explicar la herramienta que los originó.
- Un error transitorio aislado no justifica un resultado terminal. Informá cantidad de reintentos y cualquier `read-after-write` usado para reconciliar una mutación de resultado desconocido.
- `PASS` requiere publicación, aceptación, reconciliación y liberación completas.
- En `NO-OP` por lease activa, indicá únicamente `runId`, fase y expiración observados sin modificar el estado.
- En `SKILLS_MAINTENANCE`, reemplazá las rutas de roadmap y matriz por `no aplicable` salvo que la tarea también autorice Focal.
- En `COORDINATOR_REPAIR`, distinguí commits temporales observados de commits alcanzables al final. `PASS` requiere que ningún commit, merge, workflow o ref temporal de reparación permanezca alcanzable desde `main`.
- Cuando se sanee historia, listá commits y paths candidatos, su clasificación probada, los commits posteriores reconstruidos y la comparación exacta de `authorDate` y `committerDate`. Incluí archivos placeholder como `X`, salidas de herramientas y dumps solo cuando la evidencia conjunta demuestre que son basura. `PASS` exige cero candidatos alcanzables desde heads o tags, cero ramas temporales y ningún commit de limpieza.
- Para cada error, informá el código, la ruta de recuperación y la validación que permitió reanudar. `UNCLASSIFIED_INTERNAL_FAILURE` no puede quedar sin diagnóstico o checkpoint recuperable.
- Si se reescribió el commit final de Focal mediante GitHub Actions, informá el árbol preservado, parent, autor, committer, fechas y mensaje verificados.
- La imposibilidad de borrar auditoría interna de GitHub o del proveedor es una limitación de plataforma; no la confundas con contenido controlado por el repositorio.
