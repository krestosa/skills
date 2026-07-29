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

## Reenvío y fallback previos a la reparación

Antes de entrar en reparación por un comando no correlacionado:

1. confirmá que el issue sigue `idle`, `runId == null` y que el comando no fue procesado;
2. reenviá una sola vez la misma operación con `commandId` nuevo y timestamps recalculados;
3. completá otra ventana de 45 segundos reales;
4. verificá que `.github/workflows/automation-state.yml` admita:
   - `issues: types: [edited]`;
   - `schedule` cada cinco minutos;
   - `workflow_dispatch`;
   - ejecución para eventos sin `github.event.issue`;
5. si el fallback programado existe y quedan al menos diez minutos, observá hasta seis minutos desde el segundo envío;
6. si el comando se procesa dentro de esa ventana, continuá normalmente y no clasifiques el retraso como avería;
7. si la adquisición se procesa después de que el llamador ya terminó, liberá la lease huérfana con el mismo `runId` y una nota neutral; no inicies trabajo retrospectivo.

No entres en reparación mientras el reenvío o el fallback aplicable sigan pendientes.

## Activación estricta

Entrá en `COORDINATOR_REPAIR` únicamente cuando se cumplan simultáneamente:

1. el issue canónico `#7` existe, conserva ambos bloques `v3` válidos y muestra `status == idle` con `runId == null`, o el issue/workflow falta y no existe evidencia positiva de una ejecución activa;
2. se escribió un comando nuevo preservando el cuerpo cuando el issue era utilizable;
3. se agotaron la ventana inicial, el reenvío único y el fallback programado aplicable sin correlación, o existe un run o job terminal fallido asociado al comando, o el coordinador es estructuralmente ilegible;
4. no existe evidencia positiva de una lease activa, un workflow mutador activo o trabajo funcional concurrente;
5. la instrucción actual autoriza modificar `krestosa/Focal`.

No actives este modo por latencia ordinaria, una lease ajena, un comando rechazado correctamente, un fallo funcional del proyecto ni para evitar el protocolo normal.

## Safeguard del canal durante la reparación

Un fallo transitorio del conector durante `COORDINATOR_REPAIR` no demuestra que el coordinador esté roto ni habilita abandonar la reparación.

1. Reintentá la misma lectura o mutación hasta cuatro intentos totales con backoff de 2, 5, 10 y 20 segundos.
2. Para toda mutación con respuesta de error, hacé `read-after-write` y verificá árbol, ref, issue, PR o workflow antes de repetir.
3. Conservá el mismo payload, SHA esperado e identificador idempotente mientras el resultado sea desconocido.
4. No crees una segunda reparación paralela ni reescribas historia para compensar un error no confirmado.
5. Solo clasificá `CONNECTOR_RETRY_EXHAUSTED` después de agotar reintentos y verificaciones; preservá cualquier rama o PR recuperable y retomá desde allí en la siguiente ejecución.

## Canal de ejecución obligatorio

Toda lectura y mutación de `krestosa/Focal` durante `COORDINATOR_REPAIR` debe ejecutarse mediante:

- el conector de GitHub; o
- GitHub Actions instalado en el propio repositorio.

No uses clon local, Git local, API directa fuera del conector, shell remoto externo, proxy ni workspace persistente para modificar Focal.

## Privacidad operativa

La reparación no debe registrar el cliente que emitió los comandos.

- No leas ni imprimas `sender.login` salvo que sea indispensable para demostrar un filtro defectuoso; si se inspecciona, no lo copies a archivos, logs nuevos, PRs, notas ni reportes.
- No agregues campos `owner`, `executionSource`, `client`, `provider`, `model`, `agent`, `actor` o `sender` al contrato.
- Eliminá campos legacy de procedencia del estado en la siguiente transición válida.
- Los tests deben usar valores neutrales y comprobar ausencia de nombres de proveedor, modelo, aplicación, conector y plataforma de conversación.
- La auditoría interna de GitHub no es contenido controlado por el repositorio y no puede prometerse su eliminación.

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
- liberar una lease que no fue adquirida, salvo la lease huérfana tardía identificada inequívocamente por el mismo `runId` de la ejecución ya terminada;
- continuar si aparece `status == working` con un `runId` ajeno;
- dejar en `main` commits, merges, archivos, workflows, ramas o refs temporales de reparación alcanzables;
- cambiar la lógica funcional fuera del defecto mínimo verificado del coordinador;
- reescribir historia funcional no relacionada.

