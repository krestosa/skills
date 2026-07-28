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
- `runId`, `owner` y `executionSource`: propietario;
- `startedAt`, `heartbeatAt` y `leaseExpiresAt`: vigencia;
- `softStopAt`, `cleanupAt`, `hardKillAt` y `deadlineAt`: límites;
- `baseMainSha`: baseline observado;
- `workBranch`, `workBranchHeadSha`, `pullRequest` y `checkpointSha`: continuidad remota;
- `lastCompletedAt`, `lastResult` y `lastRunId`: último ciclo finalizado;
- `lastCommandId`, `lastCommandAccepted`, `lastCommandReason` y `lastCommandProcessedAt`: correlación del comando;
- campos adicionales desconocidos: conservarlos sin reinterpretarlos ni eliminarlos.

`status == working`, un `runId` ajeno y `leaseExpiresAt` futuro representan una ejecución activa. `status == idle` y `runId == null` representan ausencia de propietario.

## Identidad y lease

Cada ciclo crea un `runId` UUID v4 y un `commandId` único por operación.

Parámetros canónicos:

- lease inicial: 30 minutos;
- heartbeat: antes de 10 minutos desde el anterior;
- renovación adicional: antes de publicación, espera de CI, merge y cleanup;
- todos los timestamps: UTC ISO-8601;
- la lease solo existe cuando el bloque de estado confirma el mismo `commandId`, aceptación, razón esperada, `runId` propio y expiración futura.

Editar el issue no equivale a adquirir o renovar.

## Preservación del cuerpo

Para cada comando:

1. Releé el issue #7.
2. Validá ambos bloques y `schemaVersion: 3`.
3. Conservá exactamente todo el cuerpo fuera del JSON del bloque de comando.
4. Conservá intacto el bloque de estado observado y cualquier campo desconocido.
5. Reemplazá solo el JSON del bloque de comando.
6. Actualizá el cuerpo completo.
7. Esperá de 3 a 10 segundos y releé.
8. Correlacioná por `lastCommandId`.
9. Usá polling acotado; no busy-wait ni esperas indefinidas.
10. No crees comentarios operativos.

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
  "owner": "<identidad no secreta>",
  "executionSource": "<scheduled-chat|github-actions|manual>",
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

La adquisición exige `LEASE_ACQUIRED`, `status == working`, `runId` propio y expiración futura.

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

Exigí `HEARTBEAT_ACCEPTED`, `runId` propio y expiración futura.

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
  "note": "<resultado conciso>"
}
```

La liberación exige `LEASE_RELEASED`, `status == idle`, `runId == null` y `lastRunId` propio.

## Adquisición y ejecución activa

Antes de mutar `krestosa/Focal`:

1. Ejecutá `inspect`.
2. Si existe una lease ajena futura, no envíes `acquire`:
   - terminá `NO-OP`;
   - no duermas esperando que finalice;
   - no crees rama, PR, comentario ni commit.
3. Si el estado está `idle`, enviá `acquire`.
4. Si el comando no se correlaciona dentro del límite, releé el estado. No reenvíes a ciegas ni asumas propiedad.
5. Solo comenzá mutaciones después de confirmar propiedad.

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

Si recibís `NOT_LEASE_OWNER`, si el estado cambia a otro `runId` o si no podés confirmar renovación antes de una expiración insegura:

- detené nuevas mutaciones;
- no mergees;
- publicá únicamente un checkpoint ya preparado si puede hacerse sin riesgo;
- no liberes una lease ajena;
- ejecutá reconciliación con la evidencia disponible;
- reportá `PARTIAL` o `BLOCKED` según exista trabajo remoto útil.

## Workflow ausente o corrupto

Si el issue o el workflow falta o es inválido:

- no inicies desarrollo funcional;
- tratá la reparación como infraestructura prioritaria de `krestosa/Focal`;
- repará mediante rama y PR si no existe lease activa verificable;
- validá el workflow y ejecutá un `inspect`;
- continuá solo después de `STATE_OBSERVED`.

## GitHub Actions mutadoras

Todo workflow capaz de modificar código, ramas, PRs, releases o documentación funcional debe:

- declarar `concurrency.group: focal-autonomous-development`;
- usar `cancel-in-progress: false`;
- adquirir la misma lease del issue #7 antes de mutar;
- liberar mediante un finalizador si conserva propiedad.

El coordinador `Automation State Coordinator` es la única excepción: procesa comandos y no adquiere su propia lease.
