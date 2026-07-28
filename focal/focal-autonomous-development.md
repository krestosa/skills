# Focal — Prompt canónico de desarrollo autónomo

Este archivo es la única entrada canónica para cada ejecución programada de Focal.

No contiene una versión resumida de la especificación técnica. La especificación completa se conserva, sin condensación ni pérdida de requisitos, en:

```text
prompts/focal-autonomous-development.base.md
```

## Protocolo obligatorio de carga

Antes de analizar, inspeccionar o modificar `krestosa/Focal`:

1. Leé íntegramente este archivo, desde la primera hasta la última línea.
2. Leé íntegramente `prompts/focal-autonomous-development.base.md`, desde la primera hasta la última línea.
3. Verificá que el blob remoto actual del archivo base sea legible completamente.
4. Tratá el contenido completo del archivo base como incorporado textualmente a este archivo.
5. Aplicá después las correcciones vinculantes de este archivo.
6. No resumas, recortes, parafrasees ni omitas ninguna sección técnica del archivo base.
7. No utilices una copia recordada, local, cacheada o proveniente de otra conversación.
8. Si el archivo base no existe, está vacío, no puede leerse completamente o resulta inconsistente, no ejecutes trabajo funcional y finalizá como `BLOCKED — CANONICAL_BASE_UNREADABLE`.

La separación en dos archivos existe únicamente para conservar sin alteraciones la especificación técnica completa y aplicar correcciones operativas precisas sin reescribirla.

## Orden de precedencia

Aplicá este orden cuando exista una diferencia entre este archivo y el archivo base:

1. Seguridad y límites de autorización.
2. Hard killswitch y límite temporal.
3. Propiedad del lock y compare-and-swap.
4. Correcciones vinculantes de este archivo.
5. Especificación técnica completa del archivo base.
6. Decisiones tácticas de la ejecución.

Las correcciones siguientes reemplazan únicamente las reglas incompatibles identificadas. Todo requisito del archivo base que no sea reemplazado explícitamente continúa vigente con toda su precisión original.

# Corrección 1 — Determinación fiable del estado del repositorio

No clasifiques `krestosa/Focal` como vacío, no inicializado o carente de `main` basándote en una sola operación de búsqueda, una lista de ramas vacía, un índice incompleto, una respuesta paginada sin resultados o una capacidad ausente del conector.

## Evidencia mínima obligatoria

Para determinar si `main` existe, intentá en este orden, según las operaciones disponibles:

1. Leer un archivo conocido desde `main`, comenzando por `README.md`.
2. Buscar commits recientes del repositorio.
3. Resolver el head de la rama predeterminada.
4. Consultar metadatos del repositorio.
5. Consultar directamente un SHA conocido cuando exista evidencia previa en GitHub.

El repositorio se considera inicializado cuando cualquiera de estas evidencias remotas verificables demuestra la existencia de un commit alcanzable desde `main`.

Una búsqueda de ramas que devuelve una lista vacía no demuestra por sí sola que el repositorio esté vacío.

Una operación que no puede enumerar refs tampoco demuestra que `main` no exista.

No declares `TARGET_REPOSITORY_UNINITIALIZED` mientras una lectura de archivo, búsqueda de commits o resolución directa de `main` siga siendo posible.

## Estado inicial actualmente verificado

`krestosa/Focal` dispone de una rama `main` inicializada. Cada ejecución debe volver a resolver su head remoto actual y no depender de un SHA recordado.

También existe la rama operativa:

```text
automation/runtime-state
```

con el archivo:

```text
automation/run-state.json
```

Cada ejecución debe volver a leerlos desde GitHub y verificar su estado actual.

## Bootstrap de un repositorio genuinamente vacío

Solo si todas las operaciones remotas fiables confirman que no existe ningún commit alcanzable:

1. Creá un commit raíz mínimo en `main` mediante una operación de GitHub capaz de crear un commit sin padre.
2. El commit raíz debe modificar exactamente una ruta, preferentemente `README.md`.
3. Resolvé y verificá el SHA resultante.
4. Creá `automation/runtime-state` desde ese SHA.
5. Creá `automation/run-state.json` en un commit separado.
6. Verificá ambas ramas y ambos commits remotamente.
7. Continuá únicamente si el bootstrap fue verificado.

Si las herramientas disponibles no permiten crear un commit raíz, finalizá como `BLOCKED — ROOT_COMMIT_CAPABILITY_UNAVAILABLE` sin afirmar que el repositorio está inicializado.

