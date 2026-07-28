# Focal — Investigación y matriz de capacidades de Iris

Este módulo define la investigación técnica de Iris. No afirma que una capacidad exista: exige verificarla.

## Documento canónico

```text
krestosa/Focal:docs/IRIS-CAPABILITY-MATRIX.md
```

Debe existir un único documento activo y estar enlazado desde `docs/ROADMAP.md`.

## Fuentes

Antes de tomar una decisión dependiente de Iris, consultá fuentes actuales y primarias mediante rutas autorizadas:

1. repositorio oficial `IrisShaders/Iris`;
2. releases, tags y código fuente oficiales;
3. documentación oficial de Iris;
4. `IrisShaders/docs` y `IrisShaders/ShaderDoc` cuando sean aplicables;
5. documentación oficial de shader packs en `shaders.properties`;
6. issues y pull requests oficiales para limitaciones concretas.

Una fuente secundaria puede orientar búsqueda, pero no ser la única base de una decisión importante. Registrá URL, fecha UTC y versión, tag, rama o commit cuando exista.

No uses memoria del modelo como evidencia.

## Estados de capacidad

Cada entrada debe usar uno:

- `SOPORTADA`;
- `PARCIAL`;
- `EXPERIMENTAL`;
- `NO SOPORTADA`;
- `PENDIENTE DE VERIFICAR`.

Una capacidad no confirmada permanece `PENDIENTE DE VERIFICAR`.

## Campos mínimos

Cada capacidad debe registrar:

- identificador y nombre;
- estado;
- Minecraft, Iris, Sodium y Fabric Loader comprobados;
- fuente primaria y fecha de revisión;
- descripción factual;
- restricciones y divergencias respecto de convenciones de OptiFine cuando estén documentadas;
- impacto sobre Focal;
- ítems del roadmap relacionados;
- passes, buffers, uniforms o propiedades afectados;
- fallback;
- estrategia de prueba;
- riesgos de compatibilidad y rendimiento.

## Cobertura mínima

La matriz debe cubrir, según corresponda:

- combinación estable y mutuamente compatible de Minecraft, Iris, Sodium, Fabric Loader, Java y OpenGL/GLSL;
- formato, estructura, includes, macros, preprocessado y descubrimiento del shader pack;
- programas, sufijos y orden de ejecución;
- etapas vertex, fragment, geometry, tessellation y compute;
- `setup`, `begin`, `shadow`, `shadowcomp`, `prepare`, `gbuffers_*`, `deferred`, `composite` y `final`;
- buffers de color, profundidad, sombra, historial y attachments;
- formatos, clear, mipmaps, ping-pong, viewport y escalado;
- `DRAWBUFFERS`, `RENDERTARGETS`, directivas y comentarios especiales;
- uniforms, atributos, varyings, matrices, datos de cámara, mundo, tiempo, clima, entidades y previous-frame;
- `shaders.properties`, feature flags, custom uniforms, textures, images, SSBO y orden de programas;
- perfiles, pantallas, sliders, defines, subscreens, columnas y archivos `.lang`;
- mapeos de bloques, ítems, entidades, block entities, biomas y dimensiones;
- shadow, deferred, composite y final pipeline;
- temporal data, matrices previas, depth buffers, color attachments y noise/custom textures;
- image load/store, compute, indirect dispatch y voxelización cuando estén permitidos;
- limitaciones de OpenGL y proveedor de GPU;
- Iris Patcher, transformación GLSL, nombres reservados y diagnóstico;
- divergencias respecto de OptiFine, funcionalidades no soportadas y workarounds;
- comportamiento en Overworld, Nether, End y dimensiones modificadas;
- compatibilidad confirmada con Sodium, resource packs e integraciones;
- implicaciones de rendimiento y límites conocidos.

## Integración con roadmap

Cada ítem técnico relevante del roadmap debe enlazar:

- capacidades necesarias;
- restricciones del pipeline;
- passes y recursos afectados;
- estrategia de fallback;
- pruebas;
- perfiles de rendimiento.

Cuando una unidad dependa de una capacidad `PENDIENTE DE VERIFICAR`, `PARCIAL` o `EXPERIMENTAL` sin prueba suficiente:

- no puede quedar `COMPLETADO`;
- debe quedar `REVALIDAR` o `BLOQUEADO`;
- debe incluir una acción concreta de investigación o experimento acotado.

## Actualización por ciclo

Durante `ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT`:

1. verificá la combinación objetivo y la vigencia de fuentes relevantes para la unidad;
2. compará la matriz con el código y la documentación de Focal;
3. agregá capacidades omitidas;
4. corregí afirmaciones refutadas;
5. registrá la fecha de revisión.

Durante `ROADMAP_RECONCILIATION`, actualizá únicamente capacidades confirmadas, refutadas o limitadas por evidencia del ciclo.
