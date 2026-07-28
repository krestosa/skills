# Focal — Política vinculante de estado operativo fuera del historial Git

Esta política reemplaza completamente los mecanismos anteriores basados en:

- la rama `automation/runtime-state`;
- el archivo `automation/run-state.json`;
- commits operativos;
- comentarios acumulativos en issues;
- resultados publicados como comentarios.

Su objetivo es coordinar ejecuciones programadas, ejecuciones manuales y GitHub Actions sin contaminar el historial Git ni acumular elementos visibles en el issue de estado.

# Corrección 13 — Coordinador body-only mediante GitHub Issue y GitHub Actions

## Fuente canónica

La única fuente actual de coordinación es:

```text
Repositorio: krestosa/Focal
Issue: #7
Título esperado: [automation-state] Focal execution state
Workflow: .github/workflows/automation-state.yml
```

Los issues #2 y #5 son prototipos cerrados y obsoletos. No deben leerse, reabrirse ni utilizarse para coordinación.

La rama `automation/runtime-state` y `automation/run-state.json` son legado congelado. No representan el estado actual.

## Principio rector

El issue #7 mantiene en su cuerpo dos bloques JSON:

```text
<!-- focal-command:v3 -->
...
<!-- /focal-command -->
```

```text
<!-- focal-state:v3 -->
...
<!-- /focal-state -->
```

El bloque de comando contiene la solicitud más reciente.

El bloque de estado contiene:

- la lease actual;
- el propietario;
- la fase;
- los timestamps;
- la rama, PR y checkpoint;
- el resultado del último comando procesado;
- el resultado del último ciclo finalizado.

No se crean comentarios para adquirir, inspeccionar, renovar, cambiar de fase o liberar.

No se crean commits para ninguna transición operativa.

## Compatibilidad obligatoria con el conector de GitHub

La ejecución debe operar únicamente mediante acciones disponibles en el conector:

1. leer el issue #7;
2. conservar íntegramente su cuerpo actual;
3. reemplazar únicamente el objeto JSON del bloque `focal-command:v3`;
4. actualizar el cuerpo del mismo issue;
5. releer el issue hasta observar el resultado correlacionado en `focal-state:v3`;
6. leer ramas, PRs, commits, checks y workflows cuando corresponda.

No depende de GitHub CLI, `gh`, `curl`, secretos locales ni acceso de red directo desde la VM.

No publiques comentarios operativos en el issue.

No utilices `add_comment_to_issue` para este protocolo.

## Atomicidad y exclusión mutua

El workflow declara:

```yaml
concurrency:
  group: focal-automation-state
  cancel-in-progress: false
```

El workflow procesa las ediciones del issue #7 en forma serializada.

Para cada comando:

1. relee el cuerpo actual;
2. extrae el comando y el estado;
3. verifica `schemaVersion: 3`;
4. rechaza un `commandId` ya procesado;
5. valida lease, propietario y timestamps;
6. aplica o rechaza la operación;
7. actualiza el bloque de estado en el mismo cuerpo;
8. registra `lastCommandId`, `lastCommandAccepted`, `lastCommandReason` y `lastCommandProcessedAt`;
9. incrementa `version`.

La edición posterior realizada por el workflow puede disparar otro evento, pero el mismo `commandId` debe detectarse como ya procesado y no generar una nueva mutación.

## Regla de preservación del cuerpo

Antes de enviar un comando:

1. leé nuevamente el issue #7;
2. verificá que ambos bloques existan y sean JSON válidos;
3. conservá exactamente el texto fuera del bloque de comando;
4. conservá intacto el bloque de estado observado;
5. reemplazá únicamente el JSON entre los delimitadores del comando;
6. actualizá el cuerpo completo del issue con esa modificación puntual.

No reconstruyas el issue desde memoria.

No sobrescribas el estado con una versión vieja.

No elimines los delimitadores, el texto descriptivo ni campos desconocidos.

## Identidad de comandos

Cada operación usa un `commandId` único e irrepetible.

Debe ser suficientemente aleatorio o incluir UUID para impedir colisiones entre ejecuciones.

El comando usa:

```json
{
  "schemaVersion": 3,
  "commandId": "<identificador único>",
  "operation": "inspect | acquire | recover | heartbeat | release"
}
```

Toda operación excepto `inspect` requiere `runId`.

## Inspección

```json
{
  "schemaVersion": 3,
  "commandId": "<identificador único>",
  "operation": "inspect"
}
```

La inspección es exitosa cuando el estado observado contiene:

```text
lastCommandId == commandId enviado
lastCommandAccepted == true
lastCommandReason == STATE_OBSERVED
```

## Adquisición normal

```json
{
  "schemaVersion": 3,
  "commandId": "<identificador único>",
  "operation": "acquire",
  "runId": "<UUID v4>",
  "owner": "scheduled-run",
  "executionSource": "scheduled-run",
  "mode": "normal",
  "phase": "LOCK_ACQUISITION",
  "startedAt": "<UTC ISO-8601>",
  "heartbeatAt": "<UTC ISO-8601>",
  "leaseExpiresAt": "<UTC ISO-8601 futuro>",
  "softStopAt": "<UTC ISO-8601>",
  "cleanupAt": "<UTC ISO-8601>",
  "hardKillAt": "<UTC ISO-8601>",
  "deadlineAt": "<UTC ISO-8601>",
  "baseMainSha": "<SHA remoto actual>",
  "workBranch": null,
  "workBranchHeadSha": null,
  "pullRequest": null,
  "checkpointSha": null,
  "note": null
}
```

La ejecución posee la lease únicamente cuando el estado contiene simultáneamente:

```text
lastCommandId == commandId enviado
lastCommandAccepted == true
lastCommandReason == LEASE_ACQUIRED
status == working
runId == runId propio
leaseExpiresAt es futuro
```

Editar el issue no equivale a adquirir la lease.

## Recuperación

Usá el formato de adquisición con:

```json
{
  "operation": "recover",
  "mode": "recovery"
}
```

La confirmación exige `lastCommandReason == LEASE_RECOVERED`.

## Heartbeat y cambio de fase

```json
{
  "schemaVersion": 3,
  "commandId": "<identificador único>",
  "operation": "heartbeat",
  "runId": "<runId propietario>",
  "phase": "<fase actual>",
  "heartbeatAt": "<UTC ISO-8601>",
  "leaseExpiresAt": "<UTC ISO-8601 futuro>",
  "workBranch": "<rama o null>",
  "workBranchHeadSha": "<SHA o null>",
  "pullRequest": "<número o null>",
  "checkpointSha": "<SHA o null>",
  "note": null
}
```

La renovación es válida únicamente cuando:

```text
lastCommandId == commandId enviado
lastCommandAccepted == true
lastCommandReason == HEARTBEAT_ACCEPTED
runId == runId propio
leaseExpiresAt es futuro
```

Si aparece `NOT_LEASE_OWNER`, detené inmediatamente nuevas mutaciones funcionales.

## Liberación

```json
{
  "schemaVersion": 3,
  "commandId": "<identificador único>",
  "operation": "release",
  "runId": "<runId propietario>",
  "completedAt": "<UTC ISO-8601>",
  "result": "PASS | FAIL | INCOMPLETE | BLOCKED",
  "checkpointSha": "<último SHA remoto preservado o null>",
  "note": "<resultado conciso>"
}
```

La liberación es válida cuando:

```text
lastCommandId == commandId enviado
lastCommandAccepted == true
lastCommandReason == LEASE_RELEASED
status == idle
runId == null
lastRunId == runId propio
```

## Protocolo de espera

Después de editar el issue:

1. conservá el `commandId` enviado;
2. dormí entre 3 y 10 segundos;
3. releé el issue #7;
4. extraé el bloque de estado actual;
5. verificá si `lastCommandId` coincide;
6. si no coincide, repetí con sleep acotado;
7. no hagas busy-wait;
8. no publiques otro comando mientras el anterior siga sin resultado, salvo recuperación explícita de un timeout comprobado;
9. aplicá un límite conservador de intentos.

Una coincidencia de `lastCommandId` sin `lastCommandAccepted: true` es un rechazo, no una adquisición parcial.