# Corrección 2 — Semántica de la rama `automation/runtime-state`

La rama `automation/runtime-state` se crea desde un commit existente de `main`.

Por lo tanto, hereda legítimamente el árbol de archivos de ese commit base. No debe considerarse inválida por contener los archivos heredados de `main`.

La regla correcta es:

- la rama no se fusiona con `main`;
- la rama no se usa para desarrollar el shader;
- la rama no se usa como rama de PR funcional;
- después de su creación, sus commits operativos ordinarios deben modificar exclusivamente `automation/run-state.json`;
- si se introduce un schema operativo, debe realizarse en un commit separado y explícito;
- no deben realizarse cambios funcionales en archivos heredados dentro de esa rama;
- el ZIP distribuible no incluye el archivo de estado;
- la presencia del árbol heredado no viola el protocolo.

Esta corrección reemplaza cualquier frase del archivo base que pueda interpretarse como que la rama debe poseer físicamente un único archivo en todo su árbol.

# Corrección 3 — El lock compartido es el mecanismo canónico de exclusión

La adquisición atómica de `automation/run-state.json` mediante compare-and-swap es el mecanismo primario, obligatorio y canónico para coordinar:

- chats programados;
- chats manuales;
- operadores manuales;
- GitHub Actions;
- workflows de recuperación;
- cualquier proceso autorizado con capacidad de mutación.

GitHub Actions `concurrency` complementa este lock, pero no lo reemplaza.

La inspección global de runs de GitHub Actions es una señal defensiva suplementaria. No debe convertirse en un bloqueo permanente cuando el conector actual no exponga una operación fiable para enumerar todos los runs activos del repositorio.

## Modos de detección de Actions

Registrá uno de estos valores en el informe terminal:

```text
VERIFIED_GLOBAL
VERIFIED_KNOWN_RUNS
COORDINATED_BY_SHARED_LOCK
UNVERIFIED_AND_UNSAFE
```

### `VERIFIED_GLOBAL`

Se enumeraron de forma fiable todos los runs relevantes y no existe otro run mutador activo.

### `VERIFIED_KNOWN_RUNS`

No existe enumeración global, pero se verificaron todos los runs concretos conocidos por SHA, PR, workflow o run ID y no hay evidencia de concurrencia.

### `COORDINATED_BY_SHARED_LOCK`

La herramienta no permite una enumeración global fiable. La ejecución puede continuar cuando se cumplen todas estas condiciones:

- `automation/run-state.json` puede leerse;
- la adquisición compare-and-swap funciona;
- no existe una lease válida ajena;
- no existe un run activo conocido;
- no existe evidencia positiva de concurrencia;
- la ejecución registra explícitamente la limitación;
- todo workflow mutador diseñado por el proyecto debe adquirir el mismo lock;
- los workflows mutadores deben compartir el mismo grupo `concurrency`.

La ausencia de una operación global de listado, por sí sola, no es motivo de `BLOCKED`.

### `UNVERIFIED_AND_UNSAFE`

No puede realizarse un scan global y tampoco puede leerse o adquirirse atómicamente el lock compartido. En este caso sí debe finalizarse como `BLOCKED`.

## Regla conservadora

Bloqueá o entrá en sleep mode si existe cualquiera de estas señales positivas:

- lease válida ajena;
- run activo conocido;
- Action mutadora conocida en estado no terminal;
- inconsistencia de propiedad;
- compare-and-swap no disponible;
- cambio remoto concurrente durante la adquisición;
- imposibilidad de verificar el archivo operativo.

No bloquees únicamente por ausencia de una API de enumeración global cuando el lock compartido sí puede coordinar de forma atómica.

## Carrera simultánea

Si dos ejecuciones leen el mismo blob `idle`:

1. Ambas pueden preparar una adquisición.
2. Solo una escritura compare-and-swap con el SHA esperado puede resultar válida.
3. La segunda debe recibir conflicto, releer y reconocer al nuevo propietario.
4. La segunda debe entrar en sleep mode o finalizar como `BLOCKED — ACTIVE_RUN`.
5. Ninguna ejecución puede tratar un fallo compare-and-swap como permiso para sobrescribir.

# Corrección 4 — Requisitos de GitHub Actions

Todo workflow con capacidad de mutación debe declarar:

```yaml
concurrency:
  group: focal-autonomous-development
  cancel-in-progress: false
```

Además, antes de cualquier mutación debe adquirir el mismo lock remoto utilizado por los chats.

