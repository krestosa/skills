# Focal — Coordinación y exclusión mutua

Este módulo define el único mecanismo canónico de estado operativo.

## Fuente canónica

```text
Repositorio: krestosa/Focal
Issue: #7
Título esperado: [automation-state] Focal execution state
Workflow: .github/workflows/automation-state.yml
Nombre del workflow: Automation State Coordinator
Command block: <!-- focal-command:v3 -->
State block: <!-- focal-state:v3 -->
```

El cuerpo del issue es la única fuente de lease. El historial Git, ramas operativas, archivos JSON y comentarios no son estado activo. El workflow serializa comandos mediante `concurrency.group: focal-automation-state` y `cancel-in-progress: false`.

## Invariantes de borde obligatorias

1. Después de cargar el prompt, la **PRIMERA lectura remota de `krestosa/Focal`** debe ser el issue `#7` completo.
2. Antes de adquirir la lease solo se permite, además de esa lectura, resolver la rama predeterminada y el SHA de `main` requerido por `baseMainSha`. Se exceptúan únicamente las lecturas limitadas exigidas para evaluar una lease vencida recuperable y las operaciones estrictas de `COORDINATOR_REPAIR` definidas en `10-coordinator-repair.md`.
3. La primera mutación remota debe reemplazar exclusivamente el JSON de `focal-command:v3` para `inspect`, `acquire` o `recover`.
4. Nunca edites directamente `focal-state:v3`; únicamente `Automation State Coordinator` puede modificarlo.
5. No leas en profundidad ni mutes roadmap, matriz, archivos, ramas, PRs, commits, checks, workflows o releases hasta que el estado confirme propiedad. Solo se permiten la inspección limitada previa a `recover` y la reparación bootstrap acotada de `10-coordinator-repair.md`.
6. Antes de cada mutación posterior, releé el issue y confirmá `status == working`, `runId` propio y lease futura.
7. La **ÚLTIMA mutación remota del ciclo** debe ser el comando `release` en `focal-command:v3`.
8. Después de `release` solo se permiten lecturas del issue para confirmar el estado y emitir el reporte.
9. Si un chat está trabajando pero el issue muestra `idle`, ese chat no posee la ejecución: debe detenerse. La única excepción es `COORDINATOR_REPAIR`, que no autoriza trabajo funcional y se limita al coordinador.
10. `cleanup_branches` es una operación administrativa independiente. No puede formar parte del inicio, cuerpo o cierre de un `FOCAL_CYCLE`; `cleanup_branches` no forma parte de un ciclo de desarrollo.

## Minimización obligatoria de procedencia

La coordinación necesita identificar una ejecución, no la herramienta que la ejecuta.

- `commandId` y `runId` son los únicos identificadores operativos permitidos.
- No incluyas campos `owner`, `executionSource`, `client`, `provider`, `model`, `agent`, `actor`, `sender` ni equivalentes en comandos nuevos.
- No escribas nombres de proveedor, modelo, aplicación, cliente, conector, producto o plataforma de conversación en el issue, notas, logs, ramas, commits, PRs, checks, reportes o artefactos de Focal.
- Los campos legacy de procedencia que existan en `focal-state:v3` deben ser eliminados por el coordinador en la siguiente transición válida; mientras tanto no se consideran parte de la propiedad.
- No registres el login del emisor en la salida del workflow. La auditoría de GitHub permanece en la plataforma y no debe duplicarse dentro de los artefactos del repositorio.
- No prometas borrar auditoría interna de GitHub o del proveedor: el contrato cubre únicamente contenido y metadatos controlados por los repositorios.

## Estado legacy retirado

No leas, crees, actualices ni recuperes coordinación desde:

```text
automation/runtime-state
automation/run-state.json
issue #2
issue #5
```

No mantengas una ruta fallback hacia esos mecanismos. El historial puede documentar su existencia, pero no son ejecutables.

## Campos canónicos del bloque de estado

Interpretá como estado operativo:

- `schemaVersion` y `version`: contrato y revisión del estado;
- `status`: `idle` o `working`;
- `mode`: `normal` o `recovery`;
- `phase`: fase vigente;
- `runId`: único propietario operativo;
- `startedAt`, `heartbeatAt` y `leaseExpiresAt`: vigencia;
- `softStopAt`, `cleanupAt`, `hardKillAt` y `deadlineAt`: límites;
- `baseMainSha`: baseline observado;
- `workBranch`, `workBranchHeadSha`, `pullRequest` y `checkpointSha`: continuidad remota;
- `lastCompletedAt`, `lastResult` y `lastRunId`: último ciclo finalizado;
- `lastCommandId`, `lastCommandAccepted`, `lastCommandReason` y `lastCommandProcessedAt`: correlación del comando;
- campos adicionales desconocidos: conservarlos salvo que sean campos de procedencia prohibidos.

