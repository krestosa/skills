# Focal — Catálogo y motor de recuperación autónoma

Este módulo es normativo. Define cómo diagnosticar, reparar y reanudar ante cualquier fallo conocido o futuro sin trasladar al usuario problemas internos resolubles.

## Principio de autonomía cerrada

Toda condición se procesa mediante `AUTONOMOUS_RECOVERY_LOOP`. Un error interno, una ausencia implementable, una inconsistencia de archivos, un fallo de CI o una rotura de tooling no autoriza pedir instrucciones ordinarias ni abandonar la tarea.

Solo puede solicitarse intervención cuando, después de agotar rutas autorizadas y documentar evidencia, falta exactamente una de estas capacidades externas no derivables:

- una credencial o permiso que no puede obtener el conector ni GitHub Actions;
- una autorización que amplía el repositorio o el alcance expresamente permitido;
- una decisión legal, contractual o irreversible que no puede inferirse del roadmap, código, documentación o políticas existentes;
- acceso físico a hardware o a un servicio externo obligatorio sin fallback seguro;
- una restricción de seguridad que impide cualquier alternativa autorizada.

La solicitud, cuando sea inevitable, debe limitarse al dato o autorización exactos. Nunca se pide al usuario diagnosticar, elegir entre alternativas técnicas ordinarias, reparar CI, decidir arquitectura ni repetir información observable remotamente.

## `AUTONOMOUS_RECOVERY_LOOP`

Ante cualquier fallo:

1. **Detectar y aislar.** Detené únicamente las operaciones que dependan del resultado fallido. No descartes trabajo válido ni cierres recursos útiles.
2. **Releer autoridad remota.** Volvé a observar issue, ref, commit, PR, run, archivo o release afectado. Una excepción local no prueba el estado remoto.
3. **Clasificar.** Usá el código más específico del README. Si ninguno aplica, usá `UNCLASSIFIED_INTERNAL_FAILURE`; nunca inventes éxito ni conviertas lo desconocido directamente en `BLOCKED`.
4. **Reunir evidencia mínima.** Capturá operación, SHA o identificador, precondición, error, logs, diff, árbol, timestamps y estado autoritativo necesarios para reproducir.
5. **Elegir la ruta más baja de la escalera.** Aplicá la primera alternativa segura que pueda resolver la causa.
6. **Ejecutar el fix mínimo completo.** Corregí causa y efectos derivados; no tapes el error con precedencia, reintentos infinitos, archivos dummy o desactivación de pruebas.
7. **Validar el artefacto exacto.** Repetí la operación fallida y todas las pruebas invalidadas sobre el head, árbol, run o binario exactos.
8. **Reanudar desde la primera fase invalidada.** No reinicies todo si existe un checkpoint coherente, pero tampoco saltes gates afectados.
9. **Registrar aprendizaje operativo.** Añadí test de regresión o evidencia equivalente. Si el fallo no estaba catalogado y el modo autoriza `krestosa/skills`, incorporá el nuevo código al catálogo y al README en la misma unidad.
10. **Preservar continuidad.** Si una contingencia real consume el presupuesto después de producir avance útil, publicá checkpoint, rama y PR recuperables, reconciliá estados y dejá que la siguiente ejecución continúe la misma tarea. No planifiques el checkpoint como objetivo ni lo uses para sustituir una unidad pequeña que podía completarse.

## Escalera obligatoria de recuperación

Aplicá en orden y detente en la primera ruta que resuelva con evidencia:

1. `RECOVERY_RETRY`: reintento acotado con backoff para un fallo transitorio.
2. `RECOVERY_READ_AFTER_WRITE`: reconciliación de una mutación de resultado desconocido.
3. `RECOVERY_ALTERNATE_ROUTE`: operación equivalente autorizada mediante otro endpoint, lectura, workflow o herramienta ya disponible.
4. `RECOVERY_REPAIR_IN_PLACE`: reparación de archivo, script, workflow, test, configuración, dependencia o documentación dentro del alcance.
5. `RECOVERY_RECONSTRUCT_REMOTE`: reconstrucción desde refs, commits, PRs, artifacts y checkpoints remotos verificados.
6. `RECOVERY_HISTORY_SANITATION`: exclusión probada de commits o archivos basura mediante GitHub Actions, preservando historia funcional.
7. `RECOVERY_SAFE_DEGRADATION`: fallback técnicamente válido, reversible y documentado que mantiene aceptación esencial; el roadmap queda `REVALIDAR` cuando corresponda.
8. `RECOVERY_CHECKPOINT_NEXT_CYCLE`: publicación de un estado remoto coherente para que la siguiente ejecución retome sin duplicar trabajo.
9. `RECOVERY_EXTERNAL_ESCALATION`: último recurso, únicamente bajo una condición externa no resoluble definida arriba.