## Contrato de historia final sin commits de reparación

Los commits de reparación, transporte, archivos vacíos y no-op no forman parte del historial canónico. La limpieza es una reescritura probada, no una eliminación por heurística.

### Clasificación obligatoria

Antes de excluir un SHA, reuní evidencia suficiente:

- `NOOP_COMMIT`: commit de un solo parent y `tree(commit) == tree(parent)`;
- `EMPTY_ARTIFACT_COMMIT`: el diff se limita a archivos de cero bytes en rutas temporales o de transporte, sin contenido funcional, cambios de modo, renames, submódulos ni efectos laterales;
- `FAILED_TRANSPORT_COMMIT`: existe un run fallido correlacionado, el diff está limitado a infraestructura temporal y el replay sin ese commit produce el árbol funcional esperado;
- commits que no cumplen exactamente una clase permanecen intactos.

El mensaje, el autor, la hora, el nombre de rama o el estado del run nunca bastan solos. No excluyas commits firmados, asociados a una release, alcanzables por tags, compartidos por ramas protegidas, usados por otro PR o funcionalmente necesarios. No atravieses un merge sin mapear todos sus parents y demostrar topología equivalente.

### Reescritura mediante GitHub Actions

Antes de finalizar `COORDINATOR_REPAIR`:

1. fijá `expectedOldHead`, el último parent limpio, el árbol funcional validado y la lista cerrada de candidatos con evidencia;
2. ejecutá exclusivamente mediante GitHub Actions; no uses force push local ni una mutación directa del conector;
3. trabajá en un checkout completo y reconstruí la cadena en orden topológico:
   - omití los candidatos;
   - para cada commit posterior conservado, reaplicá su diff exacto contra el nuevo parent y calculá un árbol nuevo;
   - conservá exactamente nombre y correo de autor mediante `GIT_AUTHOR_NAME` y `GIT_AUTHOR_EMAIL`;
   - conservá exactamente fecha y timezone de autor mediante `GIT_AUTHOR_DATE` tomada del commit original;
   - conservá exactamente nombre y correo de committer mediante `GIT_COMMITTER_NAME` y `GIT_COMMITTER_EMAIL`;
   - conservá exactamente fecha y timezone de committer mediante `GIT_COMMITTER_DATE` tomada del commit original;
   - conservá exactamente el mensaje y, cuando esté soportado, la topología de parents;
   - creá cada commit reconstruido con `git commit-tree` o un mecanismo equivalente que permita fijar esos metadatos;
4. no asignes a commits posteriores la hora del workflow o de la limpieza: su cronología debe ser la misma que tenían antes de retirar los candidatos;
5. verificá para cada commit conservado que su diff semántico respecto del nuevo parent equivale al diff original y que el árbol final coincide con el árbol funcional validado;
6. si el tramo contiene merges y no puede reconstruirse cada parent, abortá antes de cambiar refs;
7. actualizá la ref objetivo con `--force-with-lease` contra `expectedOldHead`; si cambió, abortá y reconstruí desde el nuevo estado en otra ejecución;
8. no crees una rama remota de backup ni un tag de backup. La evidencia vive en el run y en los SHAs observados, no en refs persistentes;
9. retirá del árbol final el workflow y los scripts temporales antes de calcular el commit final;
10. eliminá mediante la misma Action todas las ramas y tags temporales creados para el transporte. El paso de eliminación debe ejecutarse con `if: always()` cuando sea seguro, incluso si la validación o el push fallan;
11. verificá que ningún candidato ni commit temporal sea alcanzable desde `refs/heads/*` o `refs/tags/*`, que no exista workflow temporal y que no haya un commit o merge de limpieza en la cadena final;
12. verificá parent, árbol, autor, committer, `authorDate`, `committerDate`, timezone y mensaje de cada commit posterior reconstruido;
13. solo entonces continuá con el smoke test y el retorno al ciclo normal.

