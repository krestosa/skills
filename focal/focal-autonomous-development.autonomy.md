# Focal — Política vinculante de autonomía y bootstrap

Este archivo complementa la especificación técnica completa y las correcciones operativas anteriores de Focal.

Su objetivo es impedir que una ejecución se detenga y requiera intervención del usuario únicamente porque falta una pieza interna que el propio agente está autorizado a crear dentro de `krestosa/Focal`.

# Corrección 12 — Crear autónomamente toda infraestructura interna faltante

## Principio rector

La ausencia de una herramienta, archivo, workflow, configuración, directorio, fixture, schema, test, validador, harness, documento, lockfile, script, supervisor o cualquier otra pieza interna requerida por el proyecto no constituye por sí sola un bloqueo externo.

Cuando una ejecución detecte que necesita una pieza interna que todavía no existe, debe tratar esa ausencia como trabajo de bootstrap prioritario y crearla autónomamente dentro de `krestosa/Focal`.

No debe limitarse a informar:

- que falta CI;
- que falta un runtime guard;
- que falta un validador;
- que falta una estructura de proyecto;
- que falta una configuración;
- que falta un workflow;
- que falta un test;
- que falta un harness;
- que falta documentación;
- que falta un lockfile;
- que falta una rama;
- que falta un archivo de estado;
- que falta una herramienta de empaquetado;
- que falta una capacidad que puede implementarse en el repositorio.

Debe crear la mínima implementación segura, verificable y extensible que elimine esa carencia y continuar desde allí.

## Clasificación obligatoria de ausencias

Toda dependencia faltante debe clasificarse como uno de estos estados:

```text
INTERNAL_BOOTSTRAP_REQUIRED
INTERNAL_CAPABILITY_IMPLEMENTABLE
EXTERNAL_CAPABILITY_AVAILABLE_BY_ALTERNATIVE
EXTERNAL_IRREVERSIBLE_BLOCKER
```

### `INTERNAL_BOOTSTRAP_REQUIRED`

La pieza pertenece al propio repositorio y puede crearse mediante archivos, scripts, workflows, tests, documentación o configuración.

Resultado obligatorio: crearla. No finalizar como `BLOCKED`.

### `INTERNAL_CAPABILITY_IMPLEMENTABLE`

La operación no está disponible directamente, pero puede implementarse con código propio, herramientas estándar, GitHub Actions, Git Data API, scripts locales, fixtures o una ruta equivalente autorizada.

Resultado obligatorio: implementar la capacidad mínima o crear el mecanismo que la suministre. No pedir intervención ordinaria.

### `EXTERNAL_CAPABILITY_AVAILABLE_BY_ALTERNATIVE`

La herramienta preferida no está disponible, pero existe otra ruta autorizada, por ejemplo:

- otra operación del conector de GitHub;
- Git Data API en lugar de Contents API;
- un workflow de GitHub Actions;
- Python estándar;
- una herramienta local ya instalada;
- una implementación propia pequeña;
- validación estática local;
- fixtures offline;
- un artefacto reproducible creado por CI.

Resultado obligatorio: utilizar o crear la alternativa.

### `EXTERNAL_IRREVERSIBLE_BLOCKER`

Solo corresponde cuando ninguna ruta autorizada puede resolver el requisito y existe una restricción externa real, como:

- credenciales indispensables ausentes;
- permisos remotos insuficientes;
- autorización requerida fuera de `krestosa/Focal`;
- servicio externo obligatorio completamente inaccesible y sin alternativa;
- restricción legal o de seguridad;
- capacidad de plataforma inexistente que no puede implementarse ni sustituirse;
- imposibilidad material de preservar el trabajo antes del hard stop.

Solo esta categoría permite solicitar intervención del usuario o finalizar como `BLOCKED` por la ausencia de una capacidad.

La carga de trabajo, la complejidad, la inexistencia de archivos internos, la falta de CI, la ausencia de checks, la falta de un script o la necesidad de escribir más código no son bloqueos externos.

## Escalera autónoma de resolución

Ante una necesidad faltante, aplicá en este orden:

1. Buscá si ya existe localmente o en una rama, PR o checkpoint remoto.
2. Si existe trabajo parcial, retomalo y completalo.
3. Si no existe, creá la pieza mínima directamente en la rama de trabajo actual cuando pertenezca a la misma unidad.
4. Si es una capacidad transversal, creá o retomá una rama de bootstrap coherente.
5. Implementá primero una versión mínima segura y comprobable.
6. Añadí tests o validación específica para esa versión.
7. Publicá un checkpoint remoto temprano.
8. Ejecutá la nueva capacidad.
9. Continuá la tarea original si queda presupuesto temporal suficiente.
10. Si no queda tiempo, dejá la rama y PR listas para que el siguiente ciclo continúe automáticamente.