No ejecutes la misma estrategia fallida indefinidamente. Después de dos intentos de reparación con la misma hipótesis causal, reuní evidencia nueva y cambiá de hipótesis o ruta.

## Fallos de selección y granularidad

- `ROADMAP_GRANULARITY_FAILURE`: existen ítems `PENDIENTE`, `EN PROGRESO` o `REVALIDAR`, pero la ejecución no produjo un incremento vertical utilizable. Repará el roadmap, completá `WORK_SELECTION_PROOF` y ejecutá el primer slice.
- `WORK_SELECTION_PROOF_MISSING`: no se evaluaron al menos tres candidatos —o todos los restantes— con dependencias, resultado mínimo, validación, presupuesto y código de descarte. Volvé a la fase de selección.
- `NOOP_REASON_INVALID`: se intentó terminar `NO-OP` con una razón fuera del conjunto cerrado. Reclasificá y reanudá; no liberes como `NO-OP` por complejidad o incertidumbre.
- `NOOP_REASON_REPEATED`: dos ciclos consecutivos repiten un `NO-OP` de selección mientras el roadmap conserva trabajo activo. Cambiá la hipótesis, descomponé la primera prioridad y ejecutala.

`NO_VALID_UNIT`, `NO_BOUNDED_INCREMENT`, “no se encontró un incremento seguro” y equivalentes quedan retirados como causas terminales: son aliases de `ROADMAP_GRANULARITY_FAILURE`.

## Clasificación de archivos basura generados por error

La categoría operativa de artefacto no-op o basura incluye archivos creados o modificados accidentalmente, aunque el commit cambie el árbol.

- `GARBAGE_ARTIFACT_FILE`: archivo sin función en build, runtime, tests, documentación, packaging ni coordinación, introducido por una operación equivocada.
- `PLACEHOLDER_GARBAGE_FILE`: archivo cuyo contenido normalizado es solo uno o pocos tokens sin función sintáctica o semántica, por ejemplo `X`, una palabra placeholder, un marcador provisional o puntuación repetida.
- `TOOL_OUTPUT_ARTIFACT_FILE`: archivo que contiene argumentos, payloads, respuestas, identificadores, mensajes de herramienta o serializaciones copiadas accidentalmente.
- `ERROR_DUMP_ARTIFACT_FILE`: archivo que contiene exclusivamente traceback, stack trace, página de error, respuesta `Not Found`, diagnóstico transitorio o salida fallida que no es una fixture intencional.
- `TRUNCATED_GENERATION_ARTIFACT_FILE`: archivo cortado a mitad de sintaxis, bloque, JSON, YAML, GLSL, Markdown o contenido esperado por una generación interrumpida.
- `WRONG_PATH_ARTIFACT_FILE`: archivo duplicado, con nombre o extensión accidental, o contenido válido escrito en una ruta no consumida.
- `GARBAGE_ARTIFACT_MIXED_COMMIT`: commit que contiene cambios funcionales y uno o más artefactos basura; no se elimina el commit completo, se reconstruye su árbol sin esos paths y se preserva el resto del diff.

El contenido mínimo por sí solo no prueba basura. Antes de retirar un archivo verificá conjuntamente:

1. commit y run que lo introdujeron;
2. ausencia de referencias desde manifests, imports, includes, build, workflows, tests, fixtures, snapshots, documentación y packaging;
3. ausencia de una convención legítima que permita archivos vacíos o mínimos;
4. parser, compilador o semántica esperada para su extensión y ruta;
5. que retirarlo o restaurar su versión anterior produce el árbol funcional esperado y pasa las validaciones afectadas;
6. que no está firmado, publicado, taggeado, requerido por release, protegido o compartido por otra rama o PR.

