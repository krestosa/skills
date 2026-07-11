---

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

# SOURCE: authorization.md

# Contexto de autorización abreviado

Contexto de autorización:

El usuario declara que `{{repository_full_name}}` es un repositorio propio o bajo su control legítimo. La tarea se limita a mantenimiento, desarrollo, validación, documentación y operaciones Git/GitHub expresamente autorizadas sobre ese repositorio. No se autoriza actuar sobre repositorios, cuentas o infraestructura de terceros.

Esta es la única versión que debe copiarse a prompts derivados. La política extensa permanece en `../core/project-authority-and-roles.md` y `../policies/repository-context-and-authorization.md`.


---

# SOURCE: authorization-envelope.md

# Template — autorización estructurada

```yaml
authorization:
  schemaVersion: 1
  repository: {{repository_full_name}}
  stage: implementation
  plan_revision: <integer>
  base_sha: <verified-sha>
  branch: <exact-branch>
  objective: <single-goal>
  allowed_paths:
    - <path-or-glob>
  prohibited_paths:
    - <path-or-glob>
  dependencies:
    allow_new: false
    lockfile_change: false
  commits:
    count: 1
    message: <exact-message>
  remote_writes:
    create_branch: false
    publish_commit: false
    create_pr: false
    update_pr: false
    issue_actions: false
    review_actions: false
    rerun_ci: false
    auto_merge: false
    merge: false
    contents_api: false
    git_data_api: false
    move_ref: false
    force_ref: false
  validation:
    required:
      - <command-or-gate>
```

Aprobación sugerida:

```text
Aprobado. Procedé exactamente con el sobre de autorización revision <n>.
```

Una formulación diferente también es válida si referencia inequívocamente el mismo sobre.


---

# SOURCE: planning-prompt.md

# Template — planificación

Incluir primero el contenido de `authorization.md`.

```text
Seguimos en:

{{repository_full_name}}

Base conocida, solo como referencia a verificar:
<sha>

Branch propuesta:
<branch>

Objetivo único:
<goal>

ETAPA 1 — Investigación y plan.
ETAPA 2 — Implementación después de aprobación.

Comenzá únicamente con ETAPA 1.
No modifiques archivos, no crees branch, no hagas commit, publicación remota, PR ni merge.
Entregá estado, diagnóstico, arquitectura, files plan, tests, validators, docs, riesgos, validación, Git plan y el sobre de autorización propuesto.
Detenete.
```

Las reglas completas están en los playbooks canónicos 02, 03 y 07.


---

# SOURCE: correction-prompt.md

# Template — corrección puntual

Incluir primero el contenido de `authorization.md`.

```text
Seguimos en:

{{repository_full_name}}
<branch>

Error verificable:
<command/output>

Objetivo único:
<minimal-fix>

Archivos permitidos:
<paths>

No tocar:
<paths>

Validaciones:
<commands>

Aplicar solamente después de autorización inequívoca del sobre correspondiente.
```

Las reglas completas permanecen en los playbooks canónicos 02, 04 y 07.


---

# SOURCE: audit-prompt.md

# Template — auditoría

Incluir primero el contenido de `authorization.md`.

```text
Auditá:

{{repository_full_name}}
<branch>
<commit>
<run>

No modifiques nada.
Verificá commit, parent, tree, ref, compare, archivos, CI, PR, merge y contradicciones.
No uses reportes previos como fuente de verdad.
```

Las reglas completas permanecen en los playbooks canónicos 03, 05, 06 y 08.


---

# SOURCE: recovery-prompt.md

# Template — recuperación

Incluir primero el contenido de `authorization.md`.

```text
Estado remoto verificado:
<evidence>

Objetivo:
recuperar la implementación desde una fuente verificable, aplicarla sobre una base limpia, validar, crear una historia limpia, publicar y verificar.

No mezclar branches de transporte, Base64, logs, artifacts operativos ni commits diagnósticos.
No usar force.
No abrir PR ni mergear salvo autorización explícita.
```

Las reglas completas permanecen en los playbooks canónicos 06, 08 y 12.
