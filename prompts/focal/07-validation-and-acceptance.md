# Focal — Pruebas, validación y aceptación

Este módulo define evidencia y resultados. Ningún cambio queda exento de determinar validaciones aplicables.

## Plan previo

Antes de editar, registrá para la unidad:

- criterios de aceptación;
- archivos y subsistemas;
- riesgos;
- pruebas requeridas;
- pruebas disponibles en el entorno;
- evidencia esperada;
- nivel de evidencia requerido: estático, OpenGL standalone, shader parcheado o cliente Iris;
- condición que impediría `PASS`.

## Validaciones por tipo

### Siempre aplicables

- estado remoto, base y head exactos;
- diff y referencias internas;
- ausencia de rutas o includes inexistentes;
- coherencia entre roadmap, matriz de Iris y documentación;
- enlaces oficiales de Iris presentes y vigentes para cada feature afectada;
- ausencia de secretos, binarios inesperados y texto no factual;
- validación del formato de archivos modificados.

### Shader pack

Cuando se modifiquen shaders o propiedades:

- estructura del pack;
- resolución y ciclos de includes;
- programas y stages;
- perfiles y dimensiones aplicables;
- parser o compilación GLSL disponible;
- interfaces, outputs, attachments y formatos;
- referencias de propiedades;
- análisis de loops, índices, divisores, NaN/Inf y límites;
- compile/link mediante `focal-gl compile` cuando el programa sea reproducible;
- render/readback mediante `focal-gl render` o `focal-gl suite` cuando exista comportamiento runtime verificable;
- cliente Iris cuando la aceptación dependa de patcher, geometría, estados o integración real.

Un parser o compilador sintáctico no reemplaza un contexto OpenGL real.

### `OPENGL_RUNTIME_HARNESS`

El programa `focal-gl` es una pieza obligatoria del producto y debe validarse como tooling y como runtime gráfico.

Pruebas mínimas del CLI:

```text
focal-gl probe --json
focal-gl compile --pack <path> --program <name> --json
focal-gl render --pack <path> --fixture <name> --artifacts <dir> --json
focal-gl suite --pack <path> --profile SAFE --json
```

La suite del harness debe comprobar:

- ayuda, argumentos inválidos y códigos de salida;
- creación de contexto real;
- reporte de vendor, renderer, versión, GLSL, perfil, extensiones y límites;
- selección y fallback de backend;
- compilación por stage;
- link de programas;
- framebuffer completeness;
- creación y formato de attachments;
- upload de geometría, texturas, samplers y buffers;
- draw o dispatch real;
- clears, barriers, mipmaps y ping-pong cuando correspondan;
- readback de color y depth;
- invariantes deterministas;
- detección de NaN/Inf;
- errores y debug messages OpenGL;
- timeout, crash, context loss y limpieza;
- JSON schema y artefactos;
- repetibilidad;
- diferenciación entre Mesa software y GPU/driver real.

El hito inicial del harness no se considera completo hasta que compile, enlace, renderice y lea de vuelta al menos un gbuffers-style, un composite-style y un `final` equivalente.

### Tooling, scripts y workflows

- tests unitarios;
- integración de CLI;
- fixtures;
- validación YAML/JSON/schema;
- permisos mínimos y timeouts;
- acciones fijadas cuando la política del repositorio lo requiera;
- simulación del coordinador sin mutar el issue real, salvo smoke test controlado;
- documentación de instalación y dependencias del CLI;
- comportamiento reproducible en entorno limpio.

### Packaging y release

- contenido y raíz del ZIP;
- exclusiones;
- reproducibilidad;
- versión y changelog;
- checksums;
- licencia y atribuciones;
- instalación y rollback documentados;
- inclusión o distribución documentada de `focal-gl`.

### Iris y visual

Cuando el entorno lo permita:

- carga y recarga en Iris;
- compilación dentro del cliente;
- logs y errores OpenGL;
- salida de Iris Patcher;
- capturas comparativas;
- escenas deterministas;
- perfiles y dimensiones;
- resize, teletransporte y discontinuidades;
- métricas de rendimiento y regresión.

La imposibilidad de ejecutar Minecraft no elimina las validaciones estáticas, de tooling, empaquetado, OpenGL o CI disponibles.

## Niveles de evidencia

Usá estos niveles en roadmap, PR y reporte:

1. `STATIC`: estructura, parsing, contratos y análisis.
2. `GL_COMPILE_LINK`: stages compilados y programa enlazado en un contexto real.
3. `GL_RENDER_READBACK`: draw/dispatch, framebuffer y readback verificados.
4. `IRIS_PATCHED`: salida transformada por Iris inspeccionada o ejecutada.
5. `IRIS_CLIENT`: pack cargado y ejercitado en el cliente bloqueado.

