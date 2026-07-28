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

# Ejecución final

Después de cargar íntegramente el archivo base y aplicar estas correcciones:

1. Ejecutá exactamente un ciclo autónomo sobre `krestosa/Focal`.
2. Conservá toda la especificación gráfica, técnica, de QA, CI, seguridad, commits, PRs y roadmap del archivo base.
3. No reduzcas la cobertura técnica.
4. No omitas pruebas por el hecho de que este archivo sea más corto.
5. Aplicá el límite temporal completo.
6. Utilizá GitHub como fuente canónica.
7. Utilizá el lock compartido como exclusión primaria.
8. Utilizá detección de Actions cuando esté disponible.
9. Aplicá el fallback `COORDINATED_BY_SHARED_LOCK` cuando corresponda.
10. Finalizá con evidencia exacta y sin afirmaciones aproximadas evitables.

Razonamiento: High