`status == working`, un `runId` ajeno y `leaseExpiresAt` futuro representan una ejecución activa. `status == idle` y `runId == null` representan ausencia de propietario.

## Identidad y lease

Cada ciclo crea un `runId` UUID v4 y un `commandId` único por operación.

Parámetros canónicos:

- lease inicial: 30 minutos;
- heartbeat operativo: en cada cambio de fase y como máximo cada cinco minutos;
- renovación adicional: antes de publicación, espera de CI, merge y cleanup interno;
- margen previo a cualquier mutación: si restan menos de cinco minutos, renovar primero;
- todos los timestamps: UTC ISO-8601;
- la lease solo existe cuando el bloque de estado confirma el mismo `commandId`, aceptación, razón esperada, `runId` propio y expiración futura.

Editar el issue no equivale a adquirir o renovar. Escribir un comando sin observar la respuesta tampoco.

## Fallos del conector y mutaciones de resultado desconocido

Los errores del canal de herramientas no cambian por sí mismos el estado remoto.

1. Aplicá hasta cuatro intentos totales con backoff de 2, 5, 10 y 20 segundos a timeouts, desconexiones, `429`, `5xx`, indisponibilidad temporal y excepciones internas sin rechazo autoritativo.
2. Una lectura fallida se repite contra la misma fuente canónica; no se sustituye por memoria ni por una copia local.
3. Una mutación que devuelve error queda en estado `CONNECTOR_MUTATION_OUTCOME_UNKNOWN` (`OUTCOME_UNKNOWN`). Antes de repetirla, ejecutá `read-after-write` sobre issue, archivo, ref, commit, PR, merge, check o release afectado.
4. Si el efecto remoto coincide con la intención, registrá la operación como aplicada y continuá. Si no coincide y las precondiciones siguen vigentes, reintentá exactamente la misma operación con el mismo payload e identificador idempotente.
5. Para escribir `focal-command:v3`, conservá el mismo `commandId` mientras la propia escritura no esté confirmada. Generá un `commandId` nuevo solo cuando la escritura fue observada pero el coordinador no la procesó durante la ventana definida en Entrega resiliente de comandos.
6. Durante una interrupción no confirmes ni niegues propiedad por inferencia. Pausá mutaciones funcionales y reintentá la lectura del issue hasta recuperar una observación autoritativa o agotar el presupuesto.
7. El primer error no permite liberar la lease, cerrar la PR, descartar la rama ni terminar la tarea. Si el proceso completo desaparece, la siguiente ejecución retoma desde issue, rama, PR y checkpoint remotos.
8. Solo después de agotar reintentos, `read-after-write` y fallbacks aplicables puede clasificarse `CONNECTOR_RETRY_EXHAUSTED`; si existe checkpoint útil, el resultado es `PARTIAL`, no `BLOCKED`.

## Preservación del cuerpo

Para cada comando:

1. Releé el issue #7.
2. Validá ambos bloques y `schemaVersion: 3`.
3. Conservá exactamente todo el cuerpo fuera del JSON del bloque de comando.
4. Conservá intacto el bloque de estado observado; no copies campos de procedencia legacy a comandos nuevos.
5. Reemplazá solo el JSON del bloque de comando.
6. Actualizá el cuerpo completo.
7. Esperá entre 5 y 10 segundos reales antes de cada relectura.
8. Correlacioná por `lastCommandId`.
9. Mantené polling acotado durante al menos 45 segundos reales antes de clasificar el comando como no procesado; no busy-wait ni esperas indefinidas. Un run terminal fallido permite abreviar la ventana.
10. No crees comentarios operativos.
11. Si otro actor reemplazó el comando antes de ser procesado, no asumas éxito: releé estado, verificá propiedad y reenviá únicamente con un `commandId` nuevo si sigue siendo seguro.

## Entrega resiliente de comandos

La pérdida o demora de un evento `issues.edited` no debe producir un bloqueo prematuro.

