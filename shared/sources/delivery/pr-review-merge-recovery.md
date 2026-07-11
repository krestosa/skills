# 32. Pull Request

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

Solo abrir o modificar un PR con autorización explícita.

## 32.1 Responsabilidad connector-first

Después de que la branch exista en el remoto, preferir el conector para:

- crear PR;
- obtener metadata;
- inspeccionar patch y archivos cambiados;
- actualizar title o body;
- cambiar draft/ready state;
- solicitar reviewers;
- aplicar labels;
- consultar reviews y threads;
- mergear únicamente cuando se autorice.

La creación de PR debe usar `create_pull_request`; si esa acción no está disponible:

- el conector no puede inferir repo/head/base;
- existe un fork;
- el head pertenece a otro repositorio;
- la semántica cross-repo no queda representada de forma segura.

## 32.2 Prerrequisitos

- branch remota verificada;
- commit verificado;
- CI verde o estado de excepción explícito;
- docs actualizadas;
- no artifacts operativos;
- no branch auxiliar;
- no scope extra;
- base y head exactos.

## 32.3 Draft por defecto

Crear draft salvo que el usuario pida expresamente ready-for-review.

## 32.4 PR body

```text
Summary
Scope
Architecture
Behavior
Safety boundaries
Validation
Files
Risks
Out of scope
```

La descripción debe reflejar el diff remoto real, no el plan inicial.

---

# 33. Code Review y follow-up de comentarios

Actuar como reviewer senior y usar datos thread-aware cuando existan.

## 33.1 Lectura de review

Orden preferido:

1. PR metadata mediante conector.
2. Lista de archivos y patch mediante conector.
3. Review submissions mediante conector.
4. Review threads con estado `resolved`, anchors y comentarios mediante conector, si la función está disponible.
5. Usar acciones thread-aware del conector; si no preservan el campo o estado requerido, bloquear esa parte y reportar la capacidad faltante.

No asumir que una superficie plana de comentarios representa todos los threads. Tampoco asumir lo contrario: descubrir primero si la sesión ofrece una función thread-aware.

## 33.2 Clasificación de feedback

Separar:

```text
actionable unresolved
informational
approval
resolved
outdated
duplicate
conflicting
ambiguous
```

Agrupar por archivo o comportamiento.

## 33.3 Scope de corrección

Antes de editar:

- enumerar threads accionables;
- vincular cada cambio a un thread o cluster;
- no resolver todos si el usuario no lo pidió;
- si pidió “todo”, interpretar todos los unresolved accionables;
- elevar contradicciones antes de cambiar código.

## 33.4 Write safety

Las operaciones de colaboración en GitHub son write actions remotas independientes del cambio de código. Leer un PR o implementar una corrección no autoriza automáticamente a escribir en la conversación.

No ejecutar sin autorización explícita y específica:

- crear o actualizar comentarios top-level;
- responder inline review comments;
- actualizar comentarios inline o replies;
- resolver o reabrir review threads;
- enviar reviews `COMMENT`, `APPROVE` o `REQUEST_CHANGES`;
- dismiss reviews existentes;
- agregar o quitar reactions;
- solicitar o remover reviewers;
- convertir el PR a draft o marcarlo ready;
- modificar base branch, title, body o state;
- habilitar auto-merge;
- mergear.

Antes de una write action de review, volver a leer:

```text
repository
PR number
head SHA
comment/review/thread ID
resolved/outdated state
current body when replacing content
```

Después de escribir, volver a consultar el objeto y confirmar que la mutación se aplicó al target correcto. No interpretar una respuesta HTTP exitosa como verificación suficiente cuando existe una acción Read para recuperar el estado final.

## 33.5 Review técnico

Revisar:

- correctness;
- architecture;
- security;
- performance;
- error handling;
- tests;
- docs;
- naming;
- ownership;
- backwards compatibility;
- migration;
- release risk.

Clasificar findings:

```text
BLOCKER
MAJOR
MINOR
NIT
QUESTION
```

No aprobar con BLOCKER o MAJOR abierto.

---

# 34. Merge

Solo por pedido explícito.

Antes:

- PR open;
- CI green;
- head current;
- base current;
- mergeable;
- no unresolved review;
- no drift;
- no branch contamination.

Después:

- merged true;
- merge commit;
- `{{default_branch}}` HEAD;
- post-merge workflow;
- docs/roadmap;
- branch cleanup.

---

# 35. Post-merge

Verificar:

```text
`{{default_branch}}` contains commit
workflow passes
branch may be deleted
roadmap is current
docs links pass
no temporary files
```

Cerrar fase solo después.

---

# 36. Manejo de branches

## 36.1 Nombres

```text
feature/
fix/
docs/
tooling/
chore/
recovery/
```

## 36.2 No branches auxiliares

Evitar:

```text
publish/
transport/
diagnostic/
tmp/
upload/
patch/
```

## 36.3 Limpieza

Después de merge:

```bash
# GitHub remote publication: use connector Git Data API or connector write actions; do not use git push.
git branch -D <branch>
# GitHub remote refresh: resolve refs and commits through the connector; do not use git fetch.
```

No eliminar branches sin confirmación cuando sea destructivo.

---

# 37. Recuperación de publicación fallida

Activar modo RECOVERY cuando:

- SHA no existe;
- branch vacía;
- implementación en artifacts;
- branch auxiliar contaminada;
- PR parcial;
- CI sobre tree distinto.

Procedimiento:

```text
freeze
→ inspect
→ identify clean base
→ identify real patch
→ verify checksum/tree
→ create clean workspace
→ apply
→ validate
→ commit
→ publish
→ verify
→ delete auxiliary branch
```

No mergear ramas de transporte.

No convertir commits operativos en historia de producto.

---

# 38. Incident management

## 38.1 Severity

### SEV-1

- `{{default_branch}}` roto;
- security regression;
- data loss;
- credentials exposed.

### SEV-2

- CI bloqueado;
- release imposible;
- branch final incorrecta;
- commit perdido.

### SEV-3

- validator false positive;
- docs drift;
- non-critical feature regression.

## 38.2 Incident report

```text
Summary
Impact
Timeline
Root cause
Contributing factors
Detection gap
Resolution
Preventive actions
```

---
