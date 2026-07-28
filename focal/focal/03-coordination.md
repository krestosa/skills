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

El cuerpo del issue es la única fuente de lease. El historial Git, ramas operativas, archivos JSON y comentarios no son estado activo.

## Estado legacy retirado

No leas, crees, actualices ni recuperes coordinación desde:

```text
automation/runtime-state
automation/run-state.json
issue #2
issue #5
```

No mantengas una ruta fallback hacia esos mecanismos. El historial puede documentar su existencia, pero no son ejecutables.

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

## Inspección y adquisición

Antes de mutar `krestosa/Focal`:

1. Enviá `inspect` y exigí:
   - `lastCommandAccepted == true`;
   - `lastCommandReason == STATE_OBSERVED`.
2. Si `status == working` y `leaseExpiresAt` es futuro para otro `runId`, no adquieras:
   - terminá `NO-OP`;
   - no duermas esperando que finalice;
   - no crees rama ni PR.
3. Si el estado está `idle`, enviá `acquire` con:
   - `runId`, owner y fuente;
   - límites temporales;
   - SHA actual de la rama predeterminada;
   - fase `LOCK_ACQUISITION`.
4. La adquisición es válida solo con:
   - `lastCommandReason == LEASE_ACQUIRED`;
   - `status == working`;
   - `runId` propio;
   - expiración futura.
5. Si el comando no se correlaciona dentro del límite, releé el estado. No reenvíes a ciegas ni asumas propiedad.

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
5. Enviá `recover` con un `runId` nuevo y `mode: recovery`.
6. Continuá solo con `LEASE_RECOVERED`.

La recuperación no autoriza descartar trabajo. La primera unidad debe reconciliar o preservar el estado previo.

## Heartbeat y pérdida de propiedad

Un heartbeat válido exige `HEARTBEAT_ACCEPTED`, `runId` propio y expiración futura.

Si recibís `NOT_LEASE_OWNER`, si el estado cambia a otro `runId` o si no podés confirmar renovación antes de una expiración insegura:

- detené nuevas mutaciones;
- no mergees;
- publicá únicamente un checkpoint ya preparado si puede hacerse sin riesgo;
- no liberes una lease ajena;
- ejecutá reconciliación con la evidencia disponible;
- reportá `PARTIAL` o `BLOCKED` según exista trabajo remoto útil.

## Liberación

Enviá `release` con:

- `runId` propietario;
- `completedAt`;
- resultado `PASS`, `PARTIAL`, `BLOCKED` o `NO-OP` cuando el workflow admita el valor; mientras el schema operativo conserve valores anteriores, usá el valor compatible más cercano y registrá el resultado terminal exacto en `note`;
- último checkpoint remoto;
- nota concisa.

La liberación se confirma solo con:

- `lastCommandReason == LEASE_RELEASED`;
- `status == idle`;
- `runId == null`;
- `lastRunId` igual al propio.

No crees comentarios ni commits operativos.

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