Una Action debe registrar, cuando correspondan:

- `executionSource: github-actions`;
- workflow;
- run ID;
- run attempt;
- job;
- head branch;
- head SHA;
- timestamps de lease.

La Action debe liberar el lock mediante un finalizador `if: always()` únicamente cuando el `runId` continúe siendo suyo.

`concurrency` coordina Actions entre sí. El lock remoto coordina Actions con chats y procesos externos.

# Corrección 5 — Reloj monotónico y supervisor creados por la ejecución

La falta de un reloj monotónico suministrado por la plataforma no permite usar horas aproximadas.

La propia ejecución debe crear su reloj monotónico como primera acción local ejecutable mediante una herramienta equivalente a:

```python
import time
from datetime import datetime, timedelta, timezone

started_monotonic = time.monotonic()
started_at = datetime.now(timezone.utc)
soft_stop_at = started_at + timedelta(minutes=50)
cleanup_at = started_at + timedelta(minutes=55)
hard_kill_at = started_at + timedelta(minutes=58, seconds=30)
deadline_at = started_at + timedelta(minutes=59)
```

Para cálculos internos utilizá `time.monotonic()` o un reloj monotónico equivalente.

Para persistencia remota utilizá UTC ISO-8601.

No describas el inicio, fin o duración como “aproximados” si la VM permite ejecutar Python, `timeout` o una herramienta local equivalente.

El reloj monotónico no necesita persistir entre tareas. Debe existir durante toda la ejecución actual y ser independiente de cambios en el reloj civil.

Si la VM no permite ejecutar ningún supervisor local, ningún reloj monotónico y ningún mecanismo de terminación del grupo de procesos:

- no adquieras el lock funcional;
- no comiences implementación;
- finalizá como `BLOCKED — RUNTIME_GUARD_UNAVAILABLE`.

La primera versión del supervisor puede ser efímera durante el bootstrap, pero debe cumplir el soft stop y el hard stop. Después debe implementarse y probarse dentro del repositorio conforme al archivo base.

# Corrección 6 — Fuente de ejecución

Cuando el ciclo provenga de la tarea programada de ChatGPT, utilizá:

```text
executionSource: scheduled-chat
```

No lo clasifiques como `manual` salvo que la ejecución haya sido iniciada efectivamente por un operador manual fuera de la tarea programada.

# Corrección 7 — Inicialización y adquisición actuales

En el estado actual, la ejecución no debe intentar recrear la rama operativa o el archivo de estado si ya existen.

Debe:

1. Releer `main` y resolver su head actual.
2. Releer `automation/runtime-state`.
3. Releer `automation/run-state.json`.
4. Conservar el blob SHA exacto del archivo de estado.
5. Verificar que el JSON sea válido.
6. Verificar timestamps y propiedad.
7. Aplicar el protocolo de lease.
8. Adquirir mediante compare-and-swap si el estado es `idle`.
9. Verificar la adquisición mediante una segunda lectura.

Un `404` de una operación concreta debe verificarse mediante otras operaciones remotas antes de concluir que la rama o el archivo no existen.

# Corrección 8 — PASS y evidencia sobre Actions

La definición de PASS del archivo base se mantiene, con esta precisión:

La detección de GitHub Actions puede considerarse suficiente bajo uno de estos resultados:

- `VERIFIED_GLOBAL`;
- `VERIFIED_KNOWN_RUNS`;
- `COORDINATED_BY_SHARED_LOCK`.

`COORDINATED_BY_SHARED_LOCK` es aceptable únicamente si el compare-and-swap fue ejecutado y verificado, no existe evidencia positiva de otro run activo y la limitación del conector queda informada.

`UNVERIFIED_AND_UNSAFE` nunca puede ser PASS.

No afirmes “no hay Actions activas” cuando no hubo scan global. Informá en su lugar que la coordinación se realizó mediante el lock compartido.

# Corrección 9 — Informe terminal ampliado

Añadí al informe terminal:

```text
Detección de Actions: VERIFIED_GLOBAL | VERIFIED_KNOWN_RUNS | COORDINATED_BY_SHARED_LOCK | UNVERIFIED_AND_UNSAFE
Capacidad de listado global disponible: sí | no
Coordinación compare-and-swap verificada: sí | no
Reloj monotónico creado por la ejecución: sí | no
Supervisor local activo: sí | no
Fuente del SHA de main:
Fuente del estado de automation/runtime-state:
```

Cuando una operación de listado devuelva cero resultados, indicá qué operación fue y qué verificaciones adicionales se realizaron.

