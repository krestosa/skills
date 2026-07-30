# Focal — Control plane autónomo v4

Este módulo es normativo y adapta `FOCAL_CYCLE` al control plane publicado en `krestosa/Focal` por la PR #96. Cuando una cláusula anterior sobre fuente de estado, orden terminal, watchdog o limpieza administrativa sea incompatible con este módulo, prevalece este módulo. No modifica criterios funcionales, de roadmap, Iris, calidad ni aceptación.

## Arquitectura obligatoria

El control plane usa una autoridad única de coordinación y workflows permanentes especializados:

- `.github/workflows/automation-state.yml`: único procesador serializado de comandos y mirror del estado;
- rama `automation/state-v4`, archivo `.focal/automation-state.json`: estado canónico transaccional;
- issue `#7`: superficie de entrada de comandos y mirror humano del estado canónico;
- `.github/workflows/stale-lease-watchdog.yml`: guard terminal independiente;
- `.github/workflows/repository-maintenance.yml`: mantenimiento permanente de ramas y archivos basura;
- `.github/workflows/validation.yml`: validación del repositorio y evidencia funcional.

No crees workflows ad hoc para borrar ramas, retirar archivos basura, reconstruir estado, renovar leases ni ejecutar una operación Git puntual. Extendé una capacidad permanente únicamente mediante una PR validada. Un workflow temporal solo es admisible para el saneamiento histórico excepcional ya autorizado y debe contener el marcador `# focal-temporary-workflow: true`, quedar fuera del árbol final y ser retirado por la ruta de mantenimiento permanente.

## Fuente canónica y mirror

1. La primera lectura remota continúa siendo el issue `#7` completo.
2. El bloque `focal-command:v3` del issue es la única entrada de comandos del agente.
3. El bloque `focal-state:v3` del issue es un mirror autoritativo para el agente durante el ciclo, producido desde el archivo transaccional; el agente nunca lo edita directamente.
4. La fuente persistente canónica es `.focal/automation-state.json` en `automation/state-v4`.
5. Ante discrepancia entre mirror y archivo transaccional, no mutés trabajo funcional. Esperá la reconciliación automática o ejecutá `COORDINATOR_REPAIR` si se cumplen sus gates.
6. No uses la rama transaccional como rama de trabajo, checkpoint funcional ni baseline del producto.

## Compare-and-swap e idempotencia

Todo comando puede incluir:

```json
{
  "expectedStateVersion": 123,
  "expectedCheckpointSha": "<SHA observado o null>"
}
```

- Usá `expectedStateVersion` para `acquire`, `recover`, `heartbeat`, `release` y `assert_terminal` cuando el estado observado lo provea.
- Usá `expectedCheckpointSha` cuando la operación dependa de que el checkpoint no haya cambiado.
- `STATE_VERSION_MISMATCH` y `CHECKPOINT_MISMATCH` invalidan la operación; releé el issue y recalculá desde el estado nuevo. No repitas con valores antiguos.
- Conservá el mismo `commandId` para un resultado de transporte desconocido. Un comando ya presente en `processedCommandIds` se considera procesado aunque no sea el último comando.
- Los checkpoints de fase de `phaseCheckpoints` son evidencia de reanudación; no son autorización para saltar gates.

## Separación entre entrega funcional y reconciliación

Una entrega funcional mergeada no debe mantener la lease abierta únicamente porque quede documentación o reconciliación pendiente.

El comando `release` puede agregar:

```json
{
  "functionalCheckpointSha": "<merge o checkpoint funcional>",
  "reconciliationPullRequest": 123,
  "reconciliationBranch": "docs/reconcile-example",
  "reconciliationCheckpointSha": "<head documental>",
  "reconciliationStatus": "pending | complete | blocked",
  "reconciliationNote": "<nota neutral>"
}
```

- Si la reconciliación está publicada y recuperable, liberá como `PARTIAL` o el resultado factual correspondiente.
- El estado registra el handoff en `reconciliation` y vuelve a `IDLE`.
- La ejecución siguiente retoma primero ese handoff si sigue abierto y ejecutable.
- No mantengas `WORKING` esperando una PR documental cuando ya existe un checkpoint remoto suficiente.

## Finalización obligatoria equivalente a `finally`

Toda ejecución que haya adquirido o recuperado una lease debe ejecutar esta secuencia, incluso ante excepción, `PASS`, `PARTIAL`, `BLOCKED`, `NO-OP`, agotamiento del presupuesto o fallo de validación:

1. Detener procesos locales propios.
2. Preservar en GitHub el último checkpoint útil, PR y rama recuperables.
3. Completar todas las mutaciones funcionales, documentales y de entrega permitidas.
4. Releer el issue y confirmar propiedad.
5. Enviar `release` con resultado factual, checkpoint y handoff de reconciliación si existe.
6. Aplicar polling y `read-after-write` hasta observar `LEASE_RELEASED`, `status == idle`, `runId == null` y `lastRunId` propio.
7. Enviar exactamente un comando `assert_terminal` para el mismo `runId` finalizado.
8. Aplicar polling y `read-after-write` hasta observar `TERMINAL_STATE_CONFIRMED`, `status == idle`, `runId == null` y `terminalVerifiedRunId` propio.
9. Recién entonces emitir el reporte terminal.

`release` es la última mutación de código, archivos, ramas, PRs, merges, documentación, labels y releases. La única mutación permitida después de `release` es `assert_terminal` sobre el bloque de comando del issue. Después de `assert_terminal` solo se permiten lecturas.

## Comando `assert_terminal`

```json
{
  "schemaVersion": 3,
  "commandId": "<único>",
  "operation": "assert_terminal",
  "runId": "<runId finalizado>",
  "expectedStateVersion": 123
}
```

Exigí simultáneamente:

- `lastCommandAccepted == true`;
- `lastCommandReason == TERMINAL_STATE_CONFIRMED`;
- `status == idle`;
- `runId == null`;
- `terminalVerifiedRunId` igual al run finalizado;
- `terminalVerifiedAt` presente.

No produzcas un reporte normal que afirme cierre, `IDLE` o autonomía completa si este gate no fue observado. En ese caso continuá el safeguard de comandos mientras quede presupuesto. Si el proceso desaparece, el guard terminal recuperará la lease, pero esa recuperación no convierte retroactivamente el ciclo en `PASS`.

## Guard terminal independiente

El guard terminal se ejecuta cada cinco minutos bajo `concurrency.group: focal-automation-state`.

- Antes de `hardKillAt`, conserva la política de lease expirada sin actividad mutadora reciente.
- Desde `hardKillAt`, libera la lease como `PARTIAL` aunque exista actividad remota, para impedir un `WORKING` permanente.
- Preserva `workBranch`, `workBranchHeadSha`, `pullRequest` y `checkpointSha` en `pendingRecovery`.
- No autoriza comenzar trabajo funcional sin una nueva adquisición o recuperación confirmada.
- Es una red de seguridad; no reemplaza la obligación del ejecutor de enviar `release` y `assert_terminal`.

## Mantenimiento permanente de ramas y archivos basura

`repository-maintenance.yml` es la única ruta ordinaria para limpieza administrativa. Comparte el lock `focal-automation-state` y solo actúa cuando el estado está `IDLE`.

Puede retirar únicamente:

- ramas completamente detrás de la rama predeterminada, sin PR abierta, no protegidas y distintas de `automation/state-v4`;
- `.DS_Store`, `Thumbs.db`, `*.orig`, `*.rej`, bytecode de Python y caches de pytest;
- workflows que contengan explícitamente `# focal-temporary-workflow: true`.

Debe preservar:

- `main`, ramas protegidas y la rama transaccional;
- ramas con PR abierta;
- trabajo no mergeado;
- workflows sin marcador temporal;
- archivos no cubiertos por el allowlist.

La limpieza programada no forma parte de `FOCAL_CYCLE`. No liberes una lease para ejecutar mantenimiento dentro del mismo ciclo. Si detectás basura durante una ejecución funcional, registrá la evidencia y dejá que el workflow permanente la retire cuando el coordinador esté libre, salvo que el archivo forme parte del diff funcional actual y deba corregirse antes del merge.

## Gate del reporte terminal

Antes de usar `08-terminal-report.md`, registrá como evidencia:

- command ID de `release`;
- `LEASE_RELEASED` observado;
- command ID de `assert_terminal`;
- `TERMINAL_STATE_CONFIRMED` observado;
- `terminalVerifiedAt`;
- estado final `IDLE` y `terminalVerifiedRunId` propio.

El reporte debe distinguir:

- entrega funcional;
- reconciliación pendiente o completa;
- recuperación automática aplicada, si la hubo;
- mantenimiento administrativo, que es independiente;
- estado terminal verificado, no inferido.