Reglas:

- `STATIC` no demuestra que el driver acepte o ejecute el shader.
- `GL_COMPILE_LINK` no demuestra salida correcta.
- `GL_RENDER_READBACK` no reproduce por sí solo Minecraft/Iris.
- `IRIS_PATCHED` no demuestra integración completa si no hubo cliente.
- `IRIS_CLIENT` debe registrar versiones, logs, hardware, driver, perfil y escena.

## Criterios runtime por clase de feature

- cambios puramente documentales: `STATIC`;
- includes, macros y contratos sin shader ejecutable: `STATIC`, con link oficial;
- shader stage o interfaz: mínimo `GL_COMPILE_LINK`;
- buffers, attachments, outputs, clears, blend, ping-pong o final: mínimo `GL_RENDER_READBACK`;
- temporal, history, reproyección o multipass: `GL_RENDER_READBACK` multiframe;
- Iris Patcher, reserved names o transformación: `IRIS_PATCHED`;
- geometría Minecraft, render states, dimensiones, entidades o compatibilidad Sodium: `IRIS_CLIENT`;
- rendimiento: evidencia en backend/hardware declarado, nunca extrapolación universal.

## CI del harness

La CI debe ejecutar, cuando el entorno lo permita:

- `focal-gl probe` sobre Mesa software;
- fixtures SAFE de compile/link;
- render/readback offscreen;
- invariantes deterministas;
- watchdog y timeout tests;
- publicación de JSON, logs e imágenes como artefactos ante fallo;
- matriz separada para capacidades OpenGL avanzadas cuando estén disponibles.

Un resultado Mesa software:

- prueba reproducibilidad funcional de esa ruta;
- no prueba rendimiento;
- no prueba drivers NVIDIA/AMD/Intel;
- no permite afirmar compatibilidad universal.

La evidencia de GPU real debe provenir de runner apropiado o procedimiento manual reproducible y quedar enlazada.

## Pruebas no ejecutables

Cuando una prueba requerida no pueda ejecutarse:

1. no inventes el resultado;
2. registrá el nombre exacto;
3. explicá la limitación;
4. indicá comando, entorno o procedimiento para ejecutarla;
5. enlazá el ítem afectado;
6. dejalo `REVALIDAR` si la prueba es necesaria para aceptación;
7. no declares `PASS`;
8. ejecutá todas las capas inferiores disponibles;
9. conservá el reporte `UNSUPPORTED` separado de `FAIL`.

## CI y corrección

- Inspeccioná checks del head exacto.
- Un check requerido fallido debe corregirse antes de merge.
- Un check pendiente, cancelado, omitido o desconocido no es verde.
- Si el fallo es ajeno al cambio, documentá evidencia y conservá `PARTIAL`; no lo declares aprobado.
- No esperes indefinidamente. Publicá checkpoint y terminá antes del límite.
- Después del merge, verificá el SHA de la rama predeterminada y los checks post-merge disponibles.

## Criterios de merge

Puede mergearse cuando:

- la lease sigue siendo propia;
- el head revisado no cambió;
- la base sigue siendo válida o fue reconciliada;
- todos los criterios aplicables están satisfechos;
- pruebas obligatorias y checks requeridos están verdes;
- no existe revisión bloqueante;
- documentación y roadmap de la PR son coherentes para el estado previo al merge;
- cada feature afectada mantiene enlaces oficiales de Iris;
- el nivel de evidencia alcanzado coincide con la clase de feature.

No mergees para fabricar evidencia.

## Resultados

### `PASS`

Exige:

- objetivo del ciclo cumplido;
- cambios publicados;
- implementación requerida presente en la rama predeterminada;
- pruebas obligatorias aprobadas;
- CI aplicable verde;
- `ROADMAP_RECONCILIATION` publicada en la rama predeterminada;
- matriz de Iris actualizada cuando correspondía;
- lease liberada y `idle` confirmado.

Un ciclo que afirma aceptación runtime sin la evidencia OpenGL o Iris requerida no puede ser `PASS`.

### `PARTIAL`

Existe avance remoto útil, pero falta merge, prueba, CI, reconciliación final o aceptación completa.

### `BLOCKED`

Existe una restricción externa real sin alternativa autorizada, o el coordinador/permiso indispensable impide operar.

### `NO-OP`

No se realizó trabajo funcional porque otra lease estaba activa, no existía unidad válida o el estado remoto ya satisfacía el objetivo.

No uses `PASS` para una PR abierta, trabajo solo local, pruebas faltantes, CI desconocida, roadmap sin reconciliar o lock sin liberar.
