# Focal — Reparación bootstrap del coordinador

Este módulo define la única excepción al gate de lease cuando el propio coordinador impide obtenerla. No autoriza desarrollo funcional sin exclusión mutua.

## Ventana de observación obligatoria

Antes de diagnosticar que un comando no fue procesado:

1. registrá la hora UTC y, cuando exista, un reloj monotónico inmediatamente después de actualizar el issue;
2. esperá tiempo real entre lecturas; las llamadas consecutivas sin demora no constituyen polling válido;
3. releé cada 5 a 10 segundos durante al menos 45 segundos de tiempo transcurrido total;
4. si el run del coordinador está `queued`, `in_progress`, `waiting` o `pending`, continuá observando dentro del presupuesto del ciclo;
5. solo podés abreviar la ventana cuando un run o job del coordinador ya terminó con fallo, cancelación o error verificable asociado al comando;
6. no midas la espera por cantidad de tool calls, respuestas o intentos, sino por tiempo UTC o monotónico realmente transcurrido;
7. si el entorno no permite esperar o confirmar el tiempo transcurrido, no diagnostiques una avería: terminá `BLOCKED` por observación insuficiente.

La latencia normal de GitHub Actions no activa `COORDINATOR_REPAIR`.

## Activación estricta

Entrá en `COORDINATOR_REPAIR` únicamente cuando se cumplan simultáneamente:

1. el issue canónico `#7` existe, conserva ambos bloques `v3` válidos y muestra `status == idle` con `runId == null`;
2. se escribió un comando `inspect` nuevo preservando el cuerpo;
3. se completó la ventana de observación obligatoria y `lastCommandId` no se correlacionó, o existe un run o job terminal fallido asociado al comando;
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

No hardcodees una allowlist de `sender.login` limitada al propietario o a `github-actions[bot]`. Ese patrón puede bloquear conectores autorizados y dejar comandos sin correlación.

La frontera de confianza debe basarse en:

- evento `issues.edited` del issue exacto `#7`;
- capacidad otorgada por GitHub para editar ese issue;
- esquema y operación permitidos;
- correlación por `commandId`;
- invariantes de estado y propiedad de lease;
- `concurrency.group: focal-automation-state` con `cancel-in-progress: false`;
- idempotencia cuando `lastCommandId == commandId`.

Registrar el sender para auditoría es válido; rechazar por un conjunto fijo de logins no lo es salvo que exista una fuente de identidad dinámica, verificable y compatible con las GitHub Apps autorizadas.

## Diagnóstico obligatorio

Determiná una causa verificable antes de editar. Revisá, según disponibilidad:

- tiempo real entre la escritura del comando y las lecturas posteriores;
- run, job y logs asociados al evento `issues.edited`;
- trigger `issues: types: [edited]`;
- condición exacta del issue `#7`;
- permisos `issues: write` y los permisos adicionales realmente usados;
- filtros de actor o sender;
- checkout, `PYTHONPATH`, modo de invocación y disponibilidad de scripts;
- sintaxis YAML y Python;
- errores de API, imports, timeouts y códigos de salida;
- recursión idempotente causada por la edición que hace el propio workflow;
- vigencia del workflow en la rama predeterminada.

No reemplaces el coordinador por escritura directa del bloque de estado.

## Validación mínima

La reparación exige:

1. tests unitarios para `inspect`, `acquire`, lease ajena, `heartbeat`, `release` e idempotencia;
2. test o aserción que impida reintroducir una allowlist fija de sender incompatible con conectores autorizados;
3. test del modo real de invocación del script o módulo, incluidos imports y `PYTHONPATH` cuando correspondan;
4. validación YAML y del repositorio;
5. checks verdes del head exacto;
6. merge a la rama predeterminada;
7. comando `inspect` nuevo observado durante la ventana obligatoria y correlacionado con `STATE_OBSERVED`;
8. cuando sea seguro, ciclo diagnóstico `acquire` → `release` que termine en `idle`, `runId == null`, `lastRunId` propio y `LEASE_RELEASED`.

Si el smoke test post-merge falla, conservá la PR o una nueva rama de reparación y reportá `BLOCKED` por coordinador todavía inoperable. No inicies trabajo funcional.

## Retorno al ciclo normal

Una vez confirmado `STATE_OBSERVED`:

1. finalizá `COORDINATOR_REPAIR`;
2. releé el issue;
3. generá un `runId` de desarrollo nuevo;
4. retomá desde el gate cero normal;
5. no reutilices el run diagnóstico como ejecución funcional.

La reparación bootstrap no emite `release` salvo que haya adquirido explícitamente una lease de diagnóstico. Si nunca adquirió lease, el reporte debe indicar `Lock liberado: no adquirido`.
