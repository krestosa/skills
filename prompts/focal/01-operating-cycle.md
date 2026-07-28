# Focal — Protocolo operativo de un ciclo

Este módulo define el procedimiento de `FOCAL_CYCLE`. No define el producto, el lock, el roadmap ni los criterios técnicos.

## 1. Inicio

1. Registrá `startedAt` en UTC y un reloj monotónico cuando el entorno lo permita.
2. Clasificá la topología:
   - `CONNECTOR_ONLY`;
   - `SUPERVISED_LOCAL_SUBPROCESSES`;
   - `FULL_LOCAL_WORKER`.
3. Todo proceso local funcional debe tener timeout, captura de salida y terminación de hijos.
4. Usá como guardas máximas, salvo un límite más estricto de la ejecución:
   - soft stop funcional: 50 minutos;
   - inicio de cleanup: 55 minutos;
   - hard stop: 58 minutos y 30 segundos.
5. No afirmes control POSIX sobre un worker que no sea un proceso local controlable.

## 2. Estado remoto inicial

Mediante el conector de GitHub:

1. Resolvé repositorio, rama predeterminada y SHA actual de `krestosa/Focal`.
2. Inspeccioná el issue de coordinación, ramas recuperables, PRs abiertas, commits, checks, workflows y releases relevantes.
3. No confíes en un clon, stash, reflog, workspace o archivo local de una ejecución anterior.
4. Materializá archivos localmente solo desde un ref remoto exacto y únicamente para validación o edición durante el ciclo actual.
5. Cualquier diferencia local sin contraparte remota carece de autoridad y no puede justificar progreso.

## 3. Exclusión mutua

Aplicá `03-coordination.md`.

- Si hay lease ajena válida: resultado `NO-OP`, sin rama, PR, pruebas ni mutaciones.
- Si el coordinador está corrupto o inaccesible después de fallbacks razonables: `BLOCKED`.
- Solo el `runId` confirmado por el estado puede continuar.

## 4. Recuperación remota

Después de adquirir o recuperar la lease:

1. Releé el SHA de la rama predeterminada.
2. Inspeccioná la rama, PR o checkpoint indicados por el estado del ciclo anterior.
3. Priorizá trabajo remoto incompleto y válido antes de abrir una unidad nueva.
4. No mezcles ramas incompatibles ni crees una implementación paralela de la misma unidad.
5. Si el trabajo previo no puede validarse, preservalo y marcá sus ítems `REVALIDAR`.

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

## 7. Rama, implementación y checkpoints

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
7. Renovà la lease según `03-coordination.md`.

## 8. Validación y publicación

1. Ejecutá el plan de validación de `07-validation-and-acceptance.md`.
2. Revisá el diff completo y las referencias.
3. Abrí o actualizá una pull request con alcance, motivación, pruebas, riesgos y estado del roadmap.
4. Inspeccioná checks del head exacto.
5. Corregí fallos causados por el cambio cuando el tiempo lo permita.
6. Mergeá autónomamente solo si todos los gates aplicables están aprobados, el head no cambió y no existe bloqueo de revisión.
7. Si CI continúa o una prueba obligatoria falta, dejá la PR y el checkpoint remotos; no marques el trabajo como completado.

## 9. Fase final obligatoria

Ejecutá `ROADMAP_RECONCILIATION` después del último estado remoto disponible, aun cuando el ciclo termine `PARTIAL` o `BLOCKED` después de haber adquirido la lease.

La reconciliación debe reflejar el estado de la rama predeterminada, no la intención ni el workspace.

## 10. Cierre

En un bloque de finalización equivalente a `finally`:

1. Detené procesos locales propios.
2. Verificá que todo trabajo preservable esté en GitHub.
3. Liberá la lease si todavía sos propietario.
4. Releé el issue hasta confirmar `idle` o documentá exactamente por qué no pudo confirmarse.
5. Emití únicamente la plantilla de `08-terminal-report.md`.

No repitas el reporte en otro formato.
