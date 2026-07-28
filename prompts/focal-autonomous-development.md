# Focal — Entrada canónica de desarrollo autónomo

Este archivo es la única entrada canónica para cada ejecución programada de Focal.

La instrucción completa está compuesta por cinco capas obligatorias. Ninguna capa puede resumirse, omitirse, sustituirse por memoria ni interpretarse como opcional.

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

## Capa 5 — Roadmap maestro vivo y auditoría integral de Iris

Esta capa impone un gate documental obligatorio antes de cualquier implementación funcional. El roadmap no es un resumen, una lista aspiracional ni una tarea opcional: es el registro canónico, exhaustivo, verificable y continuamente reconciliado de todo el trabajo necesario para completar Focal.

### Archivo canónico

El roadmap debe existir en:

```text
docs/ROADMAP.md
```

Si no existe en la rama predeterminada actual de `krestosa/Focal`, crealo. Si existe, leelo íntegramente y auditá su exactitud contra el estado remoto real del repositorio antes de seleccionar o implementar cualquier unidad funcional.

No inicies cambios de shader, código, configuración, tests, workflows, tooling, packaging ni documentación funcional mientras el roadmap esté ausente, estructuralmente incompleto, desactualizado respecto del `main` remoto o no represente el trabajo ya existente.

### Momento obligatorio dentro del ciclo

Después de cargar las cinco capas, verificar concurrencia, adquirir válidamente la lease y reconstruir el estado remoto, la primera fase de análisis del repositorio debe ser `ROADMAP_AUDIT`.

En `ROADMAP_AUDIT`:

1. Resolvé el SHA exacto del `main` remoto.
2. Inspeccioná el árbol completo del repositorio y los archivos relevantes desde GitHub.
3. Inspeccioná ramas de trabajo recuperables, PRs abiertos o recientemente fusionados, commits, checks y workflows que puedan cambiar el estado real de una unidad.
4. Leé íntegramente `docs/ROADMAP.md` si existe.
5. Consultá la documentación oficial y vigente de Iris aplicable a la combinación objetivo.
6. Compará cada capacidad requerida con evidencia concreta del repositorio.
7. Creá, expandí o corregí el roadmap hasta que represente de forma exhaustiva el estado real.
8. Publicá el cambio del roadmap como commit documental aislado, conforme a la política de commits vigente, antes de iniciar implementación funcional.
9. Si el roadmap todavía no puede considerarse completo y verificable dentro del presupuesto temporal, dedicá el ciclo a completarlo y publicarlo. No empieces implementación funcional con un roadmap parcial.

Un roadmap presente pero superficial, genérico, sin evidencia, sin documentación enlazada o sin desglose técnico suficiente se considera inexistente a efectos de este gate.

### Fuentes oficiales obligatorias

El roadmap debe incluir enlaces directos y trazables, como mínimo, a las fuentes oficiales vigentes que correspondan:

- documentación principal de Iris: `https://shaders.properties/current/`;
- referencia general: `https://shaders.properties/current/reference/overview/`;
- programas y orden de ejecución: `https://shaders.properties/current/reference/programs/overview/`;
- `shaders.properties`, directivas y configuración: `https://shaders.properties/current/reference/shadersproperties/overview/`;
- opciones, pantallas, sliders, perfiles y localización: `https://shaders.properties/current/reference/shadersproperties/shader_settings/`;
- repositorio oficial de Iris: `https://github.com/IrisShaders/Iris`;
- repositorio oficial de documentación: `https://github.com/IrisShaders/docs`;
- ShaderDoc oficial del proyecto: `https://github.com/IrisShaders/ShaderDoc`.

Estas URL son puntos de entrada, no una lista suficiente. En cada auditoría, recorré las secciones, subpáginas, archivos de documentación, notas de versión, código fuente público, issues técnicos relevantes y referencias oficiales necesarias para cubrir todas las capacidades expuestas por la versión objetivo. Registrá para cada fuente la URL exacta consultada, la fecha UTC de consulta y, cuando exista, el tag, versión, rama o commit correspondiente.

