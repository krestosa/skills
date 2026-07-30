# Focal — Protocolo operativo de un ciclo

Este módulo define el procedimiento de `FOCAL_CYCLE`. No define el producto, el lock, el roadmap ni los criterios técnicos.

## 1. Preflight local y primera lectura remota

1. Generá un `runId` UUID v4 y un `commandId` UUID v4 por comando.
2. Registrá `startedAt` en UTC y un reloj monotónico cuando el entorno lo permita.
3. Clasificá la topología:
   - `CONNECTOR_ONLY`;
   - `SUPERVISED_LOCAL_SUBPROCESSES`;
   - `FULL_LOCAL_WORKER`.
4. Todo proceso local funcional debe tener timeout, captura de salida y terminación de hijos.
5. Usá como guardas máximas, salvo un límite más estricto de la ejecución:
   - soft stop funcional: 50 minutos;
   - inicio de cleanup: 55 minutos;
   - hard stop: 58 minutos y 30 segundos.
6. No afirmes control POSIX sobre un worker que no sea un proceso local controlable.
7. La **primera llamada remota contra `krestosa/Focal`** debe leer íntegramente el issue `#7`.
8. No leas todavía roadmap, matriz, árbol, ramas, PRs, commits, checks, workflows ni releases.
9. No registres proveedor, modelo, aplicación, cliente, conector, actor ni plataforma de conversación. `runId` y `commandId` son las únicas identidades operativas.

## 1.1 Safeguard transversal del conector

Este protocolo aplica a toda lectura o mutación remota del ciclo, antes y después de adquirir la lease.

1. Un primer error de transporte, timeout, `429`, `5xx`, indisponibilidad temporal o excepción interna no termina el ciclo.
2. Reintentá la misma operación hasta cuatro intentos totales con backoff real de 2, 5, 10 y 20 segundos, respetando `Retry-After` y el hard stop.
3. En lecturas, repetí la consulta contra el mismo repositorio, ref, issue, PR, run o archivo.
4. En mutaciones con respuesta de error, marcá el resultado como desconocido y hacé `read-after-write` sobre el recurso autoritativo.
5. Si el efecto ya está aplicado, continuá sin duplicarlo. Si no está aplicado y la guarda de lease, SHA o head sigue vigente, reintentá la misma mutación con el mismo payload e identificador idempotente.
6. No cambies de `commandId` por un error de transporte. Un `commandId` nuevo corresponde únicamente al reenvío posterior a una escritura confirmada pero no procesada durante la ventana de coordinación.
7. Mientras el conector no permita confirmar propiedad, pausá nuevas mutaciones funcionales, conservá el checkpoint remoto existente y seguí reintentando; no asumas que la lease se perdió ni que la mutación falló.
8. Solo emití `CONNECTOR_RETRY_EXHAUSTED` cuando se agotaron los cuatro intentos, la verificación remota y cualquier fallback aplicable, o cuando el tiempo restante ya no permite un cierre seguro.

## 1.2 Safeguard de saneamiento histórico

Este protocolo se aplica antes de mergear y antes de `release` cuando el ciclo creó o detectó commits o refs de transporte sin valor funcional.

1. Detectá `NOOP_COMMIT`, `EMPTY_ARTIFACT_COMMIT` y `FAILED_TRANSPORT_COMMIT` por árbol, diff, runs y reachability; nunca por nombre o mensaje solamente.
2. En una rama de trabajo propia, saneá únicamente el tramo creado por la ejecución. En `main`, actuá solo por la ruta excepcional autorizada y exclusivamente mediante GitHub Actions.
3. La Action reconstruye desde el último parent limpio, omite candidatos y reaplica cada diff posterior. Conserva para cada commit posterior su autor, committer, `authorDate`, `committerDate`, timezone y mensaje originales; la hora de limpieza no reemplaza la cronología existente.
4. No atravieses merges salvo que todos los parents puedan mapearse y la topología equivalente quede demostrada. No toques tags, releases, ramas protegidas u otros PRs.
5. Verificá árbol final, diffs de commits conservados y ausencia de candidatos en `refs/heads/*` y `refs/tags/*` antes de continuar.
6. La actualización de ref usa `--force-with-lease` contra el head exacto. El workflow, scripts, ramas y tags temporales se eliminan; no se crea un commit de limpieza.
7. Si la Action falla antes del cambio de ref, no continúes con merge ni cierre. La ref objetivo debe quedar intacta y la rama temporal debe eliminarse mediante cleanup incondicional.