No abras múltiples PRs redundantes para la misma carencia. Antes de crear una rama nueva, inspeccioná ramas y PRs abiertas y continuá la unidad existente cuando sea compatible.

## Prohibición de diagnóstico pasivo

Una ejecución no debe consumir el ciclo únicamente en descubrir y describir una carencia interna.

Cuando exista tiempo y autorización suficientes, debe producir al menos uno de estos resultados remotos:

- archivo habilitante creado;
- workflow creado;
- script creado;
- test creado;
- fixture creado;
- schema creado;
- configuración creada;
- rama de bootstrap publicada;
- PR existente actualizada;
- checkpoint funcional publicado.

El informe terminal debe describir lo creado, no solo lo que falta.

## Bootstrap de CI cuando no existen checks

La ausencia de checks o workflows de CI debe activar inmediatamente `INTERNAL_BOOTSTRAP_REQUIRED`.

La ejecución debe:

1. Inspeccionar la PR y rama actuales.
2. Continuar la PR de bootstrap existente si ya contiene la fundación del repositorio.
3. Crear un workflow mínimo en `.github/workflows/`.
4. Configurarlo para ejecutarse al menos en `pull_request`, `push` a `main` y, cuando sea útil, `workflow_dispatch`.
5. Declarar permisos mínimos.
6. Declarar el grupo de concurrencia exigido cuando el workflow pueda mutar.
7. Declarar `timeout-minutes`.
8. Fijar Actions de terceros por SHA completo.
9. Validar sintaxis YAML y estructura del workflow.
10. Añadir checks proporcionales al estado actual del repositorio.
11. Publicar el commit del workflow.
12. Verificar si se genera un run o check para el nuevo head.
13. Corregir el workflow si falla.
14. Continuar hasta obtener evidencia verde o alcanzar el límite temporal.

La CI inicial debe crecer por etapas. En un repositorio todavía mínimo puede comenzar con:

- validación de estructura;
- validación de JSON y schemas;
- validación de archivos Markdown y texto;
- detección de secretos y binarios inesperados;
- política de una ruta por commit;
- pruebas disponibles del lock y runtime guard;
- comprobación de empaquetado cuando exista;
- comprobación de referencias prohibidas.

No exijas que existan shaders, compiladores o harnesses todavía inexistentes para permitir el primer workflow. Añadí esos checks a medida que las capacidades sean implementadas.

## Excepción controlada para el bootstrap inicial de CI

No puede exigirse un check de CI preexistente para fusionar la primera implementación de la propia CI cuando ningún workflow anterior podía producir checks.

Para resolver este problema circular, se permite `BOOTSTRAP_VALIDATION` únicamente para una PR cuyo propósito sea crear o reparar la infraestructura mínima de CI.

Antes de usar esta excepción, deben cumplirse todos estos gates:

- el cambio está en una rama y PR, nunca mediante push directo a `main`;
- el head exacto fue verificado;
- cada commit respeta la política de una ruta;
- el workflow fue parseado como YAML;
- los eventos están explícitamente definidos;
- los permisos son mínimos;
- no utiliza secretos no declarados;
- no ejecuta comandos remotos inseguros;
- las Actions están fijadas por SHA completo;
- existe timeout;
- el workflow no concede permisos de escritura salvo necesidad demostrada;
- la lógica ejecutada fue validada localmente o mediante una simulación equivalente;
- el diff fue revisado completamente;
- no existe otra ejecución propietaria activa.

Cuando la plataforma permita que el workflow de la PR se ejecute antes del merge, debe esperarse y exigirse su resultado verde.

Solo cuando la plataforma no genere ningún check porque la propia CI todavía no existe o no puede activarse antes del merge, puede fusionarse la PR de bootstrap usando `BOOTSTRAP_VALIDATION`.

Después del merge:

1. verificá el SHA de `main`;
2. comprobá que el workflow exista en `main`;
3. ejecutá o esperá el primer run disponible;
4. inspeccioná el resultado;
5. si falla, creá inmediatamente una rama correctiva o dejá un checkpoint remoto si el tiempo no alcanza;
6. no declares release candidate hasta que la CI real esté verde.

Esta excepción no se aplica a features gráficas, shaders, optimizaciones, releases ni cambios ordinarios una vez que la CI ya funciona.

## Runtime guard y supervisor faltantes

La ausencia de `tools/runtime_guard.py` en el repositorio no debe provocar un bloqueo si la VM permite ejecutar Python, `timeout`, señales o un mecanismo equivalente.

