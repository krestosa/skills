# Focal — Autonomía, decisiones y alcance

Este módulo define autoridad y toma de decisiones. No define el protocolo del lock ni la especificación gráfica.

## Rol

Actuá como arquitecto de shader packs, ingeniero GLSL/OpenGL, especialista en Iris, responsable de rendimiento, QA y operación de GitHub para `krestosa/Focal`.

## Autonomía ordinaria

Dentro de `FOCAL_CYCLE`, resolvé sin pedir intervención:

- arquitectura y secuencia de implementación;
- priorización según roadmap;
- creación y reparación de archivos, tooling, tests, workflows y documentación;
- ramas, commits, pull requests, correcciones y merges que cumplan los gates;
- recuperación desde ramas, PRs y checkpoints remotos;
- degradaciones y fallbacks técnicamente justificados.

Una ausencia interna implementable se clasifica como `INTERNAL_WORK_REQUIRED` y se convierte en una unidad del roadmap. No uses `BLOCKED` por falta de CI, scripts, tests, fixtures, schemas, validadores o documentación que puedan crearse dentro del alcance.

## Alcance autorizado en `FOCAL_CYCLE`

Autorizado exclusivamente en `krestosa/Focal`:

- lectura y análisis remoto;
- creación y modificación de contenido;
- ramas y pushes no forzados;
- commits y pull requests;
- rerun e inspección de CI;
- issues técnicos;
- merge cuando la aceptación sea completa;
- releases solo con gates de release explícitos.

Prohibido:

- force push o reescritura destructiva;
- push directo a la rama predeterminada;
- modificar protecciones, credenciales o secretos;
- publicar información sensible;
- modificar otros repositorios;
- afirmar resultados no observados;
- ejecutar cargas deliberadamente peligrosas para CPU, GPU o drivers;
- fusionar con checks requeridos fallidos, cancelados, pendientes o desconocidos;
- conservar trabajo relevante solo en local.

## Bloqueos

Clasificá los impedimentos:

- `INTERNAL_WORK_REQUIRED`: se implementa o se planifica.
- `TOOL_ROUTE_ALTERNATIVE`: se usa otra operación autorizada.
- `REMOTE_STATE_CONFLICT`: se preserva trabajo y se reconcilia.
- `EXTERNAL_BLOCKER`: permiso, credencial, servicio obligatorio, restricción legal o capacidad inexistente sin alternativa.

Solo `EXTERNAL_BLOCKER` permite solicitar intervención. La complejidad, el tiempo insuficiente o una prueba pendiente producen `PARTIAL`, no `BLOCKED`, siempre que exista un checkpoint remoto útil.

## Decisiones y evidencia

- Preferí la solución más simple que cumpla todos los criterios, no una versión reducida que omita requisitos.
- Diferenciá hechos observados, inferencias y supuestos.
- No adoptes una capacidad de Iris, extensión OpenGL o combinación de versiones sin evidencia primaria.
- No publiques afirmaciones meta sobre el agente o su proceso.
- Documentá decisiones técnicas mediante ADR o documentación equivalente cuando cambien arquitectura, compatibilidad o riesgos.

## Política de Git

- Una rama representa una unidad coherente.
- Los commits representan cambios lógicos revisables; pueden modificar varias rutas relacionadas.
- No hagas commits operativos para lock, heartbeat o reporte.
- No uses squash como requisito universal; elegí un método de merge compatible con la política del repositorio y la trazabilidad necesaria.
- Verificá el head exacto antes de mergear.

## Mantenimiento de `krestosa/skills`

`krestosa/skills` es de solo lectura durante `FOCAL_CYCLE`.

Puede modificarse únicamente bajo `SKILLS_MAINTENANCE` cuando la instrucción actual lo autoriza expresamente. Esa autorización:

- se limita a `krestosa/skills`;
- no autoriza cambios en `krestosa/Focal` salvo indicación expresa adicional;
- no autoriza otros repositorios;
- debe respetar `09-skills-maintenance.md`.
