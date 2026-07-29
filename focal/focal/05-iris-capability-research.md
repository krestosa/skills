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

Índice primario recomendado:

- https://shaders.properties/current/reference/overview/
- https://shaders.properties/current/reference/programs/overview/
- https://shaders.properties/current/reference/buffers/overview/
- https://shaders.properties/current/reference/uniforms/overview/
- https://shaders.properties/current/reference/attributes/overview/
- https://shaders.properties/current/reference/constants/overview/
- https://shaders.properties/current/reference/shadersproperties/overview/
- https://shaders.properties/current/reference/miscellaneous/patcher/
- https://shaders.properties/current/reference/miscellaneous/debugging_shaders/
- https://shaders.properties/current/reference/miscellaneous/macos/
- https://github.com/IrisShaders/Iris
- https://github.com/IrisShaders/docs
- https://github.com/IrisShaders/ShaderDoc

Una fuente secundaria puede orientar búsqueda, pero no ser la única base de una decisión importante. Registrá URL, fecha UTC y versión, tag, rama o commit cuando exista.

No uses memoria del modelo como evidencia.

## Enlaces obligatorios dentro del roadmap

La matriz centraliza evidencia, pero **no reemplaza los enlaces directos dentro de cada feature de `docs/ROADMAP.md`**.

Para cada ítem del roadmap:

1. agregá un campo `Iris docs`;
2. enlazá una o más páginas primarias oficiales específicas;
3. preferí la página exacta del programa, buffer, uniform, attribute, constant, macro, propiedad, patcher o limitación;
4. evitá enlazar solo la portada cuando haya una página más precisa;
5. registrá la fecha UTC de revisión;
6. verificá que el enlace siga disponible y respalde la afirmación;
7. si no existe documentación específica, enlazá código, issue o PR oficial y documentá esa ausencia;
8. mantené el enlace aunque la capacidad sea `NO SOPORTADA` o `PENDIENTE DE VERIFICAR`.

Un ítem sin enlace primario oficial no puede marcarse `COMPLETADO`.

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
- fuente primaria, URL directa y fecha de revisión;
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
- implicaciones de rendimiento y límites conocidos;
- diferencia entre validación OpenGL standalone y ejecución real dentro de Iris.

## Capacidad obligatoria de validación runtime

La matriz debe contener una entrada estable para `OPENGL_RUNTIME_HARNESS` que documente:

- qué partes del formato Iris puede reproducir el programa standalone;
- qué shaders consume: fuente original, fuente preprocesada o salida de Iris Patcher;
- contexto OpenGL, versión, perfil, backend y extensiones requeridas;
- programas, stages, buffers, attachments, uniforms, atributos y propiedades emulados por fixtures;
- límites de fidelidad respecto del pipeline real de Minecraft/Iris;
- evidencia requerida para Mesa software, GPU/driver real y cliente Iris;
- fallback y estado cuando el contexto o una feature no estén soportados;
- relación con los ítems `GLCLI-*`, `QA-*` e `INT-*` del roadmap.

La documentación oficial confirma que Iris transforma el código antes de compilarlo. Por lo tanto, una compilación standalone de la fuente original no prueba por sí sola que Iris vaya a aceptar el pack. El roadmap y los reportes deben distinguir:

1. análisis estático;
2. compilación/link OpenGL standalone;
3. render offscreen standalone;
4. ejecución de salida parcheada;
5. carga y render dentro de Iris/Minecraft.

## Integración con roadmap

Cada ítem técnico relevante del roadmap debe enlazar:

- capacidades necesarias;
- restricciones del pipeline;
- passes y recursos afectados;
- estrategia de fallback;
- pruebas;
- perfiles de rendimiento;
- URLs directas de la documentación oficial aplicable.

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
5. registrá la fecha de revisión;
6. verificá todos los enlaces oficiales usados por las features afectadas;
7. verificá el estado de `OPENGL_RUNTIME_HARNESS`.

Durante `ROADMAP_RECONCILIATION`, actualizá únicamente capacidades confirmadas, refutadas o limitadas por evidencia del ciclo.