`ACTIVE_LEASE` obliga a sleep mode o finalización conforme a la política de ejecución concurrente.

`COMMAND_ERROR` obliga a diagnosticar y reparar el comando o workflow como infraestructura interna.

## Heartbeats

Los heartbeats modifican únicamente el cuerpo del issue #7.

Mantené la frecuencia definida por el prompt general, evitando renovaciones redundantes en ciclos muy breves.

Cada heartbeat requiere confirmación correlacionada.

Si no puede confirmarse antes de que la lease sea insegura:

- no asumas renovación;
- detené nuevas mutaciones;
- preservá el trabajo remoto;
- liberá únicamente si el estado todavía reconoce la propiedad.

## Issue o workflow faltante

La ausencia o corrupción del issue #7 o del workflow no es un bloqueo ordinario.

Clasificala como infraestructura interna y:

1. verificá que no exista un coordinador equivalente vigente;
2. creá o repará el issue body-only;
3. creá o repará `.github/workflows/automation-state.yml` mediante rama y PR;
4. validá el workflow;
5. fusioná sin squash cuando los gates correspondan;
6. ejecutá un comando `inspect` de smoke test;
7. verificá que el issue siga con cero comentarios operativos;
8. continuá únicamente cuando el estado registre `STATE_OBSERVED`.

Las ejecuciones ordinarias no modifican `krestosa/skills`. Una migración deliberada del protocolo requiere una tarea específica autorizada.

## Legado congelado

No utilices:

```text
automation/runtime-state
automation/run-state.json
issue #2
issue #5
```

Reglas:

- no escribir heartbeats en la rama antigua;
- no crear commits operativos;
- no interpretar sus datos como actuales;
- no reabrir los issues obsoletos;
- no publicar nuevos comentarios allí;
- no fusionar la rama operativa con `main`.

## Historial y trazabilidad

El mecanismo actual conserva únicamente:

- el estado más reciente en el cuerpo del issue #7;
- el historial interno de ediciones del issue provisto por GitHub;
- los runs del workflow coordinador.

No conserva una secuencia visible de comentarios operativos.

No altera `main`, no ensucia ramas funcionales y no viola la política de un archivo por commit.

## GitHub Actions mutadoras

Todo workflow capaz de modificar código o estado funcional debe:

- respetar su grupo de concurrencia funcional;
- adquirir la misma lease del issue #7 antes de mutar;
- registrar una fuente de ejecución inequívoca;
- liberar mediante un finalizador cuando siga siendo propietario.

El workflow coordinador es la única excepción: administra la lease y no intenta adquirirla para procesar comandos.

## PASS y evidencia

La coordinación puede considerarse verificada cuando:

- el issue #7 fue leído;
- el comando fue escrito en el cuerpo preservando el estado observado;
- el estado registró el mismo `commandId`;
- `lastCommandAccepted` fue `true`;
- el `runId` coincide cuando corresponde;
- la lease es futura durante el trabajo;
- la liberación termina en `idle`;
- no se crearon commits ni comentarios operativos.

## Informe terminal ampliado

Añadí:

```text
Coordinador de estado: issue-body-backed
Issue de estado: #7
Workflow coordinador: Automation State Coordinator
Command ID de adquisición:
Resultado de adquisición:
State version adquirida:
Command ID del último heartbeat:
Resultado del último heartbeat:
Command ID de liberación:
Resultado de liberación:
Estado final observado en el issue:
Comentarios operativos creados: 0
Commits operativos creados: 0
Rama automation/runtime-state utilizada: no
```

## Regla de precedencia

Esta política reemplaza toda instrucción anterior que exija:

- modificar `automation/run-state.json`;
- crear commits para adquirir, renovar o liberar;
- usar compare-and-swap sobre un blob Git;
- usar comentarios para enviar comandos o resultados;
- leer el issue #2 o #5 como estado vigente;
- considerar la rama `automation/runtime-state` como fuente actual.

No reemplaza:

- límites de seguridad;
- hard killswitch;
- necesidad de exclusión mutua;
- propiedad verificable;
- preservación remota del trabajo;
- validación de PRs;
- prohibición de force push;
- política de no squash;
- reglas de procedencia.

Razonamiento: High
