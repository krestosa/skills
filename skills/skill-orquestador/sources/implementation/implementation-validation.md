# 15. Baseline local verificable

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

Después de aprobación, la baseline requiere un workspace local completo.

## 15.1 Gate de materialización

Antes de instalar o validar, registrar:

```text
workspace mode
source origin
repository
ref requested
commit SHA
local HEAD, si existe
local tree, si existe
connector-verified commit
completeness status
```

La baseline queda bloqueada si solo existen snippets, patches parciales o archivos aislados.

## 15.2 Sincronización Git, solo cuando la red directa funciona

```bash
# GitHub remote refresh: resolve refs and commits through the connector; do not use git fetch.
git switch {{default_branch}}
# GitHub remote refresh: rebuild the connector-backed snapshot; do not use git pull.
git status --short
git rev-parse HEAD
git rev-parse HEAD^{tree}
git log --oneline -20
```

Antes de `pull`, verificar que el working tree esté limpio y que `main` no tenga commits locales no publicados.

Si la red directa no funciona:

- no repetir el comando;
- verificar el SHA remoto mediante el conector;
- usar un checkout ya materializado solo si contiene ese SHA exacto;
- si el SHA remoto no está disponible localmente, declarar la baseline local como stale o bloqueada;
- no simular sincronización mediante edición manual de archivos.

## 15.3 Baseline de dependencias y validación

```bash
npm ci --foreground-scripts
npm run doctor:electron
npm run validate:project-metadata
npm run validate:validation-system
npm run validate:local:quick
npm --silent run validate:local:quick:json
```

Registrar:

```text
command
exit code
summary
duration
workspace mode
validated SHA
environment caveat
```

## 15.4 Gate de build, ejecución y screenshot

No inferir capacidades por la versión del modelo. Probarlas en el runtime actual.

Separar:

```text
SOURCE_AVAILABLE
DEPENDENCIES_INSTALLED
BUILD_PASSED
APP_LAUNCHED
UI_RENDERED
SCREENSHOT_CAPTURED
```

Un build exitoso no demuestra que Electron abrió. Un proceso iniciado no demuestra que la UI renderizó. Una captura solo es válida si puede asociarse al SHA y al comando ejecutado.

Antes de ejecutar la aplicación, comprobar:

- runtime de Electron instalado;
- display server o modo headless/offscreen disponible;
- variables de entorno necesarias;
- puertos y procesos hijos;
- timeout;
- mecanismo de cierre;
- mecanismo real de captura.

Para cada screenshot registrar:

```text
validated SHA
launch command
capture mechanism
window or route captured
runtime mode
timestamp
known visual limitations
```

Si no existe superficie gráfica o herramienta de captura, reportar:

```text
build validated
application launch not visually verified
screenshot unavailable in current runtime
```

## 15.5 Fallo de baseline

Si baseline falla:

- detener;
- diagnosticar;
- separar fallo del repositorio, del entorno y de conectividad;
- no mezclar la reparación con el objetivo aprobado;
- pedir decisión cuando el fallo exige ampliar alcance.

---

# 16. Creación de branch

Solo después del baseline:

```bash
git switch -c <branch>
```

Verificar:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
```

No crear branches auxiliares.

---

# 17. Implementación por slices

No implementar todo de una vez.

Usar slices:

```text
Slice 1 — types
Slice 2 — core behavior
Slice 3 — main integration
Slice 4 — preload/IPC
Slice 5 — renderer
Slice 6 — tests
Slice 7 — validators
Slice 8 — docs
Slice 9 — metadata
Slice 10 — final gate
```

Cada slice debe tener:

```text
inputs
changed files
expected behavior
tests
completion criteria
```

---

# 18. Estándar de código

Exigir:

- nombres explícitos;
- funciones pequeñas;
- single responsibility;
- inmutabilidad cuando sea razonable;
- errores accionables;
- reason codes estructurados;
- no lógica por substring;
- no magic values;
- no timestamps como identidad;
- no IDs aleatorios cuando se requiere determinismo;
- no duplicación de contratos;
- no silent fallback;
- no catch vacío;
- no `any` sin justificación;
- no assertions inseguras;
- no comentarios que reemplacen diseño.

---

# 19. Tests

## 19.1 Tipos de test

- unit;
- behavior;
- integration;
- regression;
- security;
- negative;
- boundary;
- race;
- idempotence;
- serialization;
- documentation;
- workflow.

## 19.2 Matriz

Cada feature debe considerar:

```text
happy path
missing input
invalid input
boundary
stale state
concurrency
large input
security
compatibility
idempotence
cleanup
```

## 19.3 Calidad

No aceptar:

- test que solo busca un token;
- test que replica implementación;
- test sin assertion significativa;
- fixture trivial;
- test que depende del reloj;
- test que depende de red sin necesidad;
- test que pasa con implementación incorrecta.

---

# 20. Validators

Un validator serio debe combinar:

- imports reales;
- ejecución;
- fixtures;
- structural checks;
- wiring;
- security scans;
- forbidden behavior.

Debe fallar si:

- falta contrato;
- falta wiring;
- se usa API prohibida;
- se habilita comportamiento fuera de scope;
- docs no registran la fase;
- metadata no es idempotente;
- scripts no coinciden.

No debe exigir:

- nombre de branch temporal;
- commit SHA fijo;
- run ID;
- token dummy;
- artefacto operativo.

---

# 21. Validación incremental

Después de cada slice:

```bash
npm run typecheck
npm run <validator-específico>
```

Después de contratos:

```text
types → consumers → fixtures → validators
```

Después de IPC:

```text
shared types → main handler → preload → renderer → security validator
```

Después de docs:

```text
markdown → guided docs → architecture docs → metadata
```

---

# 22. Gate final

Ejecutar según alcance:

```bash
npm ci --foreground-scripts
npm run doctor:electron

npm run validate:project-metadata
npm --silent run validate:project-metadata:json

npm run validate:change-policy
npm run validate:validation-system
npm run validate:markdown-integrity
npm run validate:guided-docs
npm run validate:architecture-docs

npm run validate:structure
npm run validate:project-graph
npm run validate:project-watch

npm run validate:preview
npm run validate:dom-snapshot
npm run validate:preview-selection
npm run validate:preview-inspector

npm run validate:design-canvas
npm run validate:visual-selection-overlay
npm run validate:html-element-library
npm run validate:source-patch-preview
npm run validate:editable-inspector-surface
npm run validate:css-sass-inspector-surface
npm run validate:ui-flow

npm run validate:history-foundation
npm run validate:design-editing-preflight
npm run validate:inspector-editing-foundation
npm run validate:style-engine-foundation
npm run validate:authored-style-matching

npm run test:tooling-hardening

npm run validate:local:quick
npm --silent run validate:local:quick:json

npm run build
npm run typecheck
npm audit

git diff --check
git status --short
```

Agregar validators específicos.

---

# 23. JSON puro

Cuando un script debe producir JSON puro:

```bash
npm --silent run <script>
```

Verificar:

```bash
<command> | jq .
```

o parse equivalente.

No afirmar JSON puro si npm imprime banners.

---

# 24. Metadata

Identificar:

- canonical source;
- generated consumers;
- markers;
- ownership.

Procedimiento:

```bash
npm run sync:project-metadata
git add <approved files>
npm run sync:project-metadata
git diff --exit-code
npm run sync:project-metadata
git diff --exit-code
git diff --cached --check
```

No editar output generado como fuente primaria.

---

# 25. Build idempotence

Con cambios staged:

```bash
npm run build
git diff --exit-code
npm run build
git diff --exit-code
```

No aceptar drift.

---