# Corrección 10 — Prohibición de falsos bloqueos por limitación de herramienta

No conviertas automáticamente una capacidad ausente del conector en una ausencia del recurso remoto.

Diferenciá siempre:

- `RESOURCE_CONFIRMED_ABSENT`;
- `RESOURCE_PRESENT`;
- `CAPABILITY_UNAVAILABLE`;
- `RESULT_INCONCLUSIVE`.

Solo `RESOURCE_CONFIRMED_ABSENT` permite afirmar que el recurso no existe.

`CAPABILITY_UNAVAILABLE` exige utilizar otro método remoto autorizado o aplicar el fallback definido en este archivo.

`RESULT_INCONCLUSIVE` exige relectura o una segunda fuente de evidencia.

No declares nuevamente `TARGET_REPOSITORY_UNINITIALIZED` salvo que la ausencia de commits haya sido confirmada por múltiples operaciones remotas independientes.

# Corrección 11 — Recuperación prioritaria desde el entorno local de la VM

Esta corrección reemplaza expresamente toda regla del archivo base o de este archivo que afirme que el estado local anterior debe descartarse siempre, que GitHub es la única fuente posible de recuperación o que está prohibido continuar desde trabajo local legítimo encontrado en la VM.

GitHub continúa siendo la autoridad remota para coordinación, locks, ramas compartidas, PRs, CI, merges y persistencia final. Sin embargo, el entorno local de la VM es la primera fuente de recuperación de trabajo no publicado cuando contiene evidencia inequívoca de una ejecución anterior de `krestosa/Focal`.

## Orden obligatorio al comenzar

Después de iniciar el reloj monotónico y el supervisor, cargar íntegramente ambos archivos del prompt y antes de buscar bugs, optimizaciones, tareas nuevas o implementar cambios:

1. Inspeccioná en modo de solo lectura el entorno local de la VM.
2. Buscá workspaces Git plausibles de `krestosa/Focal` en el directorio de trabajo actual y en las raíces de workspace disponibles y razonables.
3. No recorras de forma ilimitada todo el sistema de archivos.
4. Excluí caches, dependencias, directorios temporales irrelevantes, copias de otros repositorios y rutas sin `.git` válido.
5. Recién después resolvé el estado remoto correspondiente en GitHub.
6. Antes de modificar, confirmar, publicar o continuar cualquier trabajo local, inspeccioná el lock remoto y adquirilo mediante compare-and-swap.
7. Si no existe trabajo local recuperable, reconstruí el trabajo desde GitHub conforme al resto del prompt.

La inspección local previa al lock es estrictamente de solo lectura. No permite editar archivos, ejecutar formatters que modifiquen contenido, resolver merges, crear commits, cambiar ramas, eliminar archivos, aplicar stashes ni iniciar procesos funcionales.

## Detección de workspaces candidatos

Para cada candidato local obtené, como mínimo:

- ruta absoluta;
- validez del repositorio Git;
- resultado de `git rev-parse --show-toplevel`;
- URL o URLs de los remotos;
- rama actual o estado detached;
- SHA de `HEAD`;
- estado porcelain completo;
- archivos modificados;
- archivos staged;
- archivos sin seguimiento;
- archivos eliminados;
- commits locales visibles;
- stashes existentes;
- presencia de merge, rebase, cherry-pick, revert o bisect en curso;
- worktrees vinculados;
- fecha de modificación de los archivos relevantes cuando pueda obtenerse sin alterar el workspace.

Normalizá variantes equivalentes de la URL remota, incluidas HTTPS, SSH y URLs con sufijo `.git`. Un workspace solo puede atribuirse a Focal si el remoto normalizado corresponde exactamente a `krestosa/Focal` o si existe evidencia Git inequívoca de que fue materializado desde ese repositorio por la ejecución anterior.

No uses únicamente el nombre de la carpeta `Focal` como prueba de identidad.

## Clasificación local obligatoria

Clasificá cada candidato como uno de estos estados:

```text
LOCAL_CLEAN_MATCH
LOCAL_RECOVERABLE_UNCOMMITTED
LOCAL_RECOVERABLE_COMMITS
LOCAL_RECOVERABLE_OPERATION
LOCAL_DIVERGED
LOCAL_AMBIGUOUS
LOCAL_UNRELATED
LOCAL_CORRUPT
```

### `LOCAL_CLEAN_MATCH`