## 1.3 Despacho autónomo de errores

Toda operación del ciclo está envuelta por `AUTONOMOUS_RECOVERY_LOOP` de `12-autonomous-error-recovery.md`. Ante un fallo, pausá solo dependencias, releé la autoridad remota, clasificá, reuní evidencia, aplicá la escalera de recuperación, validá el artefacto exacto y retomá desde el primer gate invalidado. `UNCLASSIFIED_INTERNAL_FAILURE` obliga a crear un diagnóstico reproducible y un fix interno; no autoriza finalizar de inmediato.

## 2. Adquisición obligatoria antes del análisis

Después de la primera lectura del issue:

1. Validá título, bloques `focal-command:v3` y `focal-state:v3`, esquema y estado.
2. Resolvé únicamente la rama predeterminada y el SHA actual de `main`, necesarios para `baseMainSha`.
3. Ejecutá `inspect` mediante el bloque de comando y registrá el instante de escritura.
4. Esperá `STATE_OBSERVED` mediante polling con demora real: releé cada 5 a 10 segundos durante al menos 45 segundos antes de clasificar el comando como no procesado. Las lecturas consecutivas sin tiempo transcurrido no cuentan.
5. Si hay una lease ajena válida, terminá `NO-OP` sin otras lecturas ni mutaciones.
6. Si el estado está `idle`, enviá `acquire`; si existe una lease vencida recuperable, aplicá `recover` conforme a `03-coordination.md`.
7. Para `acquire`, `recover`, `heartbeat` y `release`, aplicá la misma disciplina temporal: polling real, correlación por `commandId` y observación del run cuando esté disponible.
8. Si un comando no se correlaciona después de 45 segundos reales y el issue continúa inequívocamente `idle`, sin otro `runId` ni workflow mutador activo:
   - releé el comando y el estado completos;
   - generá un `commandId` nuevo;
   - reenviá una sola vez la misma operación con timestamps y expiración recalculados;
   - esperá otra ventana de 45 segundos reales.
9. Si el segundo comando tampoco se correlaciona, comprobá el fallback programado de `Automation State Coordinator`. Cuando exista y resten al menos diez minutos de presupuesto, observá hasta seis minutos desde el segundo envío para permitir el run `schedule`; no declares fallo mientras ese fallback siga pendiente o ejecutándose.
10. Esperá y releé hasta confirmar `status == working`, `runId` propio, razón esperada y expiración futura.
11. Una adquisición tardía que se correlaciona después de que la ejecución ya emitió un resultado es una lease huérfana. No retomes trabajo retrospectivamente: liberala con el mismo `runId`, resultado factual y nota neutral antes de cualquier mantenimiento.
12. Solo terminá `BLOCKED` por coordinación cuando se agotaron el polling inicial, el reenvío único, el fallback programado aplicable y la evaluación de `COORDINATOR_REPAIR`, o cuando un comando fue procesado y rechazado con una razón final válida.
13. Si el entorno no permite esperar o medir tiempo transcurrido, terminá `BLOCKED` por observación insuficiente; no declares que el coordinador está roto.
14. Fuera de `COORDINATOR_REPAIR`, no crees ramas, PRs, commits, comentarios, archivos ni checkpoints antes de la confirmación de lease.

### 2.1 Retorno después de `COORDINATOR_REPAIR`

Cuando el coordinador haya sido reparado y el smoke test confirme `STATE_OBSERVED`:

1. descartá el `runId` previo al fallo y cualquier run diagnóstico;
2. releé el issue completo;
3. generá identidad opaca y tiempos nuevos para el ciclo funcional;
4. reiniciá esta sección desde el paso 1;
5. no reutilices ramas ni commits de reparación como rama funcional del shader.

Si la reparación no queda publicada o el smoke test sigue sin correlacionarse después de agotar el reenvío y fallback obligatorios, terminá `BLOCKED` sin analizar roadmap ni código funcional.

## 3. Estado remoto autorizado

Solo después de adquirir o recuperar la lease:

1. Releé el SHA de la rama predeterminada.
2. Inspeccioná ramas recuperables, PRs abiertas, commits, checks, workflows, releases, roadmap y matriz relevantes.
3. No confíes en un clon, stash, reflog, workspace o archivo local de una ejecución anterior.
4. Materializá archivos localmente solo desde un ref remoto exacto y únicamente para validación o edición durante el ciclo actual.
5. Cualquier diferencia local sin contraparte remota carece de autoridad y no puede justificar progreso.
6. Emití un `heartbeat` de transición con fase `REMOTE_STATE_AUDIT` y confirmá `HEARTBEAT_ACCEPTED` mediante polling temporal real.

## 4. Recuperación remota

Después de adquirir o recuperar la lease:

1. Inspeccioná la rama, PR o checkpoint indicados por el estado del ciclo anterior.
2. Priorizá trabajo remoto incompleto y válido antes de abrir una unidad nueva.
3. No mezcles ramas incompatibles ni crees una implementación paralela de la misma unidad.
4. Si el trabajo previo no puede validarse, preservalo y marcá sus ítems `REVALIDAR`.

## 5. Fase inicial obligatoria

Ejecutá `ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT` conforme a `04-roadmap.md` y `05-iris-capability-research.md`.

La fase termina únicamente cuando:

- `docs/ROADMAP.md` existe y fue auditado contra el estado remoto;
- `docs/IRIS-CAPABILITY-MATRIX.md` existe y posee cobertura suficiente para tomar la decisión del ciclo;
- el roadmap y la matriz se enlazan;
- se identificó una unidad válida o se demostró una causa cerrada de `NO-OP` mediante `WORK_SELECTION_PROOF`.

Si la fase consume el presupuesto, publicá solo su corrección documental y continuá con reconciliación; no fuerces una feature.

## 6. Clasificación de riesgo y selección adaptativa

Antes de crear o retomar una rama, resolvé en este orden:

1. Si el ciclo anterior terminó `PARTIAL`, retomá primero la misma unidad, rama, PR y checkpoint. No selecciones trabajo nuevo mientras esa deuda siga siendo ejecutable.
2. Clasificá el paquete de ejecución:
   - `LOW_RISK_BULK`: cambios pequeños, independientes, reversibles, sin modificación de arquitectura, contratos públicos, shaders runtime, seguridad, persistencia, compatibilidad, historia, releases ni infraestructura crítica; cada cambio posee aceptación y validación mecánicas.
   - `HIGH_IMPACT_INCREMENT`: cualquier cambio arquitectónico, funcional, gráfico, runtime, de compatibilidad, seguridad, datos, CI crítica, migración, API, rendimiento sensible o con riesgo de perder intención.
3. En `LOW_RISK_BULK`, podés agrupar varios ítems independientes en un solo ciclo, rama y PR para evitar avance administrativo fragmentado. El lote debe seguir cabiendo completo antes del soft stop.
4. En `HIGH_IMPACT_INCREMENT`, seleccioná un solo incremento vertical con resultado observable, utilizable y mergeable. Si la feature completa no cabe, dividila por capacidad funcional y criterio de aceptación, nunca por archivo, documento preparatorio o fase administrativa.
5. Para cualquiera de los carriles, definí:
   - objetivo verificable y resultado observable;
   - ítems de roadmap incluidos;
   - alcance y archivos previstos;
   - dependencias resueltas;
   - criterios de aceptación;
   - validaciones aplicables;
   - evidencia esperada;
   - riesgos y reversibilidad;
   - condición de parada;
   - tiempo suficiente para implementación, publicación, merge, reconciliación y `release`.
6. Seleccioná el paquete más grande que tenga alta probabilidad de quedar completamente validado, mergeado y reconciliado antes del soft stop. Reducí alcance antes de empezar si esa probabilidad no es alta.
7. Un checkpoint, una nota de intención, una PR preparatoria o un documento que solo enumera trabajo pendiente no constituyen una unidad seleccionable.
8. Dos ciclos consecutivos no pueden terminar `PARTIAL` sobre la misma unidad salvo que aparezca nueva evidencia objetiva: CI todavía en ejecución, dependencia externa, conflicto remoto, pérdida de lease, fallo reproducible no resuelto o entorno obligatorio no disponible.

### 6.1 `WORK_SELECTION_PROOF` obligatorio

Antes de terminar la selección sin una unidad funcional:

1. Enumerá al menos tres candidatos del roadmap; si quedan menos, enumeralos todos.
2. Para cada candidato registrá identificador, estado, prioridad, dependencias, resultado observable mínimo, archivos o subsistemas, validación, evidencia requerida, presupuesto y un código factual de descarte.
3. No descartes un candidato por ser una feature grande. Descomponelo por capacidad funcional y criterio de aceptación hasta obtener un `HIGH_IMPACT_INCREMENT` utilizable y mergeable.
4. Aplicá esta ruta fallback obligatoria: retomar `PARTIAL`; restaurar CI o validación; continuar `OPENGL_RUNTIME_HARNESS`; reparar granularidad del roadmap y ejecutar inmediatamente su primer incremento; seleccionar la menor capacidad vertical pendiente; resolver una inconsistencia documental factual solo cuando no exista trabajo funcional ejecutable.
5. Completá la selección dentro de los primeros quince minutos reales posteriores a `LEASE_ACQUIRED` o `LEASE_RECOVERED`. Si no ocurre, clasificá `ROADMAP_GRANULARITY_FAILURE` y ejecutá `AUTONOMOUS_RECOVERY_LOOP`; no consumas el ciclo en auditoría abierta.
6. `NO_VALID_UNIT`, `NO_BOUNDED_INCREMENT`, “demasiado grande”, complejidad o incertidumbre temporal no son resultados terminales ni causas de `NO-OP`.
7. `NO-OP` solo admite `ACTIVE_RUN`, `PROJECT_ALREADY_COMPLETE`, `NO_AUTHORIZED_WORK`, `ALL_REMAINING_WORK_EXTERNALLY_BLOCKED` o `LATE_ACQUIRE_ORPHANED`, cada uno con evidencia remota explícita.
8. Si el último ciclo terminó `NO-OP` por selección y el roadmap todavía contiene `PENDIENTE`, `EN PROGRESO` o `REVALIDAR`, repetir el mismo motivo se clasifica `NOOP_REASON_REPEATED`; la ejecución debe descomponer y seleccionar trabajo.

No abras subsistemas desconectados. La infraestructura habilitante y su primera utilización pueden formar un único incremento cuando sean inseparables y validables.

## 7. Guardia de propiedad antes de cada mutación

Antes de cualquier mutación en `krestosa/Focal`, incluyendo crear o actualizar archivos, ramas, commits, PRs, labels, merges, releases o documentación:

1. Releé el issue `#7`.
2. Confirmá `status == working`, `runId` propio y `leaseExpiresAt` futuro.
3. Confirmá que ningún comando externo haya cambiado la propiedad o dejado el estado `idle`.
4. Si restan menos de cinco minutos de lease, enviá `heartbeat` y esperá `HEARTBEAT_ACCEPTED` mediante polling temporal real.
5. Si no podés confirmar propiedad, no ejecutes la mutación.

Un chat que sigue trabajando mientras el issue está `idle` está fuera del protocolo y debe detenerse inmediatamente, excepto durante las operaciones estrictamente limitadas de `COORDINATOR_REPAIR`.

## 8. Rama, implementación y checkpoints

1. Retomá una rama remota compatible o creá una rama nueva desde el SHA remoto verificado.
2. No hagas push directo a la rama predeterminada.
3. Marcá cada ítem seleccionado `🟡 EN PROGRESO` con carril, rama, PR o siguiente acción.
4. Implementá la solución mínima completa; no reduzcas criterios para que entre en el ciclo y no agregues código sin consumidor verificable.
5. Aplicá la disciplina de commits del carril:
   - `LOW_RISK_BULK`: cada archivo modificado se publica en un commit dedicado que modifica exactamente ese archivo. No combines archivos ni mezcles dos archivos por conveniencia. Validá cada commit y luego el lote completo.
   - `HIGH_IMPACT_INCREMENT`: cada commit representa un cambio lógico revisable y puede modificar varias rutas relacionadas cuando separarlas produciría estados intermedios rotos, ocultaría intención o degradaría la revisión. No fuerces un commit por archivo.
6. En ambos carriles, cada commit debe tener propósito explícito, diff mínimo, nombres coherentes, manejo de errores deliberado y pruebas proporcionales. Eliminá placeholders, código muerto, duplicación, abstracciones especulativas, wrappers sin necesidad, fallbacks silenciosos y comentarios generados que no expliquen una decisión real.
7. Un incremento de alto impacto debe quedar individualmente construible, comprobable y mergeable; no depende de una futura PR para adquirir sentido básico.
8. Publicá un checkpoint únicamente ante una contingencia real: validación extensa que puede exceder el presupuesto, espera de CI, fallo transitorio persistente, riesgo de soft stop, pérdida inminente de lease o una operación de merge. El checkpoint no puede ser el objetivo planificado del ciclo.
9. Enviá heartbeat en cada cambio de fase y como máximo cada cinco minutos mientras continúe el trabajo.
10. Cada heartbeat debe registrar fase, rama, head, PR y checkpoint actuales, sin procedencia del cliente de ejecución.

