# Focal — Roadmap y reconciliación

Este módulo define `docs/ROADMAP.md`, la selección de trabajo y las dos fases obligatorias del ciclo.

## Documento canónico

```text
krestosa/Focal:docs/ROADMAP.md
```

No mantengas otro roadmap activo. Issues, proyectos y PRs pueden aportar evidencia, pero no reemplazan este documento.

## Estados canónicos

Usá exactamente:

```markdown
- [ ] ⚪ PENDIENTE
- [ ] 🟡 EN PROGRESO
- [x] 🟢 COMPLETADO
- [ ] 🟣 REVALIDAR
- [ ] 🔴 BLOQUEADO
```

No uses checkbox marcada para trabajo incompleto.

## Fase `ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT`

Después de adquirir la lease y antes de elegir trabajo funcional:

1. Resolvé nuevamente el SHA remoto actual de la rama predeterminada.
2. Inspeccioná el árbol, documentación, issues, ramas, PRs, commits, workflows, checks y releases relevantes.
3. Verificá si existe `docs/ROADMAP.md`.
4. Si no existe, crealo y publicalo antes de desarrollar una feature.
5. Si existe, leelo íntegramente.
6. Auditá duplicados, estados ambiguos, dependencias, evidencia y siguientes acciones.
7. Compará cada afirmación con el estado de la rama predeterminada.
8. Detectá funcionalidad implementada no registrada.
9. Desmarcá o mové a `REVALIDAR` cualquier completado sin evidencia suficiente.
10. Ejecutá la auditoría de Iris de `05-iris-capability-research.md`.
11. Verificá los vínculos entre roadmap y matriz de Iris.
12. Verificá que cada feature tenga alcance, aceptación, pruebas y enlaces oficiales de Iris.
13. Verificá que exista la unidad obligatoria `OPENGL_RUNTIME_HARNESS` y que no esté absorbida por una tarea genérica de QA.
14. Publicá el bootstrap o corrección documental si cambió.
15. Solo entonces seleccioná una unidad.

La ausencia o invalidez grave del roadmap es bloqueante para desarrollo funcional y constituye la unidad prioritaria del ciclo.

## Granularidad obligatoria por feature

El roadmap debe describir **cada feature técnica o visual como una unidad identificable y verificable**. No alcanza con una línea como “sombras”, “agua”, “materiales”, “OpenGL harness” o “compatibilidad”.

Una feature puede agrupar trabajo interno inseparable, pero debe separarse cuando cambien cualquiera de estos factores:

- resultado observable;
- pass o familia de programas;
- capacidad o restricción de Iris;
- perfil o fallback;
- estrategia de prueba;
- dependencia arquitectónica;
- riesgo de rendimiento o compatibilidad;
- criterio de aceptación.

No atomices en tareas microscópicas, pero tampoco ocultes múltiples features independientes dentro de un único ítem amplio.

## Estructura obligatoria de cada ítem

Cada ítem debe tener un identificador estable, por ejemplo `FOCAL-LIGHT-001`, y conservarlo al reordenarse. Puede representarse como subsección o fila de tabla siempre que todos los campos permanezcan explícitos y legibles.

Incluí:

- estado canónico, prioridad y clasificación;
- título inequívoco;
- alcance y resultado observable;
- exclusiones o límites;
- dependencias;
- criterios de aceptación medibles;
- pruebas estáticas, unitarias, OpenGL, visuales, de integración y de rendimiento aplicables;
- comando o procedimiento de prueba;
- evidencia remota;
- capacidades de Iris relacionadas;
- **campo `Iris docs` con uno o más enlaces clickeables a documentación primaria oficial**;
- passes, buffers, uniforms, atributos, propiedades, perfiles y fallbacks afectados;
- archivos o subsistemas previstos;
- riesgos y presupuesto;
- siguiente acción concreta;
- motivo y evidencia del bloqueo cuando corresponda.

Quedan prohibidos los ítems activos de una sola frase que omitan aceptación, pruebas o documentación.

## Política de enlaces oficiales de Iris

Cada feature debe enlazar directamente la página oficial más específica disponible, preferentemente bajo:

- `https://shaders.properties/current/reference/`;
- `https://github.com/IrisShaders/Iris`;
- `https://github.com/IrisShaders/docs`;
- `https://github.com/IrisShaders/ShaderDoc`.

Reglas:

1. El enlace debe estar dentro del propio ítem del roadmap; una referencia a la matriz sin enlace directo no es suficiente.
2. Usá la página específica de programas, buffers, uniforms, attributes, constants, `shaders.properties`, patcher, debugging o limitaciones cuando exista.
3. No uses una homepage genérica si hay una página más precisa.
4. Registrá `Revisado UTC` para el conjunto de enlaces o para el ítem.
5. Verificá que el enlace responda y siga sosteniendo la afirmación antes de marcar `COMPLETADO`.
6. Si no existe documentación específica, enlazá código, issue o PR oficial y explicá la ausencia.
7. Un enlace secundario puede orientar, pero no reemplaza la fuente primaria.
8. Las referencias Markdown reutilizables son válidas si resuelven a URLs clickeables dentro de `docs/ROADMAP.md`.

## Unidad obligatoria `OPENGL_RUNTIME_HARNESS`

El roadmap debe contener una familia propia, priorizada y detallada para construir un programa ejecutable por terminal que cree un contexto OpenGL real y renderice fixtures de Focal fuera de Minecraft.

Como mínimo debe separar:

