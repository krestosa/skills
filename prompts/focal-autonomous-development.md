# Focal — Entrada canónica de desarrollo autónomo

Este archivo es la única entrada canónica para cada ejecución programada de Focal.

La instrucción completa está compuesta por tres capas obligatorias. Ninguna capa puede resumirse, omitirse, sustituirse por memoria ni interpretarse como opcional.

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
- semántica de `automation/runtime-state`;
- lock compare-and-swap;
- coordinación con GitHub Actions;
- reloj monotónico y supervisor;
- fuente de ejecución programada;
- bootstrap inicial;
- evidencia de Actions;
- prevención de falsos bloqueos;
- recuperación prioritaria del trabajo local de la VM.

Tratala como incorporada textualmente a esta entrada. Las referencias internas del snapshot a “este archivo” se refieren al propio snapshot histórico que está siendo leído. No vuelvas a cargarlo recursivamente.

## Capa 3 — Política vinculante de autonomía y bootstrap

Leé íntegramente desde la rama predeterminada actual de `krestosa/skills`:

```text
prompts/focal-autonomous-development.autonomy.md
```

Esta política obliga a crear autónomamente toda infraestructura interna faltante y resuelve el problema circular de bootstrap de CI, runtime guard, validadores, workflows y demás capacidades implementables.

## Protocolo obligatorio de carga

Antes de inspeccionar el entorno local, analizar `krestosa/Focal`, adquirir el lock o realizar cualquier mutación:

1. Leé este archivo desde la primera hasta la última línea.
2. Leé íntegramente la Capa 1.
3. Leé íntegramente la Capa 2 desde el commit exacto indicado.
4. Leé íntegramente la Capa 3.
5. Verificá que las tres capas existen y pueden leerse completamente.
6. Tratá las tres capas como un único prompt compuesto.
7. No resumas, condenses, parafrasees ni omitas ninguna sección.
8. No utilices copias locales, recordadas, cacheadas o provenientes de conversaciones anteriores.
9. Aplicá después el orden de precedencia definido abajo.
10. Ejecutá exactamente un ciclo autónomo sobre `krestosa/Focal`.

Si una capa no puede leerse por un error transitorio, reintentá mediante otra operación remota autorizada antes de concluir que es inaccesible.

## Orden de precedencia

Cuando exista una diferencia entre las capas, aplicá este orden:

1. Seguridad, límites de autorización y restricciones legales.
2. Hard killswitch y límite temporal absoluto.
3. Propiedad del lock y compare-and-swap.
4. Política de autonomía y bootstrap de la Capa 3.
5. Correcciones operativas consolidadas de la Capa 2.
6. Especificación técnica completa de la Capa 1.
7. Decisiones tácticas de la ejecución.

La Capa 3 reemplaza expresamente cualquier regla anterior que convierta una carencia interna implementable en un bloqueo o que permita terminar el ciclo limitándose a informar que falta CI, checks, runtime guard, workflows, herramientas, validadores, tests, schemas, fixtures, configuración o infraestructura propia del repositorio.

## Mandato autónomo esencial

Si falta algo necesario y está autorizado crearlo dentro de `krestosa/Focal`, crealo.

No solicites intervención del usuario para decisiones ordinarias, bootstrap, implementación, validación, configuración, CI, commits, ramas, PRs, correcciones, merges, checkpoints o priorización.

Solo puede requerirse intervención cuando exista un bloqueo externo real que no pueda resolverse mediante código, configuración, una herramienta alternativa, GitHub Actions, otra operación autorizada, una rama de recuperación o un checkpoint remoto.

Una ausencia interna debe producir trabajo. No debe producir parálisis.

Razonamiento: High