El workspace pertenece a `krestosa/Focal`, no contiene trabajo no publicado y puede reutilizarse únicamente si su commit y árbol coinciden con el estado remoto que se decida continuar.

### `LOCAL_RECOVERABLE_UNCOMMITTED`

El workspace pertenece a `krestosa/Focal` y contiene cambios staged, unstaged o sin seguimiento que pueden atribuirse razonablemente a una ejecución anterior y no presentan señales de secretos, corrupción o trabajo ajeno.

### `LOCAL_RECOVERABLE_COMMITS`

El workspace pertenece a `krestosa/Focal` y contiene uno o más commits locales que no están representados todavía por una rama remota verificada.

### `LOCAL_RECOVERABLE_OPERATION`

Existe una operación Git incompleta con metadata suficiente para identificar su intención y continuarla o preservarla de forma segura.

### `LOCAL_DIVERGED`

El historial local y el remoto contienen cambios distintos que requieren reconciliación explícita.

### `LOCAL_AMBIGUOUS`

Existe contenido potencialmente útil, pero no puede atribuirse con seguridad a Focal o a la ejecución anterior.

### `LOCAL_UNRELATED`

El repositorio o los cambios pertenecen a otro proyecto.

### `LOCAL_CORRUPT`

El repositorio Git, su índice, sus objetos o su metadata son ilegibles o inconsistentes.

## Selección entre varios candidatos

Si existen varios workspaces locales de Focal:

1. No combines sus cambios automáticamente.
2. Compará remoto, rama, HEAD, timestamps, operación en curso y relación con ramas o PRs existentes.
3. Preferí el candidato que tenga evidencia más fuerte de ser la continuación directa del último trabajo no publicado.
4. Priorizá trabajo recuperable sobre una copia limpia.
5. No elijas por fecha únicamente.
6. Si dos candidatos contienen cambios incompatibles y ninguno puede descartarse con evidencia, no continúes implementación nueva.
7. Preservá ambos de forma separada después de adquirir el lock, mediante ramas de recuperación distintas, o finalizá como `BLOCKED — MULTIPLE_LOCAL_WORKSPACES_AMBIGUOUS` si no pueden preservarse con seguridad dentro del tiempo disponible.

## Reconciliación con GitHub

Aunque exista trabajo local, siempre resolvé también:

- head remoto actual de `main`;
- rama remota equivalente, si existe;
- PR relacionada, si existe;
- último checkpoint registrado;
- lock y lease actuales;
- commits remotos;
- checks conocidos;
- cualquier cambio remoto posterior al `HEAD` local.

No asumas que el trabajo local es más nuevo ni que el remoto no cambió.

Después de adquirir y verificar el lock:

### Para cambios locales sin commit

1. Conservá el workspace original sin limpiar ni resetear.
2. Revisá cada path y su diff.
3. Detectá secretos, binarios inesperados y archivos ajenos.
4. Determiná el commit base local.
5. Comparalo con la rama remota relacionada.
6. Si la base es compatible, continuá desde el workspace local.
7. Creá commits separados por archivo conforme a la política general.
8. Publicá el primer checkpoint remoto antes de realizar trabajo adicional.
9. Solo después continuá la implementación pendiente.

### Para commits locales no publicados

1. Verificá cada commit y los paths que modifica.
2. Verificá autoría, mensaje, padres y relación con el remoto.
3. No reescribas ni descartes los commits antes de preservarlos.
4. Publicalos en la rama remota correspondiente cuando sea seguro.
5. Si la rama remota no existe, creá una rama `recovery/local-<runId>` desde una base remota compatible y reconstruí o publicá allí los commits preservando su contenido y trazabilidad.
6. Registrá el SHA remoto resultante como checkpoint.
7. Continuá desde esa rama.

### Para una operación Git incompleta

1. Inspeccioná su metadata antes de ejecutar comandos de continuación o aborto.
2. Continuá la operación únicamente si la intención, las ramas y los conflictos son inequívocos.
3. Si no es inequívoca, no ejecutes `--abort`, `reset --hard`, `clean`, checkout destructivo ni eliminación de metadata.
4. Preservá los archivos y commits recuperables en una rama remota de recuperación.
5. Documentá la operación pendiente.

### Para historial divergente

1. No fuerces push.
2. No resetees el trabajo local.
3. No sobrescribas la rama remota.
4. Creá una rama de recuperación desde un punto remoto verificable.
5. Aplicá o reconstruí los cambios locales de manera explícita, manteniendo un archivo por commit.
6. Abrí o actualizá una PR draft para reconciliación.
7. No fusiones hasta que la divergencia esté resuelta y validada.

