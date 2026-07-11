# 9. Investigación inicial y resolución del repositorio

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

## 9.1 Resolver el estado remoto con el conector

El primer contacto con GitHub debe hacerse mediante las capacidades del conector disponibles en la sesión.

Para `{{repository_full_name}}`, resolver como mínimo:

```text
repository_full_name: {{repository_full_name}}
default branch
repository visibility
remote default HEAD
relevant branches
recent commits
open PRs
relevant workflow/check state
```

Usar refs y SHAs exactos. No asumir que `main`, una branch o un run conservan el estado narrado por otro chat.

El conector debe emplearse para:

- identificar el repositorio;
- obtener metadata de la default branch;
- buscar branches y commits;
- recuperar commits exactos;
- comparar refs;
- leer archivos por path y ref;
- buscar símbolos y paths;
- inspeccionar PRs, diffs y patches;
- consultar checks, runs, jobs, steps, logs o artifacts cuando esas funciones estén disponibles en la sesión;
- resolver runs por SHA y PR sin pedir al usuario una URL cuando la identidad pueda descubrirse mediante el conector.

## 9.2 Determinar si existe un workspace local usable

Antes de ejecutar Git local, clasificar el estado:

```text
LOCAL_GIT_CHECKOUT
LOCAL_SOURCE_SNAPSHOT
CONNECTOR_ONLY
NO_REPOSITORY_CONTEXT
```

### `LOCAL_GIT_CHECKOUT`

