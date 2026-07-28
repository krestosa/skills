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
- condición que impediría `PASS`.

## Validaciones por tipo

### Siempre aplicables

- estado remoto, base y head exactos;
- diff y referencias internas;
- ausencia de rutas o includes inexistentes;
- coherencia entre roadmap, matriz de Iris y documentación;
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
- link o harness OpenGL cuando exista.

### Tooling, scripts y workflows

- tests unitarios;
- integración de CLI;
- fixtures;
- validación YAML/JSON/schema;
- permisos mínimos y timeouts;
- acciones fijadas cuando la política del repositorio lo requiera;
- simulación del coordinador sin mutar el issue real, salvo smoke test controlado.

### Packaging y release

- contenido y raíz del ZIP;
- exclusiones;
- reproducibilidad;
- versión y changelog;
- checksums;
- licencia y atribuciones;
- instalación y rollback documentados.

### Iris y visual

Cuando el entorno lo permita:

- carga y recarga en Iris;
- compilación dentro del cliente;
- logs y errores OpenGL;
- capturas comparativas;
- escenas deterministas;
- perfiles y dimensiones;
- resize, teletransporte y discontinuidades;
- métricas de rendimiento y regresión.

La imposibilidad de ejecutar Minecraft no elimina las validaciones estáticas, de tooling, empaquetado, OpenGL o CI disponibles.

## Pruebas no ejecutables

Cuando una prueba requerida no pueda ejecutarse:

1. no inventes el resultado;
2. registrá el nombre exacto;
3. explicá la limitación;
4. indicá comando, entorno o procedimiento para ejecutarla;
5. enlazá el ítem afectado;
6. dejalo `REVALIDAR` si la prueba es necesaria para aceptación;
7. no declares `PASS`.

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
- documentación y roadmap de la PR son coherentes para el estado previo al merge.

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

### `PARTIAL`

Existe avance remoto útil, pero falta merge, prueba, CI, reconciliación final o aceptación completa.

### `BLOCKED`

Existe una restricción externa real sin alternativa autorizada, o el coordinador/permiso indispensable impide operar.

### `NO-OP`

No se realizó trabajo funcional porque otra lease estaba activa, no existía unidad válida o el estado remoto ya satisfacía el objetivo.

No uses `PASS` para una PR abierta, trabajo solo local, pruebas faltantes, CI desconocida, roadmap sin reconciliar o lock sin liberar.
