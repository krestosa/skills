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

1. el issue canónico `#7` existe, conserva ambos bloques `v3` válidos y muestra `status == idle` con `runId == null`, o el issue/workflow falta y no existe evidencia positiva de una ejecución activa;
2. se escribió un comando `inspect` nuevo preservando el cuerpo cuando el issue era utilizable;
3. se completó la ventana de observación obligatoria y `lastCommandId` no se correlacionó, o existe un run o job terminal fallido asociado al comando, o el coordinador es estructuralmente ilegible;
4. no existe evidencia positiva de una lease activa, un workflow mutador activo o trabajo funcional concurrente;
5. la instrucción actual autoriza modificar `krestosa/Focal`.

No actives este modo por latencia ordinaria, una lease ajena, un comando rechazado correctamente, un fallo funcional del proyecto ni para evitar el protocolo normal.

## Canal de ejecución obligatorio

Toda lectura y mutación de `krestosa/Focal` durante `COORDINATOR_REPAIR` debe ejecutarse mediante:

- el conector de GitHub; o
- GitHub Actions instalado en el propio repositorio.

No uses clon local, Git local, API directa fuera del conector, shell remoto externo, proxy ni workspace persistente para modificar Focal.

## Alcance permitido sin lease

Mientras no exista propietario activo, se permite exclusivamente:

- leer el issue `#7`, la rama predeterminada y su SHA;
- leer `.github/workflows/automation-state.yml` y sus dependencias directas;
- inspeccionar runs, jobs y logs del coordinador asociados al comando fallido;
- leer y modificar tests específicos del coordinador;
- crear temporalmente una rama no forzada desde el SHA remoto observado;
- publicar temporalmente commits y una PR necesarios para validar el árbol reparado;
- usar un workflow temporal de GitHub Actions para plegar la reparación en la historia existente y retirar los commits de transporte;
- ejecutar después de la publicación un smoke test `inspect`, seguido opcionalmente por `acquire`, `heartbeat` y `release` con un run de diagnóstico corto.

Queda prohibido durante este modo:

- leer o modificar roadmap, matriz de Iris, shaders, tooling gráfico o documentación funcional no relacionada;
- seleccionar una feature;
- representar el trabajo como un `FOCAL_CYCLE` adquirido;
- editar directamente `focal-state:v3`;
- liberar una lease que no fue adquirida;
- continuar si aparece `status == working` o un propietario ajeno;
- dejar en `main` commits, merges, archivos, workflows, ramas o refs temporales de reparación alcanzables;
- cambiar la lógica funcional fuera del defecto mínimo verificado del coordinador;
- reescribir historia funcional no relacionada.

## Contrato de historia final sin commits de reparación

Los commits de reparación son transporte temporal, no parte del historial canónico.

Antes de finalizar `COORDINATOR_REPAIR`:

1. determiná el commit funcional previo cuyos metadatos deben preservarse;
2. determiná el árbol final validado que contiene el fix mínimo;
3. ejecutá mediante GitHub Actions una reescritura con `commit-tree` o mecanismo equivalente que:
   - use el árbol final validado;
   - conserve el parent funcional esperado;
   - conserve exactamente nombre y correo de autor;
   - conserve exactamente fecha de autor;
   - conserve exactamente nombre y correo de committer;
   - conserve exactamente fecha de committer;
   - conserve exactamente el mensaje del commit funcional elegido;
4. actualizá `main` mediante GitHub Actions con `--force-with-lease` contra el head temporal exacto;
5. verificá automáticamente que el árbol anterior validado y el árbol reescrito sean idénticos;
6. verificá que los commits y merges temporales de reparación ya no sean alcanzables desde `main`;
7. verificá que el workflow temporal no exista en el árbol final;
8. cerrá el issue disparador y eliminá ramas temporales cuando la operación disponible lo permita.

Esta reescritura es la única excepción al veto de force push y solo puede ejecutarse desde GitHub Actions para retirar infraestructura temporal. No autoriza al chat a ejecutar force push mediante el conector ni a modificar la historia de features ordinarias.

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
5. checks verdes del árbol y head temporales exactos;
6. publicación del árbol reparado y limpieza de toda historia temporal alcanzable;
7. verificación de árbol, parent, autor, committer, fechas, mensaje y ausencia del workflow temporal;
8. comando `inspect` nuevo observado durante la ventana obligatoria y correlacionado con `STATE_OBSERVED`;
9. cuando sea seguro, ciclo diagnóstico `acquire` → `heartbeat` → `release` que termine en `idle`, `runId == null`, `lastRunId` propio y `LEASE_RELEASED`.

Si el smoke test post-publicación falla, conservá únicamente las referencias remotas indispensables para recuperar la reparación y reportá `BLOCKED` por coordinador todavía inoperable. No inicies trabajo funcional.

## Retorno al ciclo normal

Una vez confirmado `STATE_OBSERVED` y verificada la limpieza de historia:

1. finalizá `COORDINATOR_REPAIR`;
2. releé el issue;
3. generá un `runId` de desarrollo nuevo;
4. retomá desde el gate cero normal;
5. no reutilices el run diagnóstico como ejecución funcional.

La reparación bootstrap no emite `release` salvo que haya adquirido explícitamente una lease de diagnóstico. Si nunca adquirió lease, el reporte debe indicar `Lock liberado: no adquirido`.