1. Para cada operación, completá primero una ventana de 45 segundos reales.
2. Si `lastCommandId` no correlaciona, el issue sigue `idle`, `runId == null` y no hay evidencia positiva de un workflow mutador activo, reenviá exactamente una vez la misma operación con:
   - `commandId` nuevo;
   - timestamps recalculados;
   - `leaseExpiresAt`, soft stop, cleanup y hard stop coherentes con el tiempo restante;
   - el mismo `runId` solo si la ejecución todavía no terminó.
3. Esperá otra ventana de 45 segundos reales.
4. Si continúa sin correlación, verificá el fallback programado de `.github/workflows/automation-state.yml`. El workflow debe admitir `schedule` cada cinco minutos y `workflow_dispatch` además de `issues.edited`.
5. Cuando el fallback programado exista y resten al menos diez minutos del ciclo, esperá hasta seis minutos desde el segundo envío, observando runs cuando estén disponibles.
6. No termines `BLOCKED`, no actives reparación y no emitas un resultado mientras el reenvío o el fallback aplicable sigan pendientes dentro del presupuesto.
7. Si el comando se correlaciona tarde después de que el llamador terminó, no inicies trabajo retrospectivo. Enviá `release` con el mismo `runId` y una nota neutral; esa liberación sanea una lease huérfana.
8. Solo después de agotar estas rutas evaluá `COORDINATOR_REPAIR`.

## Comandos canónicos

### Inspección

```json
{
  "schemaVersion": 3,
  "commandId": "<único>",
  "operation": "inspect"
}
```

Exigí `lastCommandAccepted == true` y `lastCommandReason == STATE_OBSERVED`.

### Adquisición

```json
{
  "schemaVersion": 3,
  "commandId": "<único>",
  "operation": "acquire",
  "runId": "<UUID v4>",
  "mode": "normal",
  "phase": "LOCK_ACQUISITION",
  "startedAt": "<UTC>",
  "heartbeatAt": "<UTC>",
  "leaseExpiresAt": "<UTC futuro>",
  "softStopAt": "<UTC>",
  "cleanupAt": "<UTC>",
  "hardKillAt": "<UTC>",
  "deadlineAt": "<UTC>",
  "baseMainSha": "<SHA>",
  "workBranch": null,
  "workBranchHeadSha": null,
  "pullRequest": null,
  "checkpointSha": null,
  "note": null
}
```

La adquisición exige `LEASE_ACQUIRED`, `status == working`, `runId` propio y expiración futura. Mientras el issue no muestre esos valores, el ciclo sigue sin comenzar.

### Recuperación

Usá el mismo contrato de adquisición con:

```json
{
  "operation": "recover",
  "mode": "recovery"
}
```

La recuperación exige `LEASE_RECOVERED`.

### Heartbeat

```json
{
  "schemaVersion": 3,
  "commandId": "<único>",
  "operation": "heartbeat",
  "runId": "<propietario>",
  "phase": "<fase actual>",
  "heartbeatAt": "<UTC>",
  "leaseExpiresAt": "<UTC futuro>",
  "workBranch": "<rama o null>",
  "workBranchHeadSha": "<SHA o null>",
  "pullRequest": "<número o null>",
  "checkpointSha": "<SHA o null>",
  "note": null
}
```

Exigí `HEARTBEAT_ACCEPTED`, `status == working`, `runId` propio y expiración futura.

### Liberación

```json
{
  "schemaVersion": 3,
  "commandId": "<único>",
  "operation": "release",
  "runId": "<propietario>",
  "completedAt": "<UTC>",
  "result": "PASS | PARTIAL | BLOCKED | NO-OP",
  "checkpointSha": "<último SHA remoto o null>",
  "note": "<resultado conciso y neutral>"
}
```

La liberación exige `LEASE_RELEASED`, `status == idle`, `runId == null` y `lastRunId` propio.

El comando `release` se envía solamente después de terminar todas las demás mutaciones remotas. Después de enviarlo, no vuelvas a editar el issue ni ningún otro recurso de `krestosa/Focal`.

## Adquisición y ejecución activa

Antes de analizar o mutar funcionalmente `krestosa/Focal`:

1. Leé primero el issue #7.
2. Ejecutá `inspect`.
3. Si existe una lease ajena futura, no envíes `acquire`:
   - terminá `NO-OP`;
   - no duermas esperando que finalice;
   - no inspecciones el trabajo funcional;
   - no crees rama, PR, comentario ni commit.