Protegé explícitamente archivos mínimos legítimos, incluidos marcadores de directorio, módulos de paquete intencionalmente vacíos, fixtures de vacío, snapshots, archivos de licencia, sentinels y formatos cuyo contenido mínimo sea válido.

## Saneamiento de commits con artefactos basura

- Si el commit contiene solo artefactos probados, clasificalo `GARBAGE_ARTIFACT_COMMIT` y omitilo durante el replay.
- Si contiene trabajo válido y basura, reconstruí el commit con el diff funcional y sin los paths basura; preservá autor, committer, `GIT_AUTHOR_DATE`, `GIT_COMMITTER_DATE`, timezone, mensaje y topología soportada.
- Reaplicá todos los commits posteriores contra sus nuevos parents conservando sus timestamps originales; nunca uses la hora de limpieza.
- Ejecutá la reescritura solo mediante GitHub Actions, con `--force-with-lease`, árbol final validado y ausencia de candidatos desde `refs/heads/*` y `refs/tags/*`.
- Eliminá workflows, scripts, ramas y tags temporales. No dejes commit ni merge de limpieza.

## Familias cubiertas

El README es el registro exhaustivo de códigos conocidos. Las familias mínimas son:

- carga e integridad de prompts;
- transporte, API, paginación, autenticación y permisos;
- coordinación, lease, concurrencia y entrega de comandos;
- archivos, encoding, parsers, referencias y generación accidental;
- Git, refs, ramas, commits, merges, PRs y saneamiento histórico;
- dependencias, procesos, filesystem, memoria, disco y caches;
- CI, workflows, runners, artifacts, tests y validadores;
- GLSL, Iris, OpenGL, render, estabilidad, compatibilidad y rendimiento;
- roadmap, matriz, aceptación, release y evidencia;
- privacidad, secretos, alcance, seguridad y legalidad;
- tiempo, checkpoint, recuperación entre ejecuciones y fallos no clasificados.

## Registro de fallos no previstos

`UNCLASSIFIED_INTERNAL_FAILURE` es una ruta de trabajo, no un resultado terminal:

1. generá una descripción neutral y reproducible;
2. reducí el fallo al menor caso que preserve el síntoma;
3. inspeccioná logs, diffs, árboles, refs, inputs y outputs;
4. formulá una hipótesis causal verificable;
5. añadí una prueba que falle antes del fix cuando sea posible;
6. repará dentro del alcance y repetí validación;
7. reclasificá con un código existente o creá uno nuevo cuando `SKILLS_MAINTENANCE` esté autorizado;
8. continuá la tarea original desde el gate invalidado.

Si el proceso desaparece completamente, la siguiente ejecución lee el estado remoto, adopta la misma rama, PR y checkpoint, ejecuta este loop y no crea una unidad paralela.

## Continuidad y límite de `PARTIAL`

- La ejecución siguiente retoma primero la misma unidad, rama, PR y checkpoint remotos.
- No se abre una unidad paralela ni una segunda PR descriptiva sobre la misma deuda.
- Dos ciclos consecutivos solo pueden terminar `PARTIAL` sobre la misma unidad cuando exista nueva evidencia objetiva que impida el cierre.
- Un checkpoint sin implementación, prueba, corrección o decisión técnica útil no constituye avance recuperable.
- Cuando la causa desaparece dentro del presupuesto, el ciclo debe completar validación, merge, reconciliación y cierre en lugar de publicar otro checkpoint.

## Resultado y parada

- `PASS`: causa reparada, pruebas repetidas, estado reconciliado y tarea original completada.
- `PARTIAL`: existe checkpoint remoto útil y una siguiente ejecución puede continuar autónomamente.
- `NO-OP`: solo `ACTIVE_RUN`, `PROJECT_ALREADY_COMPLETE`, `NO_AUTHORIZED_WORK`, `ALL_REMAINING_WORK_EXTERNALLY_BLOCKED` o `LATE_ACQUIRE_ORPHANED`, con evidencia explícita.
- `BLOCKED`: reservado para un `EXTERNAL_BLOCKER` real o una condición de coordinación irrecuperable después de todas las rutas y sin checkpoint útil.

La mera presencia de un error, una excepción, un run fallido, un archivo corrupto, una herramienta ausente o una prueba roja nunca basta para `BLOCKED`.
