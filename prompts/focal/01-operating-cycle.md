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
- se identificó una unidad válida o se determinó que no existe trabajo ejecutable.

Si la fase consume el presupuesto, publicá solo su corrección documental y continuá con reconciliación; no fuerces una feature.

## 6. Selección de unidad

Seleccioná una sola unidad coherente con:

- objetivo verificable;
- alcance y archivos previstos;
- dependencias resueltas;
- criterios de aceptación;
- validaciones aplicables;
- evidencia esperada;
- condición de parada;
- tiempo suficiente para publicación y reconciliación.

No abras subsistemas desconectados. Una unidad puede incluir infraestructura habilitante y su primera utilización solo si forman una secuencia inseparable y validable.

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
3. Marcá el ítem seleccionado `🟡 EN PROGRESO` con rama, PR o siguiente acción.
4. Implementá la solución mínima completa; no reduzcas criterios para que entre en el ciclo.
5. Creá commits coherentes por cambio lógico. No existe una regla de un archivo por commit.
6. Publicá un checkpoint antes de:
   - una validación extensa;
   - esperar CI;
   - alcanzar el soft stop;
   - realizar una operación de merge.
7. Enviá heartbeat en cada cambio de fase y como máximo cada cinco minutos mientras continúe el trabajo.
8. Cada heartbeat debe registrar fase, rama, head, PR y checkpoint actuales, sin procedencia del cliente de ejecución.

## 9. Validación y publicación

1. Ejecutá el plan de validación de `07-validation-and-acceptance.md`.
2. Revisá el diff completo y las referencias.
3. Abrí o actualizá una pull request con alcance, motivación, pruebas, riesgos y estado del roadmap.
4. Inspeccioná checks del head exacto.
5. Corregí fallos causados por el cambio cuando el tiempo lo permita.
6. Mergeá autónomamente solo si todos los gates aplicables están aprobados, el head no cambió y no existe bloqueo de revisión.
7. Si CI continúa o una prueba obligatoria falta, dejá la PR y el checkpoint remotos; no marques el trabajo como completado.

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
