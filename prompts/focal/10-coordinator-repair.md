# Focal — Reparación bootstrap del coordinador

Este módulo define la única excepción al gate de lease cuando el propio coordinador impide obtenerla. No autoriza desarrollo funcional sin exclusión mutua.

## Activación estricta

Entrá en `COORDINATOR_REPAIR` únicamente cuando se cumplan simultáneamente:

1. el issue canónico `#7` existe, conserva ambos bloques `v3` válidos y muestra `status == idle` con `runId == null`;
2. se escribió un comando `inspect` nuevo preservando el cuerpo;
3. después de polling acotado, `lastCommandId` no se correlacionó con ese comando o el workflow produjo un error verificable;
4. no existe evidencia positiva de una lease activa, un workflow mutador activo o trabajo funcional concurrente;
5. la instrucción actual autoriza modificar `krestosa/Focal`.

No actives este modo por latencia ordinaria, una lease ajena, un comando rechazado correctamente, un fallo funcional del proyecto ni para evitar el protocolo normal.

## Alcance permitido sin lease

Mientras el issue siga `idle`, se permite exclusivamente:

- leer el issue `#7`, la rama predeterminada y su SHA;
- leer `.github/workflows/automation-state.yml` y sus dependencias directas;
- inspeccionar runs, jobs y logs del coordinador asociados al comando fallido;
- leer y modificar tests específicos del coordinador;
- crear una rama no forzada desde el SHA remoto observado;
- publicar commits, abrir una PR y corregir únicamente el coordinador;
- mergear la reparación cuando los checks aplicables estén verdes y el head sea exacto;
- ejecutar después del merge un smoke test `inspect`, seguido opcionalmente por `acquire` y `release` con un run de diagnóstico corto.

Queda prohibido durante este modo:

- leer o modificar roadmap, matriz de Iris, shaders, tooling gráfico o documentación funcional no relacionada;
- seleccionar una feature;
- representar el trabajo como un `FOCAL_CYCLE` adquirido;
- editar directamente `focal-state:v3`;
- liberar una lease que no fue adquirida;
- continuar si aparece `status == working` o un propietario ajeno.

## Compatibilidad con GitHub Apps

El coordinador debe aceptar comandos emitidos mediante usuarios autorizados y GitHub Apps instaladas con permiso para editar el issue.

No hardcodees una allowlist de `sender.login` limitada al propietario o a `github-actions[bot]`. Ese patrón bloquea conectores autorizados y deja comandos sin correlación.

La frontera de confianza debe basarse en:

- evento `issues.edited` del issue exacto `#7`;
- capacidad otorgada por GitHub para editar ese issue;
- esquema y operación permitidos;
- correlación por `commandId`;
- invariantes de estado y propiedad de lease;
- `concurrency.group: focal-automation-state` con `cancel-in-progress: false`;
- idempotencia cuando `lastCommandId == commandId`.

Registrar el sender para auditoría es válido; rechazar por un conjunto fijo de logins no lo es.

## Diagnóstico obligatorio

Determiná una causa verificable antes de editar. Revisá, según disponibilidad:

- trigger `issues: types: [edited]`;
- condición exacta del issue `#7`;
- permisos `issues: write` y los permisos adicionales realmente usados;
- filtros de actor o sender;
- checkout o disponibilidad de scripts;
- sintaxis YAML y Python;
- errores de API, timeouts y códigos de salida;
- recursión idempotente causada por la edición que hace el propio workflow;
- vigencia del workflow en la rama predeterminada.

No reemplaces el coordinador por escritura directa del bloque de estado.

## Validación mínima

La reparación exige:

1. tests unitarios para `inspect`, `acquire`, lease ajena, `heartbeat`, `release` e idempotencia;
2. test o aserción que impida reintroducir una allowlist fija de sender;
3. validación YAML y del repositorio;
4. checks verdes del head exacto;
5. merge a la rama predeterminada;
6. comando `inspect` nuevo correlacionado con `STATE_OBSERVED`;
7. cuando sea seguro, ciclo diagnóstico `acquire` → `release` que termine en `idle`, `runId == null`, `lastRunId` propio y `LEASE_RELEASED`.

Si el smoke test post-merge falla, conservá la PR o una nueva rama de reparación y reportá `BLOCKED` por coordinador todavía inoperable. No inicies trabajo funcional.

## Retorno al ciclo normal

Una vez confirmado `STATE_OBSERVED`:

1. finalizá `COORDINATOR_REPAIR`;
2. releé el issue;
3. generá un `runId` de desarrollo nuevo;
4. retomá desde el gate cero normal;
5. no reutilices el run diagnóstico como ejecución funcional.

La reparación bootstrap no emite `release` salvo que haya adquirido explícitamente una lease de diagnóstico. Si nunca adquirió lease, el reporte debe indicar `Lock liberado: no adquirido`.
