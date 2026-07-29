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
Árbol final verificado:
Parent y metadata preservados:
Workflow temporal ausente: sí | no | no aplicable
Rama:
Pull request:
Estado del merge:
Estado de CI:
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
- `PASS` requiere publicación, aceptación, reconciliación y liberación completas.
- En `NO-OP` por lease activa, indicá el propietario, fase y expiración observados sin modificar el estado.
- En `SKILLS_MAINTENANCE`, reemplazá las rutas de roadmap y matriz por `no aplicable` salvo que la tarea también autorice Focal.
- En `COORDINATOR_REPAIR`, distinguí commits temporales observados de commits alcanzables al final. `PASS` requiere que ningún commit, merge, workflow o ref temporal de reparación permanezca alcanzable desde `main`.
- Si se reescribió el commit final de Focal mediante GitHub Actions, informá el árbol preservado, parent, autor, committer, fechas y mensaje verificados.
