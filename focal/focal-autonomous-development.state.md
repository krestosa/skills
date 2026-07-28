# Focal — Política vinculante de estado operativo fuera del historial Git

Esta política reemplaza el mecanismo anterior basado en la rama `automation/runtime-state` y el archivo `automation/run-state.json`.

Su objetivo es coordinar chats programados, chats manuales y GitHub Actions sin crear commits de adquisición, heartbeat, cambio de fase o liberación.

# Corrección 13 — Coordinador de lease basado en GitHub Issue y GitHub Actions

## Principio rector

El estado operativo no debe almacenarse mediante commits Git.

La fuente canónica de coordinación es:

```text
Repositorio: krestosa/Focal
Issue: #2
Título esperado: [automation-state] Focal autonomous execution coordinator
Workflow: .github/workflows/automation-state.yml
```

El issue contiene un bloque JSON delimitado por:

```text
<!-- focal-state:v1 -->
...
<!-- /focal-state -->
```

El workflow `Automation State Coordinator` procesa comandos enviados como comentarios y actualiza el bloque JSON del issue.

Las adquisiciones, heartbeats, cambios de fase, checkpoints y liberaciones no deben crear commits.

## Compatibilidad obligatoria con el conector de GitHub para ChatGPT

La ejecución debe utilizar únicamente operaciones disponibles mediante el conector:

- leer el issue #2;
- leer sus comentarios;
- publicar un comentario en el issue #2;
- leer ramas, PRs, commits y checks cuando corresponda.

No depende de acceso directo a `gh`, `curl`, GitHub CLI, REST desde la VM, secretos locales ni acceso de red directo.

El workflow utiliza `GITHUB_TOKEN` dentro de GitHub Actions para aplicar el comando de forma serializada.

## Atomicidad y exclusión mutua

La atomicidad ya no depende de compare-and-swap sobre un blob Git.

Depende de:

```yaml
concurrency:
  group: focal-automation-state
  cancel-in-progress: false
```

y de que el workflow:

1. procese un único comando por vez;
2. relea el estado actual del issue;
3. valide la lease y el propietario;
4. aplique o rechace el comando;
5. actualice el issue;
6. publique un resultado correlacionado.

Solo una adquisición puede ser aceptada cuando el estado es `idle` o la lease está vencida.

Una ejecución no posee el lock hasta recibir un resultado explícito con:

```json
{
  "accepted": true,
  "commandId": "<mismo commandId>",
  "reason": "LEASE_ACQUIRED",
  "runId": "<runId propio>",
  "status": "working"
}
```

Publicar el comentario no equivale a adquirir el lock.

## Formato de comandos

Todo comando debe comenzar exactamente con:

```text
<!-- focal-state-command:v1 -->
```

seguido por un objeto JSON, preferentemente dentro de un bloque `json`.

Cada comando debe incluir un `commandId` único e irrepetible.

### Inspección

```json
{
  "schemaVersion": 1,
  "commandId": "<uuid o identificador único>",
  "operation": "inspect"
}
```

### Adquisición normal

```json
{
  "schemaVersion": 1,
  "commandId": "<identificador único>",
  "operation": "acquire",
  "runId": "<UUID v4>",
  "owner": "scheduled-chat",
  "executionSource": "scheduled-chat",
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
  "note": "<nota opcional>"
}
```

### Recuperación

Utilizá el mismo formato que adquisición, con:

```json
{
  "operation": "recover",
  "mode": "recovery"
}
```

### Heartbeat o cambio de fase

```json
{
  "schemaVersion": 1,
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
  "note": "<nota opcional>"
}
```

### Liberación

```json
{
  "schemaVersion": 1,
  "commandId": "<identificador único>",
  "operation": "release",
  "runId": "<runId propietario>",
  "completedAt": "<UTC ISO-8601>",
  "result": "PASS | FAIL | INCOMPLETE | BLOCKED",
  "checkpointSha": "<último SHA remoto preservado o null>",
  "note": "<resultado conciso>"
}
```

## Formato de resultados

El workflow responde mediante un comentario que comienza con:

```text
<!-- focal-state-result:v1 -->
```

El resultado contiene, como mínimo:

```json
{
  "schemaVersion": 1,
  "commandId": "<commandId recibido>",
  "accepted": true,
  "reason": "<resultado>",
  "stateVersion": 1,
  "status": "idle | working",
  "runId": "<runId o null>",
  "leaseExpiresAt": "<timestamp o null>"
}
```

La ejecución debe buscar el resultado cuyo `commandId` coincida exactamente con el comando enviado.

No puede aceptar la respuesta de otro comando ni inferir aceptación por el paso del tiempo.

## Protocolo de espera compatible con ChatGPT

Después de publicar un comando:

1. conservá el ID del comentario cuando el conector lo devuelva;
2. dormí de 3 a 10 segundos;
3. releé los comentarios del issue #2;
4. buscá el resultado con el mismo `commandId`;
5. si no aparece, repetí con sleep acotado;
6. aplicá un máximo conservador de intentos y tiempo;
7. releé además el cuerpo del issue para distinguir retraso de respuesta y fallo real;
8. no hagas busy-wait.

Para adquisición, no realices mutaciones funcionales hasta obtener `accepted: true`.

Si recibe:

```text
ACTIVE_LEASE
```

entrá en sleep mode o finalizá conforme al protocolo de ejecución activa.

Si recibe:

```text
NOT_LEASE_OWNER
```

considerá perdida o inexistente la propiedad y detené nuevas mutaciones.

Si recibe:

```text
COMMAND_ERROR
```

inspeccioná y corregí el formato del comando o el workflow como infraestructura interna.

## Heartbeats

Los heartbeats se registran en el issue y sus comentarios, no en commits.

Mantené la frecuencia definida por el prompt general, pero evitá heartbeats redundantes cuando una operación breve termine antes del siguiente intervalo.

Cada heartbeat debe recibir confirmación explícita.

Si no puede confirmarse:

- releé el estado del issue;
- no asumas renovación;
- detené nuevas mutaciones si la lease puede expirar;
- preservá el trabajo remoto;
- liberá solo cuando siga siendo propietario.

## Issue y workflow faltantes

La ausencia del issue #2 o del workflow no es un motivo ordinario de intervención.

Clasificala como infraestructura interna y:

1. verificá que no exista un coordinador equivalente;
2. creá o repará el issue;
3. creá o repará `.github/workflows/automation-state.yml` mediante rama y PR;
4. validá el workflow;
5. fusioná sin squash cuando los gates correspondan;
6. ejecutá un comando `inspect` de smoke test;
7. continuá únicamente cuando el workflow responda correctamente.

Si el issue fue reemplazado deliberadamente, actualizá esta política en `krestosa/skills` únicamente mediante una tarea autorizada específica; las ejecuciones ordinarias de Focal no modifican `krestosa/skills`.

## Rama operativa anterior

La rama:

```text
automation/runtime-state
```

y el archivo:

```text
automation/run-state.json
```

quedan declarados como legado congelado.

Reglas obligatorias:

- no utilizarlos para adquirir o liberar el lock;
- no escribir nuevos heartbeats allí;
- no crear commits operativos allí;
- no interpretarlos como estado actual;
- no fusionar esa rama con `main`;
- conservarlos únicamente como evidencia histórica hasta que puedan eliminarse mediante una operación autorizada y segura;
- el issue #2 y su workflow tienen precedencia completa.

## Historial y trazabilidad

Este mecanismo no crea commits de estado.

Sí conserva una auditoría operativa fuera de Git mediante:

- historial de edición del issue;
- comentarios de comandos;
- comentarios de resultados;
- runs del workflow coordinador.

Esta auditoría no forma parte del historial de código, no altera `main`, no ensucia ramas funcionales y no viola la política de un archivo por commit.

## GitHub Actions mutadoras

Todo workflow capaz de modificar código o estado funcional debe:

- respetar su grupo de concurrencia funcional;
- adquirir la misma lease del issue #2 antes de mutar;
- utilizar `executionSource: github-actions`;
- liberar mediante un finalizador cuando siga siendo propietario.

El workflow coordinador de estado es la única excepción: administra la lease y por definición no debe intentar adquirirla para procesar comandos.

## PASS y evidencia

Una ejecución puede considerar verificada la coordinación cuando:

- el issue fue leído;
- el comando de adquisición recibió resultado correlacionado;
- `accepted` fue `true`;
- el `runId` coincide;
- el estado quedó `working`;
- la lease es futura;
- la liberación posterior recibió `LEASE_RELEASED` o el cuerpo del issue confirma el estado final esperado.

No es necesario crear ni inspeccionar commits operativos.

## Informe terminal ampliado

Añadí:

```text
Coordinador de estado: issue-backed
Issue de estado: #2
Workflow coordinador: Automation State Coordinator
Command ID de adquisición:
Resultado de adquisición:
State version adquirida:
Command ID del último heartbeat:
Resultado del último heartbeat:
Command ID de liberación:
Resultado de liberación:
Estado final observado en el issue:
Commits operativos creados: 0
Rama automation/runtime-state utilizada: no
```

## Regla de precedencia

Esta política reemplaza toda instrucción anterior que exija:

- modificar `automation/run-state.json`;
- crear commits para adquirir, renovar o liberar;
- usar el SHA de un blob operativo como compare-and-swap;
- considerar la rama `automation/runtime-state` como fuente actual;
- ensuciar el historial Git con estado efímero.

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
