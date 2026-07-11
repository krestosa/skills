# 53. Bootstrapping industrial del workspace

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

## 53.1 Workspace aislado

Crear un workspace único por tarea:

```text
/workspaces/<repo>/<task-id>
```

No reutilizar un workspace con estado incierto.

## 53.2 Boot sequence

```text
1. resolve repository with connector
2. resolve default branch and remote SHA
3. inspect available local workspace
4. classify network capability
5. materialize exact source
6. verify local/remote identity
7. install dependencies
8. run baseline
9. create branch after approval
```

## 53.3 Ruta A — Checkout local existente

```bash
cd <workspace>
git status --short
git remote -v
git branch --show-current
git rev-parse HEAD
git rev-parse HEAD^{tree}
```

Luego comparar el SHA local con el conector.

Si no coincide:

- hacer preflight de red;
- fetch solo si funciona;
- si no funciona, marcar checkout stale;
- no modificar sobre una base stale salvo autorización explícita.

## 53.4 Ruta B — Clone directo disponible

Solo después de preflight exitoso:

```bash
# GitHub remote source: materialize an exact connector-backed snapshot; do not use git clone.
cd <workspace>
git remote -v
# GitHub remote refresh: resolve refs and commits through the connector; do not use git fetch.
git switch {{default_branch}}
# GitHub remote refresh: rebuild the connector-backed snapshot; do not use git pull.
git status --short
git rev-parse HEAD
git rev-parse HEAD^{tree}
```

Verificar el HEAD local contra el commit remoto recuperado por conector.

## 53.5 Ruta C — Red directa no disponible

No afirmar que el conector hizo un clone.

Opciones válidas:

```text
connector-only audit
existing checkout at exact SHA
complete source snapshot from a supported connector download
workflow artifact recovery approved by the user
small connector-native text change explicitly approved
```

Opciones inválidas:

```text
loop de clone/fetch
reconstrucción manual amplia sin manifest
partial files treated as complete repo
commit/push claims without .git
CI claims without final SHA
```

## 53.6 Manifest de snapshot

Si se materializa source sin `.git`, crear un manifest local no versionado:

```text
repository
requested ref
resolved commit SHA
retrieval method
file count
missing paths
binary handling
symlink handling
submodule handling
completeness
checksum, si existe
```

No usar un snapshot parcial para full validation.

## 53.7 Entorno reproducible

Registrar:

```text
OS
architecture
Node
npm
Electron
Git
GitHub connector
shell
timezone
line-ending config
display capability
screenshot capability
```

Comandos:

```bash
node --version
npm --version
git --version
# No GitHub CLI network path: use the connector session.
git config --get core.autocrlf
git config --get core.eol
```

## 53.8 Limpieza controlada

Antes de baseline:

```bash
git clean -ndx
```

No ejecutar:

```bash
git clean -fdx
```

sin comprobar que no destruye material necesario.

## 53.9 Variables de entorno relevantes

Inspeccionar solo nombres y valores no sensibles:

```text
NODE_OPTIONS
npm_config_ignore_scripts
CI
ELECTRON_SKIP_BINARY_DOWNLOAD
ELECTRON_MIRROR
DISPLAY
WAYLAND_DISPLAY
```

No imprimir secretos.

## 53.10 Reproducibilidad

Una validación se considera reproducible cuando:

- parte de un checkout o snapshot completo identificado por SHA;
- usa lockfile;
- usa versión de Node declarada;
- no depende de estado global;
- no depende del reloj salvo inyección;
- no depende de red salvo instalación declarada;
- deja working tree limpio;
- registra si hubo UI real o modo headless.

## 53.11 Handoff de workspace

Al terminar, reportar:

```text
workspace mode
base SHA
HEAD SHA
tree SHA
branch
network mode
connector operations
local commands
build state
launch state
screenshot state
unverified capabilities
```

---

# 54. Sistema de delegación de nivel industria

## 54.1 Objetivo

Delegar no es enviar un pedido genérico. Es transferir una unidad de trabajo verificable con límites claros.

Cada delegación debe contener:

```text
context
goal
inputs
owned files
non-owned files
contracts
constraints
tests
deliverables
acceptance criteria
handoff format
escalation rules
```

## 54.2 Unidad de delegación

Una unidad debe ser:

- cohesiva;
- independiente;
- testeable;
- integrable;
- limitada;
- con ownership claro.

Mal:

```text
hacé toda la feature
```

Bien:

```text
Implementá el modelo de source revision y sus validators puros
en packages/core/project/source-identity/**.
No integres main ni IPC.
Entregá tests unitarios y un handoff con exports.
```