La ejecución debe:

1. crear un supervisor efímero antes de adquirir el lock;
2. activar el reloj monotónico, soft stop y hard stop;
3. utilizar ese supervisor durante el ciclo actual;
4. convertir la implementación persistente de `tools/runtime_guard.py` y sus tests en prioridad de bootstrap;
5. publicar el runtime guard en GitHub;
6. usar la versión persistente en ciclos posteriores.

Solo puede utilizarse `BLOCKED — RUNTIME_GUARD_UNAVAILABLE` si la plataforma realmente impide ejecutar cualquier supervisor, reloj monotónico y mecanismo de terminación, no simplemente porque el archivo todavía no fue creado.

El informe nunca debe indicar simultáneamente que el supervisor estaba inactivo y que se realizaron mutaciones funcionales, salvo que documente una falla inesperada ocurrida después de una activación verificada y haya detenido inmediatamente nuevas mutaciones.

## Herramientas y dependencias faltantes

Si falta una herramienta necesaria:

1. comprobá si existe una alternativa instalada;
2. preferí biblioteca estándar o implementación propia pequeña;
3. si corresponde, añadí una dependencia bloqueada y verificable;
4. si la VM no tiene red, trasladá la resolución online a GitHub Actions;
5. creá fixtures o snapshots para el modo offline;
6. no uses la falta de una herramienta preferida como excusa para no implementar la capacidad.

No descargues ni ejecutes software no confiable. La autonomía no elimina los requisitos de procedencia, seguridad ni reproducibilidad.

## Continuidad automática entre ciclos

Cuando una unidad no pueda completarse dentro del ciclo:

- publicá todos los cambios recuperables;
- actualizá la PR existente;
- registrá rama, PR, head SHA y siguiente acción concreta;
- marcá `INCOMPLETE`, no `BLOCKED`, salvo bloqueo externo real;
- liberá el lock;
- el siguiente ciclo debe retomar automáticamente esa rama o PR antes de comenzar una unidad nueva.

Una PR draft con trabajo válido pendiente no es un callejón sin salida. Es un checkpoint de continuidad.

## Política de estado

Usá los resultados así:

### `PASS`

La unidad y sus gates quedaron completos.

### `INCOMPLETE`

Existe trabajo válido publicado y el siguiente ciclo puede continuarlo sin intervención del usuario.

### `FAIL`

La implementación o validación falló de forma concreta, pero la causa y el estado fueron preservados para corrección automática posterior.

### `BLOCKED`

Existe una restricción externa real que no puede resolverse mediante código, configuración, workflow, herramienta alternativa, checkpoint o permiso ya concedido dentro de `krestosa/Focal`.

No uses `BLOCKED` para una carencia interna implementable.

## Prioridad frente a trabajo nuevo

El orden de prioridad debe ser:

1. recuperar trabajo local legítimo;
2. resolver un lock o estado operativo inconsistente;
3. continuar una PR o rama incompleta existente;
4. crear infraestructura interna faltante que bloquea validación o continuidad;
5. corregir CI y herramientas de bootstrap;
6. corregir defectos críticos;
7. implementar la siguiente unidad del roadmap;
8. optimizar.

En el estado actual de Focal, si la PR de fundación sigue abierta y no existe CI, la siguiente ejecución debe continuar esa PR o una rama compatible y crear la CI mínima antes de iniciar `tools/runtime_guard.py` u otra feature independiente. Después debe crear y validar el runtime guard.

## Informe terminal ampliado

Añadí:

```text
Carencias internas detectadas:
Clasificación de cada carencia:
Infraestructura creada en este ciclo:
Alternativas autónomas utilizadas:
Bootstrap validation utilizada: sí | no
Motivo de bootstrap validation:
PR o rama incompleta retomada:
Checkpoint habilitante publicado:
Bloqueo externo real encontrado:
Intervención del usuario requerida: sí | no
Justificación estricta de intervención:
```

Si `Intervención del usuario requerida` es `sí`, la justificación debe demostrar que se agotaron las alternativas autorizadas y que el impedimento pertenece a `EXTERNAL_IRREVERSIBLE_BLOCKER`.

# Regla de precedencia de esta política

Esta política reemplaza cualquier instrucción anterior que ordene detenerse únicamente porque no existe CI, no existen checks, falta un archivo interno, falta un workflow, falta un validador, falta un runtime guard persistente o todavía no fue creada una capacidad implementable.

No reemplaza:

- límites de autorización;
- seguridad;
- hard killswitch;
- propiedad del lock;
- prohibición de force push;
- prohibición de secretos;
- requisitos de procedencia;
- límites externos reales.

Razonamiento: High