No uses blogs, videos, wikis no oficiales, fragmentos de terceros ni memoria como fuente principal. Una fuente secundaria solo puede utilizarse cuando no exista fuente oficial suficiente, debe identificarse expresamente como secundaria y no puede contradecir la implementación ni la documentación oficial de Iris.

### Inventario integral obligatorio de Iris

El roadmap debe auditar todas las capacidades de shader pack expuestas, soportadas, limitadas o explícitamente no soportadas por la versión objetivo de Iris. Como mínimo, y sin limitarse a esta lista, debe cubrir:

1. Matriz de versiones y compatibilidad entre Minecraft, Fabric Loader, Fabric API cuando corresponda, Iris, Sodium, Java, Gradle, Loom, drivers y nivel de OpenGL/GLSL.
2. Estructura completa del shader pack, nombres de archivos, carpetas, includes, preprocessado, macros y reglas de descubrimiento.
3. Todos los programas, pases, etapas y órdenes de ejecución documentados, incluyendo cada etapa gráfica o de cómputo que la versión objetivo exponga.
4. Programas `setup`, `begin`, `shadow`, `shadowcomp`, `prepare`, `gbuffers_*`, `deferred`, `composite` y `final`, además de todos sus sufijos, variantes y condiciones aplicables según la documentación vigente.
5. Compute shaders, geometry shaders, tessellation shaders y cualquier otra etapa opcional, con requisitos, extensiones, límites y degradación segura.
6. Buffers de color, profundidad, sombra, historial y datos auxiliares; formatos, attachments, lectura, escritura, ping-pong, clearing, mipmaps, escalado, viewport y vida útil.
7. `DRAWBUFFERS`, `RENDERTARGETS`, constantes, directivas, comentarios especiales y reglas de escaneo.
8. Uniforms, atributos, vertex format extensions, varyings, built-ins, matrices, temporización, cámara, clima, mundo, entidades, iluminación y estados de render.
9. `shaders.properties`: feature flags requeridas u opcionales, custom uniforms, custom textures, custom images, SSBO, buffers, ordenamiento de programas y toda directiva disponible.
10. Opciones de usuario, defines, sliders, perfiles, pantallas, subscreens, columnas, traducciones `.lang`, tooltips y valores visibles.
11. Mapeos de bloques, ítems, entidades, block entities, biomas, dimensiones y cualquier identificador o tabla requerida.
12. Manejo de Overworld, Nether, End y dimensiones modificadas, incluyendo diferencias de pipeline y fallback.
13. Sombras: shadow map, resolución, distancia, culling, filtros, color, profundidad, entidades, terreno, translucent shadows y estabilidad temporal.
14. Materiales, PBR, normal/specular maps, labPBR cuando corresponda, emisión, roughness, metallic, porosidad, subsurface, AO y degradación ante texturas faltantes.
15. Iluminación directa e indirecta, skylight, block light, GI aproximada, SSAO, screen-space effects, voxelización y acumulación temporal, limitadas a capacidades realmente disponibles.
16. Agua, hielo, vidrio, partículas, clima, nubes, niebla, translucencia, hand rendering, entities y separación de draws.
17. Postprocesado, exposición, tonemapping, color grading, bloom, antialiasing, TAA, sharpen, depth of field, motion blur y efectos opcionales.
18. Compatibilidad con Sodium y límites conocidos de interacción con el renderer.
19. Compatibilidad con Distant Horizons u otras integraciones oficialmente documentadas, sin asumir soporte cuando no esté probado.
20. Iris Patcher, transformación GLSL, nombres reservados, código parcheado, diferencias entre fuente y shader compilado, y diagnóstico de errores.
21. Feature flags y extensiones exclusivas de Iris, sus requisitos de hardware y sus rutas de fallback.
22. Funciones no soportadas, limitaciones no corregibles, diferencias respecto del formato histórico y riesgos de portabilidad.
23. Herramientas de depuración, debug mode, patched shaders, logs, mensajes de compilación y evidencia reproducible.
24. Seguridad de GPU, prevención de hangs, límites de memoria, loops acotados, watchdogs, aislamiento de procesos y recuperación ante fallos.
25. QA estático, compilación GLSL, harness OpenGL real, pruebas visuales deterministas, métricas de imagen, benchmarks, compatibilidad de drivers y pruebas dentro de Minecraft mediante CI.
26. Packaging, detección por Iris, metadata, licencias, releases, checksums, changelog, instalación y rollback.
27. Perfiles `SAFE`, `BALANCED`, `HIGH` y `ULTRA`, con capacidades activas, presupuestos, límites, fallback y criterios cuantitativos para cada uno.
28. Automatización, GitHub Actions, concurrencia, lease, recuperación, killswitch, presupuesto temporal y preservación remota.
29. Documentación de usuario, documentación técnica, troubleshooting, matrices de soporte y criterios de release.
30. Cualquier feature nueva, renombrada, deprecada o removida que aparezca en la documentación o el código de la versión objetivo.

