# Focal — Protocolo operativo de un ciclo

Este módulo define el procedimiento de `FOCAL_CYCLE`. No define el producto, el lock, el roadmap ni los criterios técnicos.

## 1. Preflight local y primera lectura remota

1. Generá un `runId` UUID v4.
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

## 2. Adquisición obligatoria antes del análisis

Después de la primera lectura del issue:

1. Validá título, bloques `focal-command:v3` y `focal-state:v3`, esquema y estado.
2. Resolvé únicamente la rama predeterminada y el SHA actual de `main`, necesarios para `baseMainSha`.
3. Ejecutá `inspect` mediante el bloque de comando y esperá `STATE_OBSERVED`.
4. Si hay una lease ajena válida, terminá `NO-OP` sin otras lecturas ni mutaciones.
5. Si el estado está `idle`, enviá `acquire`; si existe una lease vencida recuperable, aplicá `recover` conforme a `03-coordination.md`.
6. Esperá y releé hasta confirmar `status == working`, `runId` propio, razón esperada y expiración futura.
7. Si el issue continúa `idle`, no interpretes que el chat está trabajando: la ejecución no comenzó. Terminá `BLOCKED` o `NO-OP`.
8. No crees ramas, PRs, commits, comentarios, archivos ni checkpoints antes de esta confirmación.

## 3. Estado remoto autorizado

Solo después de adquirir o recuperar la lease:

1. Releé el SHA de la rama predeterminada.
2. Inspeccioná ramas recuperables, PRs abiertas, commits, checks, workflows, releases, roadmap y matriz relevantes.
3. No confíes en un clon, stash, reflog, workspace o archivo local de una ejecución anterior.
4. Materializá archivos localmente solo desde un ref remoto exacto y únicamente para validación o edición durante el ciclo actual.
5. Cualquier diferencia local sin contraparte remota carece de autoridad y no puede justificar progreso.
6. Emití un `heartbeat` de transición con fase `REMOTE_STATE_AUDIT` y confirmá `HEARTBEAT_ACCEPTED`.

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
4. Si restan menos de cinco minutos de lease, enviá `heartbeat` y esperá `HEARTBEAT_ACCEPTED`.
5. Si no podés confirmar propiedad, no ejecutes la mutación.

Un chat que sigue trabajando mientras el issue está `idle` está fuera del protocolo y debe detenerse inmediatamente.

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
8. Cada heartbeat debe registrar fase, rama, head, PR y checkpoint actuales.

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
4. Releé el issue y confirmá por última vez que seguís siendo propietario.
5. Enviá `release`. Este comando debe ser la **última mutación remota** de todo el ciclo.
6. Después de `release`, no actualices archivos, ramas, PRs, comentarios, labels, releases ni el bloque de comando nuevamente.
7. Releé el issue en modo solo lectura hasta confirmar `idle`, `runId == null`, `lastRunId` propio y `LEASE_RELEASED`, o documentá exactamente por qué no pudo confirmarse.
8. Emití únicamente la plantilla de `08-terminal-report.md`.

No ejecutes `cleanup_branches` como parte del cierre. Esa operación es mantenimiento administrativo independiente y solo puede comenzar cuando no existe ninguna ejecución de desarrollo activa.

No repitas el reporte en otro formato.