## Stashes locales

Los stashes deben inspeccionarse como posible evidencia de trabajo anterior, pero no deben aplicarse automáticamente.

Solo aplicá un stash cuando:

- pertenece inequívocamente al workspace de Focal;
- su base puede determinarse;
- no duplica cambios ya presentes;
- no sobrescribe cambios actuales;
- el lock fue adquirido;
- existe tiempo suficiente para preservar inmediatamente el resultado en GitHub.

Si no se cumplen estas condiciones, conservá el stash intacto e informalo.

## Trabajo local ambiguo, corrupto o ajeno

- No descartes contenido ambiguo.
- No lo mezcles con Focal.
- No lo publiques en ramas funcionales.
- No abras sus archivos sensibles innecesariamente.
- No continúes desde un repositorio ajeno.
- Si el candidato es corrupto, intentá únicamente diagnóstico no destructivo.
- Si no existe trabajo local válido, continuá desde GitHub.
- Si existe trabajo potencialmente valioso pero no puede preservarse o atribuirse con seguridad, finalizá como `BLOCKED — LOCAL_RECOVERY_UNSAFE`.

## Prioridad de continuación

Cuando exista trabajo local recuperable y el lock pueda adquirirse:

1. Recuperar y publicar el trabajo local es la prioridad anterior a buscar bugs nuevos, optimizaciones o features.
2. No reconstruyas desde GitHub ignorando ese trabajo.
3. No reemplaces el workspace local por un checkout limpio antes de preservarlo.
4. No declares el workspace local descartable hasta que su contenido recuperable esté publicado o descartado con evidencia.
5. Después del primer checkpoint remoto verificado, GitHub vuelve a ser la fuente persistente compartida para el resto del ciclo.

Cuando no exista trabajo local recuperable:

1. Registrá que la inspección local fue realizada.
2. Indicá las rutas examinadas de forma resumida.
3. Continuá desde la rama o PR remota correspondiente.
4. No bloquees por ausencia de un workspace local.

## Límites de seguridad y tiempo

La recuperación local forma parte del presupuesto total de 59 minutos.

- No prolongues indefinidamente la búsqueda local.
- Utilizá una búsqueda acotada y determinista.
- Si la recuperación no puede completarse antes del soft stop, preservá el máximo estado seguro en GitHub y finalizá `INCOMPLETE — LOCAL_RECOVERY_CHECKPOINTED`.
- Si no puede preservarse antes del hard stop, no inicies operaciones destructivas.
- El hard killswitch continúa teniendo precedencia.
- La recuperación local nunca autoriza saltarse el lock, los gates de CI, la política de commits ni las reglas de procedencia.

## Informe terminal de recuperación local

Añadí al informe terminal:

```text
Entorno local inspeccionado: sí | no
Raíces locales examinadas:
Workspaces candidatos encontrados:
Workspace local seleccionado:
Clasificación local:
Remote local normalizado:
Rama local:
HEAD local:
Operación Git en curso:
Paths locales modificados:
Commits locales no publicados:
Stashes detectados:
Trabajo local retomado: sí | no
Primer checkpoint remoto de recuperación:
Fallback a GitHub utilizado: sí | no
Motivo del fallback a GitHub:
```

Un PASS posterior a recuperación local exige que todo trabajo recuperado que forme parte del resultado esté representado en GitHub y validado conforme al resto del prompt.

# Ejecución final

Después de cargar íntegramente el archivo base y aplicar estas correcciones:

1. Ejecutá exactamente un ciclo autónomo sobre `krestosa/Focal`.
2. Conservá toda la especificación gráfica, técnica, de QA, CI, seguridad, commits, PRs y roadmap del archivo base.
3. No reduzcas la cobertura técnica.
4. No omitas pruebas por el hecho de que este archivo sea más corto.
5. Aplicá el límite temporal completo.
6. Inspeccioná primero el entorno local de la VM y recuperá trabajo válido; cuando no exista trabajo local recuperable, continuá desde GitHub.
7. Utilizá GitHub como autoridad remota de coordinación y destino persistente de los checkpoints recuperados.
8. Utilizá el lock compartido como exclusión primaria.
9. Utilizá detección de Actions cuando esté disponible.
10. Aplicá el fallback `COORDINATED_BY_SHARED_LOCK` cuando corresponda.
11. Finalizá con evidencia exacta y sin afirmaciones aproximadas evitables.

Razonamiento: High