No marques la categoría como cubierta por mencionar solamente su nombre. Cada categoría debe descomponerse hasta unidades pequeñas, implementables y validables.

### Estructura mínima de `docs/ROADMAP.md`

El documento debe utilizar Markdown enriquecido compatible con GitHub y contener, como mínimo:

1. Título y objetivo.
2. Leyenda de estados.
3. Fecha UTC de la última auditoría.
4. SHA de `main` usado como baseline.
5. Versiones objetivo verificadas.
6. Índice navegable.
7. Fuentes oficiales y matriz de documentación consultada.
8. Matriz de compatibilidad.
9. Resumen ejecutivo de cobertura.
10. Roadmap jerárquico completo.
11. Registro de decisiones y dependencias.
12. Riesgos y bloqueos reales.
13. Evidencia de validación.
14. Historial breve de auditorías.
15. Próxima unidad prioritaria.

Usá obligatoriamente esta semántica visual:

```markdown
- [ ] ⚪ PENDIENTE — trabajo no iniciado.
- [ ] 🟡 EN CURSO — trabajo iniciado y preservado en una rama o PR remoto recuperable.
- [x] ✅ COMPLETADO — implementación y criterios de aceptación verificados.
- [ ] 🔁 REVALIDAR — existía evidencia, pero quedó obsoleta o perdió validez.
- [ ] ⛔ BLOQUEADO — existe un bloqueo externo real con evidencia.
```

Para un ítem completado usá siempre `[x]`. Para pendiente, en curso, revalidación o bloqueo usá `[ ]` junto con el marcador correspondiente. No representes un ítem incompleto como completado mediante texto ambiguo.

Cada unidad debe incluir, directamente o mediante subítems:

- identificador estable;
- nombre preciso;
- descripción técnica;
- justificación;
- dependencias;
- archivos o módulos previstos;
- pasos de implementación;
- configuración y opciones afectadas;
- perfil o perfiles afectados;
- riesgos técnicos;
- estrategia de fallback;
- pruebas requeridas;
- criterios de aceptación objetivos;
- evidencia actual;
- enlaces a documentación oficial;
- branch, commit, PR o check cuando exista;
- estado actual;
- siguiente acción concreta.

Descomponé las unidades hasta que cada checkbox represente trabajo que pueda completarse, validarse y actualizarse sin ocultar múltiples features independientes dentro de una sola línea.

### Capítulos obligatorios del roadmap

El roadmap debe reflejar y expandir toda la especificación compuesta. Como mínimo debe contener capítulos exhaustivos para:

1. Gobernanza, fuente de verdad remota y coordinación.
2. Bootstrap, estructura del repositorio y packaging.
3. Matriz de versiones y entorno soportado.
4. Auditoría completa de Iris y compatibilidad.
5. Arquitectura del pipeline y contratos de render.
6. Buffers, formatos, datos, uniforms y propiedades.
7. Sistema de materiales y PBR.
8. Iluminación, sombras y oclusión.
9. Cielo, atmósfera, nubes, clima y niebla.
10. Agua, vidrio, hielo, translucencia y partículas.
11. Reflejos, GI, screen-space y voxelización.
12. Acumulación temporal, TAA e historial.
13. Postprocesado y gestión de color.
14. Terreno, entidades, mano, block entities y dimensiones.
15. Perfiles de calidad, escalabilidad y degradación.
16. Rendimiento, presupuestos y seguridad CPU/GPU.
17. Compilación, análisis estático y validación OpenGL.
18. Pruebas visuales, métricas y benchmarks.
19. Integración Minecraft/Iris/Sodium en CI.
20. Workflows, automatización, recovery y releases.
21. Documentación, troubleshooting y soporte.
22. Criterios de release candidate y definición de completitud.

Si la especificación o la versión actual de Iris exige capítulos adicionales, agregalos. La lista anterior es un piso, no un techo.

### Reconciliación con el repositorio

Nunca marques `[x]` basándote solo en nombres de archivos, comentarios, intención, un commit existente o una afirmación previa.

Un ítem solo puede marcarse `COMPLETADO` cuando:

1. La implementación existe en el estado remoto inspeccionado.
2. Está integrada o preservada en una rama o PR remoto claramente identificado.
3. Satisface todos los criterios de aceptación del propio ítem.
4. Las pruebas exigidas existen y pasaron, o hay evidencia equivalente autorizada.
5. No existe un check fallido relevante.
6. La documentación y configuración asociadas están actualizadas.
7. La evidencia queda enlazada o identificada en el roadmap.

Si la implementación es parcial, carece de validación, tiene checks fallidos, fue revertida, quedó obsoleta por una actualización de Iris o no puede demostrarse, mantenela `EN CURSO`, `REVALIDAR` o `PENDIENTE`.

Si el repositorio y el roadmap se contradicen, la evidencia remota verificable tiene precedencia y el roadmap debe corregirse inmediatamente. También desmarcá ítems previamente completados cuando una regresión, cambio de versión, eliminación de código o pérdida de evidencia invalide su estado.

### Selección de trabajo

Solo después de publicar un roadmap válido:

1. Elegí la siguiente unidad pendiente de mayor prioridad que sea compatible con dependencias, riesgo y presupuesto temporal.
2. Marcala `🟡 EN CURSO`.
3. Registrá branch o PR de trabajo cuando exista.
4. Implementala siguiendo el proceso autónomo vigente.
5. No trabajes en features que no estén representadas en el roadmap; agregalas primero con su desglose, documentación y aceptación.

El roadmap controla el orden de trabajo, pero no reemplaza el razonamiento técnico. Reordená prioridades cuando aparezcan dependencias, regresiones, cambios de versión o riesgos nuevos, dejando la justificación registrada.

### Auditoría obligatoria al cierre

Antes de finalizar cualquier ciclo, liberar la lease o emitir el informe terminal, ejecutá `ROADMAP_RECONCILIATION`:

1. Volvé a leer el diff remoto y el estado final de la rama o PR.
2. Volvé a comparar los ítems afectados con código, documentación, tests y checks.
3. Marcá `[x] ✅ COMPLETADO` únicamente los ítems que cumplan íntegramente sus criterios.
4. Mantené `🟡 EN CURSO` para trabajo parcial preservado de forma remota y enlazá el checkpoint.
5. Devolvé a `⚪ PENDIENTE` cualquier trabajo no iniciado o no preservado.
6. Usá `🔁 REVALIDAR` cuando la evidencia anterior ya no sea suficiente.
7. Registrá bloqueos reales con evidencia y ruta de desbloqueo.
8. Actualizá fecha de auditoría, baseline, ramas, commits, PRs, checks, evidencias y próxima unidad.
9. Publicá la actualización final de `docs/ROADMAP.md` como commit documental aislado antes de liberar la lease.
10. Verificá remotamente que el roadmap publicado contiene los estados correctos.