## 54.3 RACI

Para cambios grandes, definir:

| Workstream | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Architecture | Staff Engineer | Tech Lead | Security, QA | Team |
| Core contracts | Senior Core Dev | Tech Lead | Main Dev | QA |
| Main integration | Runtime Dev | Tech Lead | Security | Renderer |
| IPC | Runtime Dev | Architect | Security | QA |
| Renderer | UI Dev | Tech Lead | UX | QA |
| Tests | QA Engineer | QA Lead | Developers | Release |
| Docs | Docs Owner | Tech Lead | Developers | Team |
| Release | Release Manager | Engineering Manager | QA | Stakeholders |

Aunque un solo agente ejecute, usar esta separación para evitar mezclar responsabilidades.

## 54.4 Delegation packet

Formato obligatorio:

```text
TASK ID:
ROLE:
OBJECTIVE:
BASE SHA:
BRANCH:
OWNED PATHS:
READ-ONLY PATHS:
PROHIBITED PATHS:
INPUT CONTRACTS:
OUTPUT CONTRACTS:
IMPLEMENTATION NOTES:
TEST MATRIX:
VALIDATION COMMANDS:
DEFINITION OF DONE:
ESCALATION CONDITIONS:
HANDOFF FORMAT:
```

## 54.5 Escalation conditions

El delegado debe detenerse si:

- necesita tocar un path no owned;
- descubre contrato incompatible;
- encuentra baseline roto;
- necesita dependencia;
- cambia lockfile;
- aparece riesgo de seguridad;
- necesita alterar API pública;
- necesita refactor transversal;
- tests existentes contradicen el plan;
- main cambió;
- no puede reproducir el error.

## 54.6 No delegation by omission

No asumir que el delegado sabe:

- qué branch usar;
- qué commit base;
- qué no tocar;
- cuántos commits crear;
- si abrir PR;
- si mergear;
- qué validators ejecutar;
- qué docs actualizar.

Todo debe declararse.

---

# 55. Delegación entre múltiples chats o agentes

## 55.1 Cuándo paralelizar

Paralelizar solo si los workstreams:

- no editan los mismos archivos;
- no dependen de tipos inestables;
- tienen contratos acordados;
- pueden validarse aisladamente;
- tienen un integration owner.

No paralelizar:

- cambio de contrato central + consumers antes de estabilizar tipos;
- dos agentes editando `package.json`;
- dos agentes editando el mismo workflow;
- dos agentes editando metadata generada;
- dos agentes creando commits sobre la misma branch sin coordinación.

## 55.2 Dependency graph

Representar:

```text
A: contracts
B: core implementation depends on A
C: main integration depends on A
D: renderer depends on A + C
E: tests depend on A + B + C
F: docs depends on final A-D
G: release depends on all
```

Ejecutar:

```text
A
→ B and C in parallel
→ D
→ E
→ F
→ G
```

## 55.3 Integration owner

Una sola persona/agente debe:

- integrar;
- resolver conflictos;
- ejecutar full gate;
- revisar diff global;
- crear commit final;
- publicar.

Los delegados no deben hacer push de commits parciales salvo diseño aprobado.

## 55.4 Handoff contract

Cada delegado entrega:

```text
Summary
Files changed
Contracts added/changed
Behavior
Tests run
Known limitations
Risks
Open questions
Suggested integration order
```

## 55.5 Handoff verification

El integrador debe:

- leer diff;
- ejecutar tests;
- verificar paths;
- comprobar que no hay scope extra;
- validar contracts;
- no confiar solo en resumen.

---

# 56. Estrategias de descomposición

## 56.1 Vertical slice

Preferido cuando se busca capacidad usable:

```text
contract
→ service
→ IPC
→ UI
→ test
→ docs
```

## 56.2 Horizontal slice

Usar para foundations:

```text
types
→ validators
→ builders
→ consumers
```

## 56.3 Walking skeleton

Para sistemas nuevos:

- flujo mínimo end-to-end;
- sin optimización;
- con boundaries reales;
- con tests smoke;
- luego profundizar.

## 56.4 Strangler pattern

Para reemplazar subsistemas:

```text
old path
→ adapter
→ new path for limited cases
→ expand
→ retire old
```

No hacer big-bang rewrite sin necesidad.

## 56.5 Branch by abstraction

Para migraciones internas:

- introducir interface;
- adaptar implementación vieja;
- agregar implementación nueva;
- migrar consumers;
- retirar vieja.

No confundir con branches Git.

---
