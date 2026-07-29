# Focal — Requisitos técnicos y gráficos

Este módulo define el producto. Las capacidades concretas dependen de la matriz de Iris y del roadmap.

## Objetivo

Desarrollar y mantener un shader pack para el objetivo de Minecraft definido por el proyecto, actualmente declarado como Minecraft Java 26.2 sujeto a verificación oficial, usando una combinación estable y mutuamente compatible de Iris, Sodium y Fabric Loader.

La representación debe ser físicamente plausible, temporalmente estable, escalable y honesta respecto de sus técnicas. No afirmes ray tracing por hardware ni compatibilidad universal sin evidencia.

## Principios de arquitectura

- Pipeline HDR coherente y documentado.
- Fallback determinista por capacidad y perfil.
- Ningún pass avanzado obligatorio para el perfil de máxima compatibilidad.
- Loops, ray marches, muestras, resoluciones y memoria con límites duros.
- Reinicio de history ante discontinuidades.
- Prevención de NaN, Inf, divisiones por cero, normalizaciones nulas, lecturas fuera de rango y recursos sin ciclo de vida.
- Presupuestos medibles por pass y perfil.
- Evitar explosión de permutaciones.
- Cambios arquitectónicos respaldados por evidencia de Iris y ADR cuando corresponda.
- Separar siempre evidencia estática, OpenGL standalone e integración real con Iris.

## Infraestructura y compatibilidad

Mantener:

- estructura válida del shader pack;
- programas, includes, propiedades, opciones y traducciones;
- matriz bloqueada de versiones y fuentes;
- empaquetado con `shaders/` en la raíz;
- compatibilidad y fallback para resource packs con y sin mapas de materiales;
- documentación de instalación, troubleshooting, licencias, atribuciones y release;
- CI reproducible y artefactos verificables.

## `OPENGL_RUNTIME_HARNESS`

Focal debe construir y mantener un programa ejecutable desde terminal, sin interfaz gráfica obligatoria, que cree un contexto OpenGL real y permita comprobar compile, link, ejecución y salida de los shaders fuera de Minecraft.

El nombre canónico de la interfaz debe ser `focal-gl`. Puede implementarse como ejecutable nativo, módulo o wrapper de script, pero el repositorio debe ofrecer un comando estable y documentado.

### Comandos mínimos

```text
focal-gl probe
focal-gl compile
focal-gl render
focal-gl suite
```

El CLI debe admitir como mínimo:

- raíz del shader pack;
- programa o pass;
- perfil Focal;
- dimensión o fixture;
- backend de contexto;
- versión y perfil OpenGL solicitados;
- tamaño de framebuffer;
- cantidad de frames;
- timeout;
- directorio de artefactos;
- salida humana y `--json`.

### `probe`

Debe crear un contexto real y reportar:

- backend usado;
- `GL_VENDOR`, `GL_RENDERER`, `GL_VERSION` y versión GLSL;
- perfil core/compatibility;
- extensiones y límites relevantes;
- soporte de compute, geometry, tessellation, images y SSBO;
- formatos y cantidad de color attachments;
- disponibilidad de framebuffer, timer queries y debug output;
- motivo factual cuando una capacidad no está disponible.

Backends esperados, según plataforma y disponibilidad:

- EGL surfaceless o pbuffer en Linux;
- contexto oculto GLFW como fallback controlado;
- WGL oculto en Windows;
- CGL/NSOpenGL o equivalente permitido en macOS;
- Mesa llvmpipe o software renderer para CI;
- GPU/driver real para evidencia de hardware.

No simules un contexto. Un parser GLSL, transpiler o mock no satisface `probe`.

### `compile`

Debe:

- resolver includes y defines del fixture;
- registrar si consume fuente original, preprocesada o salida de Iris Patcher;
- compilar cada stage aplicable;
- enlazar el programa completo;
- capturar logs íntegros y mapearlos a archivos cuando sea posible;
- verificar interfaces, varyings, outputs, bindings y stages obligatorios;
- fallar ante warnings configurados como error;
- producir reporte JSON por programa y stage.