4. Si el estado está `idle`, enviá `acquire`.
5. Si el comando no se correlaciona, completá el protocolo de entrega resiliente. No reenvíes más de una vez ni asumas propiedad.
6. Solo comenzá otras lecturas y mutaciones después de confirmar propiedad.
7. Inmediatamente después de adquirir, enviá un heartbeat de fase `REMOTE_STATE_AUDIT` antes de comenzar el análisis profundo.

## Guardia previa a cada mutación

Antes de toda llamada mutadora al conector o a GitHub:

1. Releé el issue #7.
2. Verificá `status == working`.
3. Verificá que `runId` coincida exactamente con el propio.
4. Verificá que `leaseExpiresAt` sea futura y tenga al menos cinco minutos de margen.
5. Si el margen es menor, renová y esperá `HEARTBEAT_ACCEPTED`.
6. Si aparece `idle`, otro `runId`, `NOT_LEASE_OWNER` o una expiración insegura, detené la mutación.

Esta guarda aplica a archivos, ramas, commits, PRs, reviews, labels, merges, releases, documentación, roadmap y matriz.

## Recuperación de lock abandonado

Un lock es candidato a abandono únicamente cuando:

```text
status == working
y leaseExpiresAt <= hora UTC actual
```

Antes de `recover`:

1. Inspeccioná rama, PR, checkpoint y SHA registrados.
2. Inspeccioná workflows mutadores conocidos y su estado.
3. Verificá que no exista evidencia positiva de una ejecución todavía activa.
4. Preservá referencias al ciclo anterior.
5. Enviá `recover` con un `runId` nuevo.
6. Continuá solo con `LEASE_RECOVERED`.

La recuperación no autoriza descartar trabajo. La primera unidad debe reconciliar o preservar el estado previo.

## Pérdida de propiedad

Si recibís `NOT_LEASE_OWNER`, si el estado cambia a otro `runId`, si el issue aparece `idle` durante trabajo o si no podés confirmar renovación antes de una expiración insegura:

- detené inmediatamente nuevas lecturas funcionales y mutaciones;
- no mergees;
- no crees una lease ficticia para representar retrospectivamente trabajo ya iniciado;
- no liberes una lease ajena;
- conservá únicamente evidencia remota que ya exista;
- reportá `PARTIAL` o `BLOCKED` según exista trabajo remoto útil.

## Operación administrativa `cleanup_branches`

`cleanup_branches` mantiene la lógica de GitHub Actions y solo es válido cuando:

- el usuario lo autorizó expresamente;
- el issue ya muestra `idle`;
- no existe ninguna ejecución de desarrollo autorizada trabajando;
- no forma parte de un `FOCAL_CYCLE`;
- la lista de ramas fue revisada y `main` se preserva.

Si existe `status == working`, el workflow debe responder `ACTIVE_LEASE`. Una ejecución de desarrollo no puede liberar y luego ejecutar limpieza: `release` debe seguir siendo su última mutación.

## Workflow ausente o corrupto

Si el issue o el workflow falta o es inválido:

- no inicies desarrollo funcional;
- tratá la reparación como infraestructura prioritaria de `krestosa/Focal`;
- aplicá `COORDINATOR_REPAIR` únicamente cuando no exista lease activa verificable;
- realizá todas las lecturas y mutaciones mediante el conector de GitHub o GitHub Actions;
- usá ramas, PRs, workflows y commits de reparación solo como transporte temporal;
- no cambies lógica funcional ajena al defecto mínimo del coordinador;
- validá el árbol temporal, ejecutá la limpieza de historia mediante GitHub Actions y verificá que `main` no conserve commits de reparación alcanzables;
- continuá solo después de `STATE_OBSERVED` y una adquisición confirmada.

## GitHub Actions mutadoras

Todo workflow capaz de modificar código, ramas, PRs, releases o documentación funcional debe:

- declarar `concurrency.group: focal-autonomous-development`;
- usar `cancel-in-progress: false`;
- adquirir la misma lease del issue #7 antes de mutar;
- releer y confirmar propiedad antes de cada fase mutadora;
- liberar mediante un finalizador si conserva propiedad;
- no realizar mutaciones después de `release`.

El coordinador `Automation State Coordinator` es la única excepción: procesa comandos y no adquiere su propia lease. Debe aceptar `issues.edited`, `schedule` y `workflow_dispatch`, ser idempotente y no registrar procedencia del cliente.