Si el candidato está en el tip y no hay commits posteriores, la Action puede mover la ref al último parent limpio únicamente cuando ese árbol sea exactamente el árbol final validado. Si la Action falla antes del cambio de ref, la ref objetivo debe permanecer intacta y toda rama temporal debe eliminarse; no publiques un commit compensatorio.

Esta reescritura es la única excepción al veto de force push y solo puede ejecutarse desde GitHub Actions para retirar artefactos probados. No autoriza reescribir features ordinarias ni ocultar cambios funcionales. La auditoría interna de la plataforma puede conservar eventos u objetos no alcanzables; el criterio verificable es ausencia desde las refs visibles y el árbol controlado por el repositorio.

## Compatibilidad con GitHub Apps y entrega de eventos

El coordinador debe aceptar comandos emitidos mediante usuarios autorizados y GitHub Apps instaladas con permiso para editar el issue.

No hardcodees una allowlist de `sender.login` limitada al propietario o a `github-actions[bot]`. Ese patrón puede bloquear conectores autorizados y dejar comandos sin correlación.

La frontera de confianza debe basarse en:

- evento `issues.edited` del issue exacto `#7`;
- fallback `schedule` cada cinco minutos;
- fallback manual `workflow_dispatch`;
- capacidad otorgada por GitHub para editar ese issue;
- esquema y operación permitidos;
- correlación por `commandId`;
- invariantes de estado y propiedad de lease;
- `concurrency.group: focal-automation-state` con `cancel-in-progress: false`;
- idempotencia cuando `lastCommandId == commandId`.

No registres el sender dentro de los artefactos del repositorio. GitHub conserva su propia auditoría de eventos.

## Diagnóstico obligatorio

Determiná una causa verificable antes de editar. Revisá, según disponibilidad:

- tiempo real entre la escritura del comando y las lecturas posteriores;
- si el comando terminó procesándose con retraso;
- run, job y logs asociados al evento `issues.edited`;
- presencia y funcionamiento del run programado de fallback;
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
3. test que rechace campos de procedencia y depure campos legacy del estado;
4. test del modo real de invocación del script o módulo, incluidos imports y `PYTHONPATH` cuando correspondan;
5. test del fallback `schedule` y `workflow_dispatch`;
6. validación YAML y del repositorio;
7. checks verdes del árbol y head temporales exactos;
8. publicación del árbol reparado y limpieza de toda historia temporal alcanzable;
9. verificación de árbol, parent, autor, committer, fechas, mensaje y ausencia del workflow temporal;
10. tests o aserciones para `NOOP_COMMIT`, `EMPTY_ARTIFACT_COMMIT` y `FAILED_TRANSPORT_COMMIT`, incluida la prohibición de clasificar por mensaje solamente;
11. prueba de replay que conserve `GIT_AUTHOR_DATE` y `GIT_COMMITTER_DATE` de todos los commits posteriores y produzca el árbol esperado;
12. prueba de `--force-with-lease`, ausencia de candidatos en `refs/heads/*` y `refs/tags/*`, eliminación de ramas temporales y ausencia de commit de limpieza;
13. comando `inspect` nuevo observado durante la ventana obligatoria y correlacionado con `STATE_OBSERVED`;
14. cuando sea seguro, ciclo diagnóstico `acquire` → `heartbeat` → `release` que termine en `idle`, `runId == null`, `lastRunId` propio y `LEASE_RELEASED`.

Si el smoke test post-publicación falla, conservá únicamente las referencias remotas indispensables para recuperar la reparación y reportá `BLOCKED` por coordinador todavía inoperable. No inicies trabajo funcional.

## Retorno al ciclo normal

Una vez confirmado `STATE_OBSERVED` y verificada la limpieza de historia:

1. finalizá `COORDINATOR_REPAIR`;
2. releé el issue;
3. generá un `runId` de desarrollo nuevo;
4. retomá desde el gate cero normal;
5. no reutilices el run diagnóstico como ejecución funcional.

La reparación bootstrap no emite `release` salvo que haya adquirido explícitamente una lease de diagnóstico o deba sanear una adquisición tardía inequívoca. Si nunca adquirió lease, el reporte debe indicar `Lock liberado: no adquirido`.