La fuente original no es necesariamente la fuente que Iris envía a la GPU. El CLI debe exponer `sourceMode` y distinguir al menos:

- `source`;
- `preprocessed`;
- `iris-patched`.

No declares compatibilidad Iris completa basándote solo en `source`.

### `render`

Debe ejecutar trabajo real de GPU o software OpenGL:

- crear VAO/VBO/IBO o fullscreen triangle/quad según el programa;
- crear texturas, samplers, UBO/SSBO/images cuando correspondan;
- crear framebuffer y attachments con formatos definidos;
- cargar fixtures deterministas;
- inyectar uniforms, atributos, matrices, cámara, tiempo, clima, IDs y opciones necesarios;
- ejecutar draw o dispatch;
- aplicar barreras, mipmaps, clears, ping-pong y secuencias multipass declaradas;
- leer color y depth;
- generar imagen o datos de salida;
- verificar `glGetError`, debug messages, framebuffer completeness y límites;
- detectar NaN/Inf y valores fuera de contrato;
- comparar invariantes, tolerancias o hashes de referencia;
- repetir para comprobar determinismo.

El primer hito mínimo debe renderizar al menos:

1. un programa gbuffers-style vertex/fragment sobre geometría determinista;
2. un pass composite-style sobre un attachment;
3. el pass `final` hacia un backbuffer offscreen o attachment equivalente;
4. readback verificable.

### `suite`

Debe ejecutar una matriz declarativa de fixtures y producir:

- resumen PASS/FAIL/SKIP/UNSUPPORTED;
- versión del harness;
- hash del shader pack;
- plataforma, driver, backend y capacidades;
- tiempos por compile/link/render/readback;
- artefactos PNG o equivalentes;
- logs de OpenGL y shader;
- JSON machine-readable;
- manifest de resultados.

### Seguridad y aislamiento

Cada prueba OpenGL potencialmente riesgosa debe ejecutarse en proceso aislado con:

- watchdog;
- timeout duro;
- terminación y limpieza;
- límites de resolución, frames, dispatch, memoria y muestras;
- prohibición de loops o parámetros ilimitados;
- artefactos parciales conservados;
- distinción entre crash del proceso, context loss, timeout y fallo de shader.

No ejecutes pruebas de alto riesgo en el mismo proceso que coordina GitHub.

### Códigos de salida

El contrato debe ser estable:

- `0`: todas las comprobaciones requeridas aprobaron;
- `2`: uso o configuración inválida;
- `3`: contexto OpenGL no disponible;
- `4`: compilación o link fallido;
- `5`: error OpenGL, framebuffer o ejecución;
- `6`: invariante visual o de datos fallida;
- `7`: timeout, crash o context loss;
- `8`: capacidad no soportada sin fallback aceptable.

Los códigos pueden ampliarse, pero no cambiar significado sin versión mayor del CLI.

### Fidelidad y límites

El harness standalone es obligatorio, pero no sustituye Iris:

- Iris transforma GLSL mediante su patcher;
- Minecraft aporta geometría, estados, recursos, uniforms y orden real;
- algunos comportamientos dependen de Sodium, mods, dimensión y driver;
- llvmpipe confirma una ruta OpenGL reproducible, no rendimiento ni compatibilidad de vendor;
- una GPU real confirma ese driver, no universalidad;
- la aceptación final de integración requiere cliente Iris bloqueado.

Los reportes deben indicar explícitamente el nivel de evidencia alcanzado:

1. estático;
2. compile/link standalone;
3. render/readback standalone;
4. shader parcheado;
5. cliente Iris.

## Pipeline y recursos

Diseñar y documentar, según soporte confirmado:

- gbuffers y deferred o equivalente;
- shadow pipeline;
- composite passes y final pass;
- color/depth attachments y render targets;
- historial, previous-frame data, reproyección y motion vectors;
- formatos, clear, mipmaps, ping-pong, escalado y viewport;
- custom textures, images, SSBO o compute solo con soporte verificado;
- gestión de dimensiones y fallbacks.

Todo pass nuevo debe incorporarse a fixtures del `OPENGL_RUNTIME_HARNESS` cuando sea técnicamente reproducible.

## Materiales

Cubrir progresivamente:

- albedo y color lineal;
- normal mapping;
- specular, roughness y metalness cuando la convención lo permita;
- emisivos;
- AO y porosidad cuando corresponda;
- POM con límites estrictos;
- superficies húmedas;
- transmisión y subsurface scattering aproximado cuando sea viable;
- protección ante mapas faltantes o valores extremos.

## Iluminación y sombras

Incluir rutas verificables para:

- sol, luna, skylight y block light;
- iluminación directa e indirecta aproximada;
- GI de espacio de pantalla o voxelizada condicionada;
- oclusión ambiental;
- conservación de energía y control de fireflies;
- mapas de sombra, cascadas cuando sean adecuadas, penumbra, contacto y translucencia;
- bias, acne, peter-panning y estabilidad temporal;
- fallbacks por perfil y hardware.

## Mundo y atmósfera

Cubrir:

- cielo, sol, luna, estrellas y perspectiva aérea;
- dispersión atmosférica, niebla y volumetría;
- nubes y clima;
- lluvia, nieve, tormentas y relámpagos;
- agua, hielo, vidrio y otras transparencias;
- reflexión, refracción, Fresnel, absorción, scattering, ondas y caústicas;
- vista submarina;
- Overworld, Nether, End y dimensiones modificadas.

## Temporal, reflejos y postproceso

Cubrir con aceptación cuantitativa:

- SSR con límites y fallback;
- SSGI o equivalente cuando sea viable;
- TAA, acumulación temporal, reproyección y rechazo de history;
- reducción de ghosting y disocclusion;
- exposición manual/automática;
- tonemapping y gestión de color;
- white balance y color grading controlado;
- bloom;
- sharpening y dithering;
- FXAA como fallback;
- DOF y motion blur opcionales y desactivados por defecto salvo decisión documentada.

Los efectos temporales deben incluir fixtures multiframe, discontinuidades y readback de history en `focal-gl suite`.

## Cobertura de render

Validar terreno, mano, objetos sostenidos, entidades, block entities, partículas, clima, portales, beacons, encantamientos, resize, recarga, teletransporte, cambio de FOV y cambios de dimensión.

## Perfiles

Mantener cuatro perfiles coherentes:

- `SAFE`: máxima compatibilidad, sin dependencia obligatoria de compute, SSBO, tessellation o images avanzadas.
- `BALANCED`: perfil recomendado, coste moderado y features estables.
- `HIGH`: mayor precisión, sombras, reflejos, temporal y volumetría.
- `ULTRA`: máxima calidad validada con límites duros y degradación automática.

Cada perfil debe especificar features, resoluciones, muestras, memoria, fallbacks, hardware objetivo y criterios de aceptación. Ningún perfil puede habilitar parámetros ilimitados.

`focal-gl suite` debe poder seleccionar cada perfil y reportar capacidades faltantes o degradaciones aplicadas.

## Depuración y rendimiento

Proveer vistas o métricas para albedo, normales, profundidad, materiales, sombras, luz, AO, reflejos, volumetría, motion vectors, history, exposición, NaN/Inf, clipping, muestras y coste por pass.

Toda optimización requiere escenario, perfil, métrica, comparación antes/después y backend o hardware usado.

El harness debe registrar por separado tiempo de contexto, preprocessado, compile, link, upload, draw/dispatch, synchronization y readback cuando la plataforma lo permita.