## 9. Validación y publicación

1. Ejecutá el plan de validación de `07-validation-and-acceptance.md`.
2. Revisá el diff completo y las referencias.
3. Abrí o actualizá una pull request con alcance, motivación, pruebas, riesgos y estado del roadmap.
4. Inspeccioná checks del head exacto.
5. Corregí fallos causados por el cambio cuando el tiempo lo permita.
6. Antes del merge, resolvé el número exacto de la PR, el método de merge y el subject final esperado.
7. Aplicá `MERGE_TITLE_POLICY`: preferí el título automático de GitHub; si la operación envía `commit_title` o un título personalizado, debe contener el PR exacto mediante `<título de la PR> (#<n>)` para squash o `Merge pull request #<n> from <head>` para merge commit.
8. No uses rebase merge cuando el resultado no conserve `#<n>` de forma visible en el historial de la rama predeterminada.
9. Rechazá antes de ejecutar cualquier payload de merge cuyo título personalizado no contenga el número exacto del PR.
10. Mergeá autónomamente solo si todos los gates aplicables están aprobados, el head no cambió y no existe bloqueo de revisión.
11. Después del merge, releé la PR, el commit y la rama predeterminada; confirmá `merged == true`, `merge_commit_sha`, el SHA incorporado y que el subject visible contenga `#<n>`.
12. Si falla esa verificación, clasificá `MERGE_PR_REFERENCE_MISSING`, no reescribas historia publicada y no declares `PASS`; repará el procedimiento de merge para las operaciones siguientes y reportá el defecto factual.
13. Si CI continúa o una prueba obligatoria falta, dejá la PR y el checkpoint remotos; no marques el trabajo como completado.

## 10. Fase final obligatoria

Ejecutá `ROADMAP_RECONCILIATION` después del último estado remoto disponible, aun cuando el ciclo termine `PARTIAL` o `BLOCKED` después de haber adquirido la lease.

La reconciliación debe reflejar el estado de la rama predeterminada, no la intención ni el workspace.

## 11. Cierre y última mutación

En un bloque de finalización equivalente a `finally`:

1. Detené procesos locales propios.
2. Verificá que todo trabajo preservable esté en GitHub.
3. Completá antes de liberar cualquier mutación pendiente de archivos, ramas, PRs, merges, roadmap, matriz o checkpoints.
4. Auditá la historia, las refs y todos los paths creados o modificados por el ciclo. Si existe `NOOP_COMMIT`, `EMPTY_ARTIFACT_COMMIT`, `FAILED_TRANSPORT_COMMIT`, `GARBAGE_ARTIFACT_COMMIT` o `GARBAGE_ARTIFACT_MIXED_COMMIT`, incluido un archivo con solo `X` o contenido placeholder similar sin función, completá el saneamiento por GitHub Actions y verificá ausencia de artefactos alcanzables antes de liberar.
5. Releé el issue y confirmá por última vez que seguís siendo propietario.
6. Enviá `release`. Este comando debe ser la **última mutación remota** de todo el ciclo.
7. Después de `release`, no actualices archivos, ramas, PRs, comentarios, labels, releases ni el bloque de comando nuevamente.
8. Si la llamada de `release` devuelve error, no asumas que falló: aplicá `read-after-write`; si el mismo `commandId` no aparece y seguís siendo propietario, reintentá únicamente ese mismo `release` bajo el safeguard. Luego releé el issue en modo solo lectura, con demoras reales, hasta confirmar `idle`, `runId == null`, `lastRunId` propio y `LEASE_RELEASED`, o documentá exactamente por qué no pudo confirmarse.
9. Emití únicamente la plantilla de `08-terminal-report.md`.

No ejecutes `cleanup_branches` como parte del cierre. Esa operación es mantenimiento administrativo independiente y solo puede comenzar cuando no existe ninguna ejecución de desarrollo activa.

No repitas el reporte en otro formato.