Existe `.git`, el tree es verificable y pueden ejecutarse:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git rev-parse HEAD^{tree}
```

### `LOCAL_SOURCE_SNAPSHOT`

Existe el source completo pero no la historia Git. Puede servir para instalar, buildar, ejecutar tests o abrir la aplicación, pero no para:

- demostrar parentage;
- crear un commit Git confiable;
- comparar con `origin/{{default_branch}}` mediante Git;
- hacer push.

### `CONNECTOR_ONLY`

Solo existe acceso remoto estructurado. Permite análisis, auditoría y operaciones remotas explícitamente soportadas, pero no permite afirmar que se ejecutaron tests locales.

### `NO_REPOSITORY_CONTEXT`

No existe repo identificable ni checkout. Detener y solicitar el identificador que falta.

## 9.3 Preflight de red y autenticación

Solo cuando una operación requiere red directa desde shell:

```bash
git --version
# No GitHub CLI network path: use the connector session.
# GitHub authentication and access are resolved through the connector; do not use gh.
# GitHub ref resolution: use the connector; do not use git ls-remote.
```

No ejecutar este preflight si la tarea es connector-only y no necesita Git local.

Clasificar los fallos:

```text
DNS_UNAVAILABLE
NETWORK_BLOCKED
GH_MISSING
GH_UNAUTHENTICATED
REPOSITORY_DENIED
REMOTE_NOT_FOUND
RATE_LIMITED
UNKNOWN_NETWORK_FAILURE
```

Si aparece:

```text
Could not resolve host: github.com
Could not resolve hostname github.com
Temporary failure in name resolution
```

hacer lo siguiente:

1. registrar el error una vez;
2. no repetir `clone`, `fetch`, `pull` o `push` de forma ciega;
3. mantener el análisis remoto mediante el conector;
4. determinar si ya existe un checkout o snapshot completo;
5. limitar cualquier afirmación de validación al material realmente disponible.

## 9.4 Sincronización remota mediante conector

El estado remoto se actualiza exclusivamente mediante el conector:

```text
resolve repository metadata
→ resolve default branch and exact SHA
→ compare refs/commits
→ refresh connector-backed source snapshot when required
```

Git local puede inspeccionar el workspace materializado, pero no debe contactar el remote. Antes de reconstruir el snapshot verificar:

- branch local de trabajo;
- working tree;
- remote default branch resuelta por conector;
- divergencia entre el baseline local y el SHA remoto;
- SHA esperado;
- patches locales que deban reaplicarse.

No ejecutar `git pull`, `git fetch` ni otro transporte GitHub local.

## 9.5 Buscar implementación equivalente

Con checkout local:

```bash
git grep -n "<contract>"
git grep -n "<error>"
git grep -n "<feature>"
```

Sin checkout local, usar búsqueda del conector acotada a `{{repository_full_name}}`, y recuperar los archivos exactos por ref antes de sacar conclusiones.

No implementar duplicados.

## 9.6 Reconstruir el flujo real

Documentar:

```text
input
→ owner
→ transformation
→ state
→ IPC
→ UI
→ validator
```

Identificar:

- dónde se pierde provenance;
- dónde se duplica lógica;
- dónde hay estado stale;
- dónde hay race;
- dónde existe un contrato implícito;
- dónde existe responsabilidad incorrecta.

---

# 10. Diagnóstico senior

Clasificar cada subsistema:

```text
Implemented
Partial
Foundation
Read-only
Preview-only
Planning-only
Blocked
Missing
Conflict
Deprecated
Unsafe
Unverified
```

Cada diagnóstico debe incluir:

```text
evidence
impact
risk
recommended action
```

Ejemplo:

| Subsystem | Status | Evidence | Risk | Action |
|---|---|---|---|---|
| Source revision | Missing | no digest field | stale patch | add SHA-256 provenance |

---

# 11. Diseño del plan

El plan debe contener:

1. Estado remoto verificado.
2. Diagnóstico.
3. Flujo actual.
4. Objetivo.
5. No alcance.
6. Arquitectura propuesta.
7. Contratos.
8. Algoritmos.
9. Files plan.
10. Tests.
11. Validators.
12. Docs.
13. Metadata.
14. Security.
15. Performance.
16. Risks.
17. Validation plan.
18. Git plan.
19. Approval question.

## 11.1 File plan

Tabla obligatoria:

| Path | Action | Responsibility | Dependency | Risk | Approval |
|---|---|---|---|---|---|

No usar “aproximadamente”.

## 11.2 Workstreams

Tabla:

| Workstream | Role | Inputs | Outputs | Blockers | Gate |
|---|---|---|---|---|---|

Ejemplo:

| Core contracts | Staff Engineer | current types | new types | naming | typecheck |
| Main service | Senior Dev | contracts | runtime service | path safety | unit tests |
| Docs | Documentation Owner | final behavior | architecture docs | implementation stable | docs validators |

---

# 12. Arquitectura condicional del repositorio objetivo

> Aplicación condicional: las capas Core/Main/Preload/Renderer siguientes solo son normativas cuando el repositorio usa Electron o una separación equivalente. Para otros stacks, mapear las responsabilidades a las capas reales detectadas y no inventar Electron, Node, IPC ni renderer.

## 12.1 Ownership por capa

### Core

Debe contener:

- tipos;
- contratos;
- funciones puras;
- validadores puros;
- planners;
- selectors;
- state models;
- deterministic algorithms.

No debe:

- acceder a filesystem;
- importar Electron;
- mutar UI;
- escribir archivos;
- usar APIs del navegador.

### Main

Debe contener:

- filesystem;
- path resolution;
- process execution;
- security checks;
- Electron main services;
- trusted state;
- IPC handlers;
- cache runtime;
- side effects.

### Preload

Debe:

- exponer API mínima;
- tipar requests/responses;
- no filtrar APIs generales;
- no exponer Node;
- no exponer paths absolutos.

### Renderer

Debe:

- renderizar UI;
- emitir requests limitadas;
- mantener state visual;
- descartar respuestas stale;
- no acceder a filesystem;
- no importar `node:*`;
- no confiar en datos no validados.

### Docs

Debe describir:

- estado real;
- boundaries;
- flow;
- ownership;
- next phase.

### Validators

Deben demostrar:

- comportamiento;
- wiring;
- invariants;
- prohibiciones.

---

# 13. Seguridad

Revisar:

- path traversal;
- root containment;
- symlinks;
- absolute path leaks;
- untrusted postMessage;
- IPC payload validation;
- preload surface;
- context isolation;
- sandbox;
- Node integration;
- shell execution;
- child process;
- environment secrets;
- workflow permissions;
- checkout credentials;
- artifacts;
- logs;
- source text exposure.

Reglas:

```text
shell: false
argument arrays
no eval
no dynamic require from user input
no renderer fs
no raw Buffer to renderer
no source text leak
no absolute path leak
```

---

# 14. Dependencias

Por defecto:

```text
No agregar dependencias.
```

Si se propone una:

- explicar necesidad;
- evaluar standard library;
- evaluar dependencia existente;
- evaluar tamaño;
- evaluar licencia;
- evaluar seguridad;
- evaluar mantenimiento;
- evaluar lockfile;
- pedir aprobación.

Nunca usar:

```bash
npm audit fix
npm audit fix --force
```

---
