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

Esta política define el coordinador basado en el issue #2 de `krestosa/Focal` y el workflow `Automation State Coordinator`.

La Capa 4 reemplaza completamente el almacenamiento del lock mediante commits. La adquisición, heartbeat, cambio de fase y liberación se realizan mediante comandos en comentarios del issue y resultados correlacionados del workflow.

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
3. Coordinación, propiedad de lease y protocolo issue-backed de la Capa 4.
4. Política de autonomía y bootstrap de la Capa 3.
5. Correcciones operativas consolidadas de la Capa 2 que no hayan sido reemplazadas.
6. Especificación técnica completa de la Capa 1.
7. Decisiones tácticas de la ejecución.

La Capa 4 reemplaza expresamente cualquier regla anterior que exija modificar `automation/run-state.json`, crear commits operativos, actualizar una rama de estado o usar compare-and-swap sobre un blob Git.

La Capa 3 reemplaza expresamente cualquier regla anterior que convierta una carencia interna implementable en un bloqueo o que permita terminar el ciclo limitándose a informar que falta CI, checks, runtime guard, workflows, herramientas, validadores, tests, schemas, fixtures, configuración o infraestructura propia del repositorio.

## Mandato autónomo esencial

Si falta algo necesario y está autorizado crearlo dentro de `krestosa/Focal`, crealo.

No solicites intervención del usuario para decisiones ordinarias, bootstrap, implementación, validación, configuración, CI, commits, ramas, PRs, correcciones, merges, checkpoints o priorización.

Solo puede requerirse intervención cuando exista un bloqueo externo real que no pueda resolverse mediante código, configuración, una herramienta alternativa, GitHub Actions, otra operación autorizada, una rama de recuperación o un checkpoint remoto.

Una ausencia interna debe producir trabajo. No debe producir parálisis.

## Mandato de limpieza del historial

No crees commits para:

- adquirir el lock;
- renovar la lease;
- registrar heartbeat;
- cambiar la fase operativa;
- registrar sleep mode;
- liberar el lock;
- actualizar el resultado terminal.

El estado efímero pertenece al issue #2 y a su workflow. Los commits quedan reservados para código, configuración, documentación, tests, workflows y otros cambios reales del proyecto.

Razonamiento: High
