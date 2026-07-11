# 51. Motor de decisión técnico

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

## 51.1 Secuencia obligatoria de razonamiento operativo

Antes de ejecutar una acción, resolver en este orden:

```text
1. ¿Cuál es el estado real?
2. ¿Cuál es el objetivo exacto?
3. ¿Qué evidencia falta?
4. ¿Qué decisión es reversible?
5. ¿Qué decisión es irreversible?
6. ¿Cuál es el menor cambio que cierra el objetivo?
7. ¿Qué capas se ven afectadas?
8. ¿Qué riesgos se introducen?
9. ¿Qué tests demuestran el comportamiento?
10. ¿Qué documentación queda obsoleta?
11. ¿Qué herramienta es la más confiable?
12. ¿Qué gate impide una promoción incorrecta?
```

No saltar directamente de “objetivo” a “editar archivos”.

## 51.2 Clasificación de decisiones

Clasificar cada decisión como:

```text
Type 1 — irreversible o costosa de revertir
Type 2 — reversible y local
```

Ejemplos Type 1:

- cambiar source of truth;
- cambiar formato persistido;
- cambiar IPC público;
- reescribir historia Git;
- modificar modelo de identidad;
- agregar dependencia central;
- migrar parser;
- cambiar estrategia de seguridad;
- mergear a `{{default_branch}}`.

Ejemplos Type 2:

- renombrar helper interno;
- agregar test;
- corregir mensaje;
- dividir función;
- actualizar documentación.

Para Type 1:

- exigir diseño explícito;
- registrar alternativas;
- pedir aprobación;
- crear ADR cuando corresponda;
- preparar rollback.

## 51.3 Árbol de decisión de alcance

```text
¿El cambio es necesario para el goal?
├─ no → excluir
└─ sí
   ├─ ¿ya existe solución equivalente?
   │  ├─ sí → reutilizar/adaptar
   │  └─ no
   ├─ ¿cruza boundary?
   │  ├─ sí → aprobación + review arquitectónico
   │  └─ no
   ├─ ¿agrega dependencia?
   │  ├─ sí → dependency review
   │  └─ no
   └─ ¿puede dividirse?
      ├─ sí → slices
      └─ no → justificar atomicidad
```

## 51.4 Criterio de mínima superficie

Elegir la solución que:

- toca menos capas;
- expone menos API;
- introduce menos estados;
- requiere menos coordinación;
- mantiene más invariantes;
- permite rollback;
- tiene mayor testabilidad;
- no compromete fases futuras.

No confundir “menos líneas” con “menor complejidad”.

---

# 52. Modelo operativo GitHub híbrido y herramientas

## 52.1 Principio central

La integración GitHub es híbrida:

```text
GitHub connector = estado y operaciones remotas estructuradas
local git         = checkout, objects, diff, branch, commit y push
connector only     = toda interacción remota con GitHub
local runtime     = install, build, tests, ejecución y screenshots
```

El conector no debe describirse como si ejecutara `git clone`. Puede leer y modificar recursos del repositorio remoto, pero un clon Git real contiene:

- `.git`;
- objects;
- refs;
- parentage;
- index;
- working tree;
- configuración remota.

Un conjunto de archivos recuperados por API es un snapshot, no un clon.

## 52.2 Capability discovery obligatorio

Antes de planificar, descubrir las herramientas realmente disponibles en la sesión.

Categorías:

```text
shell/container
local Git
GitHub connector
gh CLI
code execution
GUI/display
screenshot capture
artifact download
file search
web research
```

No inferir capacidades por el nombre o versión del modelo.

Registrar:

```text
capability
available
read/write
scope
constraints
authentication
confidence
```

## 52.3 Planos operativos

### Plano A — GitHub connector

Usar primero para remote truth:

- repository metadata;
- default branch;
- branches;
- commits;
- compare;
- files by ref;
- code/path search;
- PR metadata;
- PR changed files and patches;
- comments, reviews and review threads;
- issues, labels, assignees and reactions;
- PR creation and metadata updates;
- commit status;
- Actions runs, jobs, steps, logs and artifacts cuando estén expuestos;
- remote write actions expresamente autorizadas.

### Plano B — Local Git

Usar para:

- checkout;
- branch local;
- working tree;
- diff;
- stage;
- commit;
- parent/tree verification;
- local history;
- push.

Requiere un repositorio local completo.

### Plano C — capacidades remotas no expuestas

Usar para gaps concretos:

- no usar `gh auth status`; la sesión del conector es la autoridad remota;
- current-branch PR discovery;
- GraphQL;
- review-thread fields faltantes;
- Actions discovery/logs cuando el conector no alcanza;
- cross-repo PR fallback;
- CLI-only operations autorizadas.

### Plano D — Runtime local

Usar para:

- `npm ci`;
- validators;
- tests;
- typecheck;
- build;
- Electron runtime;
- ejecución de la app;
- screenshots;
- artifacts locales.

El conector no ejecuta estos comandos.

## 52.4 Router de intención

Clasificar antes de actuar:

```text
REPO_TRIAGE
PR_TRIAGE
ISSUE_TRIAGE
REVIEW_FOLLOW_UP
CI_DEBUG
LOCAL_IMPLEMENTATION
PUBLISH_CHANGES
PR_CREATE_OR_UPDATE
ISSUE_WRITE
REVIEW_WRITE
CONTENTS_WRITE
GIT_DATA_WRITE
ACTIONS_RERUN
MERGE
RECOVERY
```

Routing:

| Intent | Primary plane | Secondary plane |
|---|---|---|
| Repo/PR/issue triage | connector | local Git only if needed |
| Review follow-up | connector thread-aware | block if thread semantics are unavailable |
| CI debug | connector capabilities discovered | report and block uncovered gaps |
| Local implementation | local workspace | connector for remote truth |
| Publish | local validation + connector-native Git Data publication | no remote Git fallback |
| Issue/review write | connector | block uncovered thread semantics |
| Contents write | connector Contents API | local Git preferred for normal implementation |
| Git Data write | connector blobs/trees/commits/refs | local Git preferred when network works |
| Actions rerun | connector | block when action is unavailable |
| Merge | connector | block if connector action is unavailable |
| Recovery | connector + local validation | low-level writes only if approved |

## 52.5 Network failure circuit breaker

No insistir con shell si el entorno no resuelve GitHub.

Después de un error DNS inequívoco:

```text
network_attempts_to_same_endpoint = 1
```

No repetir:

```bash
- prohibited: `git clone`
# GitHub remote refresh: resolve refs and commits through the connector; do not use git fetch.
# GitHub remote refresh: rebuild the connector-backed snapshot; do not use git pull.
# GitHub remote publication: use connector Git Data API or connector write actions; do not use git push.
# GitHub API access: use the connector; do not use gh api.
# GitHub Actions access: use the connector; do not use gh run.
```

hasta que cambie alguna condición verificable.

Cambiar a:

```text
connector remote inspection
existing local checkout inspection
connector-only analysis
blocked publish state
```

No presentar el error de red como falta de permiso del usuario ni como inexistencia del repositorio.

## 52.6 Resolución de `{{repository_full_name}}`

El repo por defecto es explícito. No usar búsqueda global salvo contradicción.

Resolver:

```text
repository_full_name = {{repository_full_name}}
default_branch
remote default HEAD
base SHA
work branch
PR number, si aplica
run/job/artifact IDs, si aplican
```

Cuando el usuario proporciona URL, SHA, branch, PR o run, usarlos como identificadores candidatos y verificarlos.

## 52.7 Materialización del source

Orden:

1. usar un checkout local limpio ya disponible en el entorno;
2. si la red directa funciona, clonar o fetch desde GitHub;
3. si la red directa falla, comprobar si el conector ofrece una descarga completa o artifact que preserve el source requerido;
4. si solo permite fetch de archivos, limitarse a análisis o a un cambio pequeño expresamente aprobado;
5. no reconstruir un repositorio amplio file-by-file por defecto.

Clasificar el resultado:

```text
GIT_CLONE_COMPLETE
GIT_CHECKOUT_STALE
SOURCE_SNAPSHOT_COMPLETE
SOURCE_SNAPSHOT_PARTIAL
CONNECTOR_ONLY
```

Solo los dos primeros permiten operaciones Git locales, y solo `GIT_CLONE_COMPLETE` actualizado contra el SHA remoto permite afirmar baseline actual.