- CLI y contrato de comandos;
- detección de plataforma, backend, versión, extensiones y límites;
- creación de contexto OpenGL offscreen;
- preprocessado o consumo de shaders transformados;
- compilación y link por stage/programa;
- creación de buffers, texturas, samplers, framebuffer y attachments;
- render determinista de geometría y fullscreen passes;
- inyección de uniforms, atributos, defines y recursos de fixture;
- ejecución de secuencias multipass y ping-pong;
- lectura de color/depth y generación de artefactos;
- invariantes de píxeles, NaN/Inf, errores OpenGL y determinismo;
- aislamiento de proceso, watchdog y timeout;
- reporte JSON, logs, imágenes y códigos de salida;
- ejecución con Mesa software en CI y validación diferenciada sobre GPU/driver real;
- adaptación a Iris Patcher y evidencia de cliente, sin confundir el harness standalone con compatibilidad completa de Iris.

La falta de este harness impide declarar aceptación runtime general de shaders, buffers, attachments, temporal, postproceso o perfiles avanzados.

## Cobertura mínima obligatoria

El roadmap debe cubrir, adaptado a la evidencia real:

1. **Fundación y distribución:** infraestructura del pack, versiones objetivo, estructura de programas y passes, buffers y render targets, CI, empaquetado, releases, licencias y atribuciones.
2. **Pipeline:** deferred o equivalente, shadow pipeline, composite/final, attachments, depth, historial, custom textures y gestión de recursos.
3. **Materiales:** PBR, mapas de normales y specular, roughness/metallic cuando correspondan, emisivos, AO, parallax y subsurface aproximado viable.
4. **Iluminación:** directa, indirecta, block light, skylight, GI aproximada, voxelización condicionada, oclusión ambiental y conservación de energía.
5. **Sombras:** mapas de sombra, cascaded shadow maps cuando sean viables, filtrado, penumbra, contacto, translucencia, estabilidad y fallbacks.
6. **Mundo:** cielo, nubes, atmósfera, niebla, clima, agua, hielo, vidrio, transparencias, partículas y volumetría.
7. **Temporal y postproceso:** exposición, tonemapping, gestión de color, bloom, reflejos, SSR, TAA, acumulación, reproyección, motion vectors, reducción de ghosting y sharpen.
8. **Cobertura de render:** terreno, entidades, block entities, mano, objetos sostenidos, partículas, clima, portales y escenas especiales.
9. **Dimensiones:** Overworld, Nether, End y dimensiones modificadas con fallback.
10. **Compatibilidad:** Iris, Sodium, resource packs con y sin materiales, integraciones confirmadas, GPU, drivers y degradación por hardware.
11. **Configuración:** perfiles de rendimiento, opciones, pantallas, traducciones, límites y defaults seguros.
12. **Calidad:** depuración, logs, análisis estático, compilación, `OPENGL_RUNTIME_HARNESS`, capturas comparativas, benchmarks, pruebas visuales, regresiones y documentación técnica y de usuario.

Cada capacidad debe clasificarse; no presupongas que todas son obligatorias ni viables.

## Evidencia de completado

`🟢 COMPLETADO` exige simultáneamente:

- implementación presente en la rama predeterminada;
- criterios de aceptación satisfechos;
- pruebas requeridas aprobadas;
- workflow remoto exitoso cuando sea aplicable;
- documentación actualizada;
- enlaces oficiales de Iris revisados;
- evidencia enlazada;
- ausencia de bloqueo conocido que invalide el resultado.

No alcanza con código local, rama, commit sin merge, PR abierta, revisión parcial o impresión subjetiva.

Una feature que requiere ejecución OpenGL no puede quedar `COMPLETADO` solo por parsing, análisis estático o compilación sintáctica. Debe incluir evidencia del harness o permanecer `REVALIDAR`.

## Prioridad de selección

Después de la fase inicial:

1. restaurar compilación, validación o estabilidad;
2. resolver bloqueos;
3. construir o completar `OPENGL_RUNTIME_HARNESS` hasta disponer de compile/link/render/readback mínimo;
4. completar infraestructura compartida;
5. continuar `EN PROGRESO`;
6. revisar `REVALIDAR`;
7. implementar prioridad alta;
8. investigar documentación necesaria;
9. mejorar visual o rendimiento con medición.

No selecciones una unidad ausente del roadmap.

## Fase `ROADMAP_RECONCILIATION`

Después de implementación, pruebas, publicación, PR y merge disponible:

1. Obtené nuevamente el estado remoto.
2. Releé íntegramente `docs/ROADMAP.md`.
3. Compará plan, cambios, pruebas, PR, merge y rama predeterminada.
4. Actualizá todos los ítems afectados.
5. Usá `COMPLETADO` solo para evidencia ya presente en la rama predeterminada.
6. Conservá `EN PROGRESO` para avance remoto real todavía incompleto.
7. Volvé a `PENDIENTE` lo no iniciado.
8. Usá `REVALIDAR` para implementación sin validación suficiente o evidencia obsoleta.
9. Usá `BLOQUEADO` solo para restricción externa comprobada.
10. Agregá enlaces de evidencia, enlaces oficiales de Iris y siguiente acción.
11. Actualizá la matriz de Iris cuando haya nueva evidencia.
12. Eliminá afirmaciones no respaldadas.
13. Confirmá coherencia con la rama predeterminada.
14. Confirmá que ninguna feature runtime se marcó completa sin la clase de prueba OpenGL o cliente que exige.

Si una implementación solo existe en una PR no mergeada, no puede figurar como completada.

Cuando el merge funcional ya ocurrió, realizá la reconciliación documental en una rama/PR posterior o equivalente y mergeala si los gates lo permiten. `PASS` exige que la reconciliación final esté publicada en la rama predeterminada. Si queda abierta, el ciclo es `PARTIAL`.