No puede declararse `PASS` si el roadmap no fue reconciliado y publicado al cierre.

### Informe terminal obligatorio del roadmap

Añadí al informe terminal:

```text
Roadmap path: docs/ROADMAP.md
Roadmap audit status: CREATED | UPDATED | VERIFIED | INCOMPLETE
Roadmap baseline main SHA:
Roadmap commit inicial:
Roadmap commit final:
Fuentes oficiales de Iris auditadas:
Ítems marcados COMPLETADO:
Ítems mantenidos EN CURSO:
Ítems devueltos a PENDIENTE:
Ítems marcados REVALIDAR:
Bloqueos reales registrados:
Próxima unidad prioritaria:
```

La Capa 5 tiene precedencia sobre cualquier decisión táctica que permita comenzar implementación sin roadmap, omitir el inventario de Iris, conservar estados no demostrados o finalizar sin reconciliación.

## Protocolo obligatorio de carga

Antes de inspeccionar el entorno local, analizar `krestosa/Focal`, adquirir el lock o realizar cualquier mutación:

1. Leé este archivo desde la primera hasta la última línea.
2. Leé íntegramente la Capa 1.
3. Leé íntegramente la Capa 2 desde el commit exacto indicado.
4. Leé íntegramente la Capa 3.
5. Leé íntegramente la Capa 4.
6. Leé íntegramente la Capa 5.
7. Verificá que las cinco capas existen y pueden leerse completamente.
8. Tratá las cinco capas como un único prompt compuesto.
9. No resumas, condenses, parafrasees ni omitas ninguna sección.
10. No utilices copias locales, recordadas, cacheadas o provenientes de conversaciones anteriores.
11. Aplicá después el orden de precedencia definido abajo.
12. Ejecutá exactamente un ciclo autónomo sobre `krestosa/Focal`.

Si una capa no puede leerse por un error transitorio, reintentá mediante otra operación remota autorizada antes de concluir que es inaccesible.

## Orden de precedencia

Cuando exista una diferencia entre las capas, aplicá este orden:

1. Seguridad, límites de autorización y restricciones legales.
2. Hard killswitch y límite temporal absoluto.
3. Coordinación, propiedad de lease y protocolo body-only de la Capa 4.
4. Política de autonomía y bootstrap de la Capa 3.
5. Roadmap maestro vivo y auditoría integral de Iris de la Capa 5.
6. Correcciones vinculantes de este archivo.
7. Correcciones operativas consolidadas de la Capa 2 que no hayan sido reemplazadas.
8. Especificación técnica completa de la Capa 1.
9. Decisiones tácticas de la ejecución.

La Capa 4 reemplaza expresamente cualquier regla anterior que exija modificar `automation/run-state.json`, crear commits operativos, actualizar una rama de estado, usar compare-and-swap sobre un blob Git o publicar comentarios operativos.

La Capa 3 reemplaza expresamente cualquier regla anterior que convierta una carencia interna implementable en un bloqueo o que permita terminar el ciclo limitándose a informar que falta CI, checks, runtime guard, workflows, herramientas, validadores, tests, schemas, fixtures, configuración o infraestructura propia del repositorio.

La Capa 5 reemplaza expresamente cualquier regla anterior que permita implementar antes de crear o reconciliar el roadmap, tratar el roadmap como opcional, marcar trabajo sin evidencia o finalizar sin actualizar sus checkboxes y referencias remotas.

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
