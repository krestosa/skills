# Focal — Control plane autónomo v4

Este módulo es normativo y adapta las ejecuciones de Focal al control plane publicado en `krestosa/Focal`. Cuando una cláusula anterior sobre fuente de estado, orden terminal, watchdog, router de intención o limpieza administrativa sea incompatible con este módulo, prevalece este módulo. No modifica criterios funcionales, de roadmap, Iris, calidad ni aceptación.

## Arquitectura obligatoria

El control plane usa una autoridad única de lease y workflows permanentes especializados:

- `.github/workflows/automation-state.yml`: único procesador serializado de comandos funcionales y mirror del estado;
- rama `automation/state-v4`, archivo `.focal/automation-state.json`: estado canónico transaccional;
- issue `#7`: entrada de comandos funcionales y mirror humano del estado canónico;
- issue `#101`, `[automation-maintenance] Focal repository maintenance`: entrada exclusiva de comandos administrativos;
- `.github/workflows/stale-lease-watchdog.yml`: guard terminal independiente;
- `.github/workflows/repository-maintenance.yml`: mantenimiento permanente y scoped de ramas y archivos basura;
- `.github/workflows/validation.yml`: validación del repositorio y evidencia funcional.

No crees workflows ad hoc para borrar ramas, retirar archivos basura, reconstruir estado, renovar leases ni ejecutar una operación Git puntual. Extendé o repará una capacidad permanente mediante una PR validada únicamente cuando el usuario pidió cambiar su implementación. Un workflow temporal solo es admisible para el saneamiento histórico excepcional ya autorizado y debe contener el marcador `# focal-temporary-workflow: true`, quedar fuera del árbol final y ser retirado por la ruta permanente.

## Separación obligatoria de intenciones

`REPOSITORY_MAINTENANCE` significa **usar** una capacidad administrativa ya publicada. `FOCAL_CYCLE` significa **cambiar** la implementación o el producto.

- ejecutar, borrar, limpiar, retirar o previsualizar ramas detrás de `main` → `REPOSITORY_MAINTENANCE`;
- ejecutar limpieza de basura allowlisted → `REPOSITORY_MAINTENANCE`;
- ejecutar retiro de workflows explícitamente temporales → `REPOSITORY_MAINTENANCE`;
- crear, implementar, mejorar, ampliar, reparar o modificar el workflow o script de mantenimiento → `FOCAL_CYCLE`.

No conviertas una solicitud de ejecución en una unidad de desarrollo por ausencia de una operación directa del conector. El issue `#101` es el puente permanente hacia GitHub Actions. Si ese issue, workflow o contrato no existe o no puede invocarse, terminá `MAINTENANCE_EXECUTION_PATH_UNAVAILABLE`; no crees rama, PR, commit ni workflow sustituto.

## Fuente canónica y mirror funcional

1. En `FOCAL_CYCLE`, la primera lectura remota continúa siendo el issue `#7` completo.
2. El bloque `focal-command:v3` del issue `#7` es la única entrada de comandos funcionales.
3. El bloque `focal-state:v3` del issue `#7` es un mirror autoritativo para el ejecutor durante el ciclo, producido desde el archivo transaccional; nunca se edita directamente.
4. La fuente persistente canónica es `.focal/automation-state.json` en `automation/state-v4`.
5. Ante discrepancia entre mirror y archivo transaccional, no mutés trabajo funcional ni administrativo.
6. No uses la rama transaccional como rama de trabajo, checkpoint funcional ni baseline del producto.

## Compare-and-swap e idempotencia funcional

Todo comando funcional puede incluir:

```json
{
  "expectedStateVersion": 123,
  "expectedCheckpointSha": "<SHA observado o null>"
}
```

