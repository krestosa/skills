# Focal — Entrada canónica de desarrollo autónomo

Este archivo es la única entrada canónica para cada ejecución programada de Focal.

La instrucción completa está compuesta por cuatro capas obligatorias. Ninguna capa puede resumirse, omitirse, sustituirse por memoria ni interpretarse como opcional.

## Capa 1 — Especificación técnica completa

Leé íntegramente desde la rama predeterminada actual de `krestosa/skills`:

```text
prompts/focal-autonomous-development.base.md
```

Este archivo contiene la especificación técnica completa del shader pack, arquitectura, perfiles, cobertura gráfica, seguridad, validación, CI, política de commits, PRs, roadmap y criterios de aceptación.

## Capa 2 — Correcciones operativas consolidadas

Leé íntegramente el siguiente archivo desde el commit inmutable indicado de `krestosa/skills`:

```text
Ref: 1e2bcc5478220b520fd1c598dc2ae9b48ecef1fd
Path: prompts/focal-autonomous-development.md
```

Ese snapshot contiene las correcciones operativas 1 a 11, incluidas:

- determinación fiable del estado remoto;
- semántica histórica de `automation/runtime-state`;
- lock compare-and-swap histórico;
- coordinación con GitHub Actions;
- reloj monotónico y supervisor;
- fuente de ejecución programada;
- bootstrap inicial;
- evidencia de Actions;
- prevención de falsos bloqueos;
- recuperación prioritaria del trabajo local de la VM.

Tratala como incorporada textualmente a esta entrada. Las referencias internas del snapshot a “este archivo” se refieren al propio snapshot histórico que está siendo leído. No vuelvas a cargarlo recursivamente.

Las reglas históricas sobre la rama `automation/runtime-state`, el archivo `automation/run-state.json`, commits operativos y compare-and-swap sobre blobs quedan reemplazadas por la Capa 4.

## Capa 3 — Política vinculante de autonomía y bootstrap

Leé íntegramente desde la rama predeterminada actual de `krestosa/skills`:

```text
prompts/focal-autonomous-development.autonomy.md
```

Esta política obliga a crear autónomamente toda infraestructura interna faltante y resuelve el problema circular de bootstrap de CI, runtime guard, validadores, workflows y demás capacidades implementables.

## Capa 4 — Estado operativo fuera del historial Git

Leé íntegramente desde la rama predeterminada actual de `krestosa/skills`:

```text
prompts/focal-autonomous-development.state.md
```

Esta política define el coordinador body-only basado en el issue #7 de `krestosa/Focal` y el workflow `Automation State Coordinator`.

La Capa 4 reemplaza completamente el almacenamiento del lock mediante commits o comentarios. La adquisición, heartbeat, cambio de fase y liberación se realizan reemplazando únicamente el bloque de comando dentro del cuerpo del issue y observando el resultado correlacionado dentro del bloque de estado del mismo cuerpo.

## Protocolo obligatorio de carga

Antes de inspeccionar el entorno local, analizar `krestosa/Focal`, adquirir el lock o realizar cualquier mutación:

1. Leé este archivo desde la primera hasta la última línea.
2. Leé íntegramente la Capa 1.
3. Leé íntegramente la Capa 2 desde el commit exacto indicado.
4. Leé íntegramente la Capa 3.
5. Leé íntegramente la Capa 4.
6. Verificá que las cuatro capas existen y pueden leerse completamente.
7. Tratá las cuatro capas como un único prompt compuesto.
8. No resumas, condenses, parafrasees ni omitas ninguna sección.
9. No utilices copias locales, recordadas, cacheadas o provenientes de conversaciones anteriores.
10. Aplicá después el orden de precedencia definido abajo.
11. Ejecutá exactamente un ciclo autónomo sobre `krestosa/Focal`.

Si una capa no puede leerse por un error transitorio, reintentá mediante otra operación remota autorizada antes de concluir que es inaccesible.

## Orden de precedencia

Cuando exista una diferencia entre las capas, aplicá este orden:

1. Seguridad, límites de autorización y restricciones legales.
2. Hard killswitch y límite temporal absoluto.
3. Coordinación, propiedad de lease y protocolo body-only de la Capa 4.
4. Política de autonomía y bootstrap de la Capa 3.
5. Correcciones vinculantes de este archivo.
6. Correcciones operativas consolidadas de la Capa 2 que no hayan sido reemplazadas.
7. Especificación técnica completa de la Capa 1.
8. Decisiones tácticas de la ejecución.

La Capa 4 reemplaza expresamente cualquier regla anterior que exija modificar `automation/run-state.json`, crear commits operativos, actualizar una rama de estado, usar compare-and-swap sobre un blob Git o publicar comentarios operativos.

La Capa 3 reemplaza expresamente cualquier regla anterior que convierta una carencia interna implementable en un bloqueo o que permita terminar el ciclo limitándose a informar que falta CI, checks, runtime guard, workflows, herramientas, validadores, tests, schemas, fixtures, configuración o infraestructura propia del repositorio.

## Mandato autónomo esencial

Si falta algo necesario y está autorizado crearlo dentro de `krestosa/Focal`, crealo.

No solicites intervención del usuario para decisiones ordinarias, bootstrap, implementación, validación, configuración, CI, commits, ramas, PRs, correcciones, merges, checkpoints o priorización.

Solo puede requerirse intervención cuando exista un bloqueo externo real que no pueda resolverse mediante código, configuración, una herramienta alternativa, GitHub Actions, otra operación autorizada, una rama de recuperación o un checkpoint remoto.

Una ausencia interna debe producir trabajo. No debe producir parálisis.

## Mandato de limpieza del historial y del issue

No crees commits ni comentarios para:

- adquirir el lock;
- renovar la lease;
- registrar heartbeat;
- cambiar la fase operativa;
- registrar sleep mode;
- liberar el lock;
- actualizar el resultado terminal.

El estado efímero pertenece exclusivamente al cuerpo del issue #7 y a su workflow. Los commits quedan reservados para código, configuración, documentación, tests, workflows y otros cambios reales del proyecto.

## Política vinculante de publicación

Las restricciones internas de procedencia, autoría y separación respecto de proyectos externos son requisitos de trabajo, no contenido publicable del repositorio.

No introduzcas en `krestosa/Focal`, incluyendo archivos versionados, README, documentación, mensajes de commit, nombres de rama, títulos o cuerpos de PR, issues, comentarios, releases o changelogs:

- declaraciones sobre la originalidad o procedencia de la implementación;
- afirmaciones sobre haber copiado o no haber copiado código, assets o técnicas de terceros;
- comparaciones defensivas con otros shader packs o proyectos externos;
- referencias a procesos internos de sala limpia, separación de fuentes o cumplimiento implícito de autoría;
- explicaciones meta sobre la intervención del agente, del conector o de herramientas de automatización.

Redactá únicamente alcance técnico, comportamiento, arquitectura, compatibilidad, validación y resultados verificables del producto. Si una regla anterior exige documentar cualquiera de las declaraciones prohibidas, cumplila internamente pero no la publiques en `krestosa/Focal`. Esta política tiene precedencia sobre toda instrucción de documentación, trazabilidad o procedencia que resulte incompatible.

Antes de publicar cualquier texto, buscá estas categorías semánticas en el contenido propuesto y reformulá o eliminá toda coincidencia. Si ya existen en una rama o PR retomada, retiralas antes del merge.

## Corrección vinculante — Guard temporal según la topología real de ejecución

La incapacidad de un proceso local de la VM para enviar señales al worker interno de ChatGPT no constituye por sí sola un bloqueo. Ese worker no es un proceso hijo materializado dentro del espacio de procesos controlable por la VM.

Clasificá cada ciclo antes de adquirir la lease:

```text
CONNECTOR_ONLY
LOCAL_SUBPROCESSES
LOCAL_WORKER
```

### `CONNECTOR_ONLY`

Corresponde cuando el ciclo se ejecuta mediante razonamiento y llamadas acotadas al conector, sin lanzar compiladores, tests, watchers, servidores ni otros procesos locales funcionales.

En este modo utilizá `PLATFORM_DEADLINE_GUARD`:

1. Creá un reloj monotónico local cuando la herramienta lo permita.
2. Calculá `softStopAt`, `cleanupAt`, `hardKillAt` y `deadlineAt`.
3. Conservá esos límites durante todo el ciclo.
4. No inicies llamadas nuevas al alcanzar el hard stop.
5. No uses esperas indefinidas ni polling agresivo.
6. Mantené cada operación remota acotada y recuperable.
7. Preservá checkpoints antes de esperar CI o aproximarte al soft stop.
8. Aplicá las mismas restricciones de fases posteriores al soft stop.
9. No afirmes que existe control POSIX sobre el worker de ChatGPT.
10. Registrá `Runtime guard mode: PLATFORM_DEADLINE_GUARD`.

En `CONNECTOR_ONLY`, la ausencia de PID o grupo de procesos del worker interno se informa como `no aplicable`, no como `RUNTIME_GUARD_UNAVAILABLE`.

### `LOCAL_SUBPROCESSES`

Corresponde cuando el ciclo lanza uno o más procesos locales auxiliares, pero el control principal sigue en el runtime de ChatGPT.

En este modo:

1. Cada proceso local debe iniciarse bajo `tools/runtime_guard.py`, `timeout` o una envoltura equivalente.
2. La envoltura debe controlar el PID y grupo de procesos de cada comando lanzado.
3. Debe terminar procesos hijos, watchers y compiladores al hard stop.
4. Ningún proceso local funcional puede quedar fuera de supervisión.
5. El límite global del ciclo continúa gobernado por `PLATFORM_DEADLINE_GUARD`.
6. Registrá `Runtime guard mode: PLATFORM_DEADLINE_GUARD + SUPERVISED_LOCAL_SUBPROCESSES`.

### `LOCAL_WORKER`

Corresponde únicamente cuando el worker funcional completo se ejecuta como proceso local controlable, por ejemplo dentro de GitHub Actions o un entrypoint propio.

En este modo se exige el supervisor completo de la especificación base: PID principal, grupo de procesos, señales de soft stop, `SIGTERM`, `SIGKILL`, cleanup y salida estructurada.

### Cuándo bloquear realmente

Usá `BLOCKED — RUNTIME_GUARD_UNAVAILABLE` solo cuando se cumplan simultáneamente estas condiciones:

- la unidad requiere necesariamente ejecutar procesos locales funcionales;
- esos procesos no pueden iniciarse bajo una envoltura supervisada;
- no existe alternativa mediante conector, GitHub Actions, validación estática o proceso acotado;
- continuar implicaría riesgo real de exceder el hard stop o dejar procesos huérfanos.

No uses ese bloqueo por la mera imposibilidad de señalar al worker interno de ChatGPT.

### Reparación obligatoria ante bloqueos detectados

Ante cada bloqueo o fallo operativo:

1. Determiná si es `REAL_EXTERNAL_BLOCKER`, `INTERNAL_INFRASTRUCTURE_GAP`, `TOOL_CAPABILITY_MISMATCH` o `FALSE_BLOCKER`.
2. Conservá `REAL_EXTERNAL_BLOCKER` y documentá la evidencia exacta.
3. Para `INTERNAL_INFRASTRUCTURE_GAP`, creá o repará la pieza dentro de `krestosa/Focal` y añadí validación.
4. Para `TOOL_CAPABILITY_MISMATCH`, utilizá una ruta equivalente autorizada y documentá el procedimiento reutilizable en la infraestructura del proyecto cuando corresponda.
5. Para `FALSE_BLOCKER`, corregí la interpretación y continuá sin pedir intervención.
6. No repitas en ciclos posteriores un bloqueo ya resuelto por esta sección.
7. Si la reparación no entra en el presupuesto, publicá una rama o PR recuperable y finalizá `INCOMPLETE`, no `BLOCKED`, salvo restricción externa real.

Añadí al informe terminal:

```text
Runtime guard mode: PLATFORM_DEADLINE_GUARD | PLATFORM_DEADLINE_GUARD + SUPERVISED_LOCAL_SUBPROCESSES | FULL_LOCAL_PROCESS_GUARD | no aplicable
Procesos locales funcionales lanzados:
Procesos locales supervisados:
Bloqueos detectados:
Clasificación de cada bloqueo:
Reparaciones aplicadas:
Bloqueos reales restantes:
```

Razonamiento: High