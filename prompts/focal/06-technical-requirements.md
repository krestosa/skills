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

## Infraestructura y compatibilidad

Mantener:

- estructura válida del shader pack;
- programas, includes, propiedades, opciones y traducciones;
- matriz bloqueada de versiones y fuentes;
- empaquetado con `shaders/` en la raíz;
- compatibilidad y fallback para resource packs con y sin mapas de materiales;
- documentación de instalación, troubleshooting, licencias, atribuciones y release;
- CI reproducible y artefactos verificables.

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

## Cobertura de render

Validar terreno, mano, objetos sostenidos, entidades, block entities, partículas, clima, portales, beacons, encantamientos, resize, recarga, teletransporte, cambio de FOV y cambios de dimensión.

## Perfiles

Mantener cuatro perfiles coherentes:

- `SAFE`: máxima compatibilidad, sin dependencia obligatoria de compute, SSBO, tessellation o images avanzadas.
- `BALANCED`: perfil recomendado, coste moderado y features estables.
- `HIGH`: mayor precisión, sombras, reflejos, temporal y volumetría.
- `ULTRA`: máxima calidad validada con límites duros y degradación automática.

Cada perfil debe especificar features, resoluciones, muestras, memoria, fallbacks, hardware objetivo y criterios de aceptación. Ningún perfil puede habilitar parámetros ilimitados.

## Depuración y rendimiento

Proveer vistas o métricas para albedo, normales, profundidad, materiales, sombras, luz, AO, reflejos, volumetría, motion vectors, history, exposición, NaN/Inf, clipping, muestras y coste por pass.

Toda optimización requiere escenario, perfil, métrica, comparación antes/después y backend o hardware usado.