- Usá `expectedStateVersion` para `acquire`, `recover`, `heartbeat`, `release` y `assert_terminal` cuando el estado observado lo provea.
- Usá `expectedCheckpointSha` cuando la operación dependa de que el checkpoint no haya cambiado.
- `STATE_VERSION_MISMATCH` y `CHECKPOINT_MISMATCH` invalidan la operación; releé el issue y recalculá desde el estado nuevo.
- Conservá el mismo `commandId` para un resultado de transporte desconocido.
- Un comando presente en `processedCommandIds` se considera procesado aunque no sea el último.
- Los checkpoints de `phaseCheckpoints` son evidencia de reanudación; no autorizan saltar gates.

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

- Si la reconciliación está publicada y recuperable, liberá con el resultado factual.
- El estado registra el handoff en `reconciliation` y vuelve a `IDLE`.
- La ejecución siguiente retoma primero ese handoff si sigue abierto y ejecutable.
- No mantengas `WORKING` esperando una PR documental cuando ya existe un checkpoint remoto suficiente.

## Finalización funcional obligatoria equivalente a `finally`

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

## Comando funcional `assert_terminal`

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

No produzcas un reporte normal que afirme cierre, `IDLE` o autonomía completa si este gate no fue observado.

## Guard terminal independiente

El guard terminal se ejecuta cada cinco minutos bajo `concurrency.group: focal-automation-state`.

- Antes de `hardKillAt`, conserva la política de lease expirada sin actividad mutadora reciente.
- Desde `hardKillAt`, libera la lease como `PARTIAL` aunque exista actividad remota, para impedir un `WORKING` permanente.
- Preserva `workBranch`, `workBranchHeadSha`, `pullRequest` y `checkpointSha` en `pendingRecovery`.
- No autoriza comenzar trabajo funcional sin una nueva adquisición o recuperación confirmada.
- Es una red de seguridad; no reemplaza `release` y `assert_terminal`.

## Modo `REPOSITORY_MAINTENANCE`

El mantenimiento administrativo es un modo terminal independiente. No forma parte del inicio, cuerpo o cierre de `FOCAL_CYCLE`.

### Precondiciones

1. Clasificá el scope exacto antes de leer recursos funcionales.
2. La **PRIMERA lectura remota de `krestosa/Focal`** debe ser el issue `#7` completo.
3. Exigí `status == idle` y `runId == null`. Si existe una lease activa, terminá `ACTIVE_RUN`; no adquieras, liberes ni esperes esa lease.
4. Leé el issue `#101` y verificá título y un único bloque `focal-repository-maintenance:v1`.
5. Verificá que `.github/workflows/repository-maintenance.yml` ya exista. Esta comprobación no autoriza modificarlo.
6. No leas roadmap, matriz de Iris, shaders ni candidatos funcionales.

### Scopes cerrados

- `branches`: ramas completamente detrás de la rama predeterminada, sin PR abierta, no protegidas y distintas de `main` y `automation/state-v4`;
- `garbage`: `.DS_Store`, `Thumbs.db`, `*.orig`, `*.rej`, bytecode de Python y caches de pytest;
- `temporary_workflows`: workflows que contengan explícitamente `# focal-temporary-workflow: true`;
- `all`: unión de los tres scopes anteriores.

No amplíes el scope. “Borrar branches detrás de main” es `branches`, no `all`. Una solicitud de previsualización, revisión o dry-run usa `dryRun: true`; una solicitud explícita de borrar, eliminar o limpiar usa `dryRun: false`.

### Comando administrativo

Reemplazá únicamente el JSON del bloque administrado del issue `#101`:

```json
{
  "schemaVersion": 1,
  "commandId": "<único>",
  "operation": "repository_maintenance",
  "scope": "branches | garbage | temporary_workflows | all",
  "dryRun": false
}
```

- `commandId` debe ser nuevo por intención lógica.
- Ante error de transporte, conservá el mismo `commandId` y aplicá `read-after-write`.
- `processedMaintenanceCommandIds` impide replays no adyacentes.
- No escribas el comando en `focal-command:v3`; ese bloque es exclusivamente funcional.
- No adquieras una lease y no generes `runId`.

### Mutaciones prohibidas

Durante `REPOSITORY_MAINTENANCE` queda prohibido:

- crear o actualizar una rama de transporte;
- crear un commit para ejecutar un cleanup de scope `branches`;
- crear, abrir, modificar o mergear una PR;
- crear o modificar un workflow;
- entrar en `COORDINATOR_REPAIR` o `FOCAL_CYCLE` para suplir una ruta ausente;
- modificar `main` cuando el scope sea `branches`;
- ejecutar una categoría no solicitada.

La cantidad final de ramas debe ser menor o igual a la inicial. `createdBranches` debe ser una lista vacía. Toda rama eliminada debe pertenecer al plan observado antes de mutar.

### Confirmación

Después de escribir el comando:

1. Esperá con polling real el run de `Repository Maintenance`.
2. Releé el issue `#7` hasta que `lastRepositoryMaintenanceCommandId` coincida.
3. Exigí `lastRepositoryMaintenanceReason == MAINTENANCE_COMPLETED` o `MAINTENANCE_DRY_RUN`.
4. Verificá `lastRepositoryMaintenance.scope` igual al solicitado.
5. Verificá `createdBranches == []` y `branchCountAfter <= branchCountBefore`.
6. Para `branches`, verificá `defaultBranchHeadAfter == defaultBranchHeadBefore`.
7. Verificá que no exista una nueva PR, rama o workflow producidos por la operación.
8. Emití el reporte administrativo sin roadmap, Iris, lease, release, `assert_terminal`, PR ni merge.

Si el workflow termina fallido, diagnosticá el run pero no cambies automáticamente a implementación. Solo una instrucción explícita de reparar la capacidad autoriza un `FOCAL_CYCLE` posterior.

## Errores administrativos cerrados

- `MAINTENANCE_INTENT_MISROUTED`: una solicitud de ejecución entró en `FOCAL_CYCLE` o creó una rama/PR; detené esa ruta y volvé al modo administrativo sin conservar artefactos nuevos.
- `MAINTENANCE_EXECUTION_PATH_UNAVAILABLE`: issue `#101`, workflow permanente o trigger no está disponible; no improvises infraestructura.
- `MAINTENANCE_SCOPE_INVALID`: el scope no pertenece al conjunto cerrado o excede lo solicitado.
- `MAINTENANCE_CREATED_REF`: apareció una rama nueva durante la operación.
- `MAINTENANCE_CREATED_PR`: apareció o se modificó una PR por la operación administrativa.
- `MAINTENANCE_CREATED_WORKFLOW`: apareció o se modificó un workflow por la operación administrativa.
- `MAINTENANCE_BRANCH_COUNT_INCREASED`: la cantidad final de ramas supera la inicial.
- `MAINTENANCE_BRANCH_SCOPE_MODIFIED_DEFAULT_HEAD`: el scope `branches` modificó el head de la rama predeterminada.
- `MAINTENANCE_RESULT_NOT_CORRELATED`: el `commandId` no aparece en el estado después del polling y fallback permitidos.

Estos códigos no autorizan reparar implementación salvo petición expresa. La recuperación ordinaria es reintento, `read-after-write`, correlación o detención sin mutaciones sustitutas.

## Gate del reporte terminal

Para `FOCAL_CYCLE`, antes de usar `08-terminal-report.md`, registrá:

- command ID de `release`;
- `LEASE_RELEASED` observado;
- command ID de `assert_terminal`;
- `TERMINAL_STATE_CONFIRMED` observado;
- `terminalVerifiedAt`;
- estado final `IDLE` y `terminalVerifiedRunId` propio.

Para `REPOSITORY_MAINTENANCE`, registrá:

- issue `#101` y command ID administrativo;
- scope y `dryRun`;
- workflow y run exactos;
- `lastRepositoryMaintenanceCommandId` correlacionado;
- branches o paths seleccionados y eliminados;
- conteos antes/después;
- `createdBranches == []`;
- head de `main` antes/después cuando el scope sea `branches`;
- estado `IDLE` observado en issue `#7`.

El reporte debe distinguir entrega funcional, reconciliación, recuperación automática y mantenimiento administrativo. El estado terminal se verifica; no se infiere.
