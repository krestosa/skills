### 52.9.15 PR conversation locks y moderación

Acciones:

```text
lock_issue_conversation
unlock_issue_conversation
```

Estas acciones aplican tanto a issues como a PR conversations a través del número del recurso.

Tratar como moderación W2/W5 según impacto. Requieren:

- target exacto;
- motivo permitido cuando se lockea;
- autorización específica;
- verificación de que no se bloquea una discusión activa necesaria para entrega o review.

No lockear automáticamente porque un issue o PR esté cerrado o resuelto.

### 52.9.16 Matriz Read-before-Write y post-verificación

| Write action | Read-before-write | Post-verificación |
|---|---|---|
| Add/update PR comment | PR/comments + exact ID | fetch comments/timeline |
| Reply/update inline comment | review threads + comment ID | list threads/comments |
| Resolve/unresolve thread | exact thread state | list review threads |
| Add/remove reaction | current reactions when removal/ownership matters | reactions list |
| Create/update issue | repo + issue current state | fetch issue |
| Add/remove labels/assignees | current issue/PR snapshot | fetch issue/PR |
| Create PR | branch heads + compare | fetch PR + patch |
| Update PR | PR current metadata/head/base | fetch PR info |
| Submit/dismiss review | reviews + head SHA | list reviews |
| Request/remove reviewers | PR current requested reviewers | fetch PR |
| Draft/ready | PR lifecycle state | fetch PR |
| Create/update/delete file | fetch path/ref/blob SHA | fetch file + commit |
| Create blob/tree/commit | base commit/tree + manifest | fetch blob/commit + compare |
| Create branch/update ref | branch existence/current head | search/resolve branch + fetch commit |
| Rerun workflow/job | run/jobs/steps/logs | latest attempt jobs/logs |
| Auto-merge/merge | PR, reviews, checks, exact head | fetch PR + merge commit + post-merge CI |
| Lock/unlock | issue/PR conversation state | fetch issue/PR |

### 52.9.17 Idempotencia, retry y concurrencia

Las write actions no deben reintentarse ciegamente después de timeout o respuesta ambigua.

Clasificar el resultado:

```text
WRITE_CONFIRMED
WRITE_REJECTED
WRITE_CONFLICT
WRITE_PERMISSION_DENIED
WRITE_RESULT_UNKNOWN
WRITE_PARTIALLY_APPLIED
```

Ante `WRITE_RESULT_UNKNOWN`:

1. No repetir inmediatamente.
2. Leer el target.
3. Buscar la mutación esperada por ID, SHA o contenido.
4. Si ya se aplicó, registrar éxito verificado.
5. Si no se aplicó y la acción es segura/idempotente, evaluar un único retry.
6. Si podría duplicarse —comment, issue, PR, review, commit— no repetir sin deduplicación.

Controles:

- comentarios/issues/PRs pueden duplicarse;
- reactions pueden ser idempotentes o rechazadas según API, pero verificar;
- update_file/delete_file usan SHA y pueden conflictar;
- create_blob puede crear objetos equivalentes sin efecto visible;
- create_commit puede dejar commits huérfanos;
- create_branch puede fallar si ya existe;
- update_ref puede competir con otro actor;
- reruns crean attempts nuevos;
- merge no es reversible mediante la misma acción.

### 52.9.18 Rollback y compensación

No toda write action tiene rollback directo.

| Acción | Compensación |
|---|---|
| Reaction add | remove exact reaction |
| Label/assignee add | remove exact item |
| Comment update | restore prior body si fue registrado |
| Issue/PR metadata update | restore prior values |
| Draft/ready | inverse lifecycle action |
| Thread resolve | unresolve |
| Thread unresolve | resolve, solo si sigue justificado |
| File commit | revert mediante commit nuevo; no rewrite de historia |
| Branch create | delete branch solo con acción disponible y autorización; si no, dejar y reportar |
| Ref fast-forward | revert commit o nuevo commit; no force rewind |
| Rerun | no rollback; registrar attempt |
| Merge | revert commit/PR separado; no reset de la default branch |
| Auto-merge | deshabilitar solo si existe acción disponible; de lo contrario informar limitación |

Antes de una operación W4/W5, el plan debe declarar la estrategia de compensación.

### 52.9.19 Registro de auditoría de writes

Por cada write action registrar internamente:

```text
timestamp
repository
operation
authorization scope
target IDs
pre-state fingerprint
request summary
result IDs/SHAs
post-state fingerprint
verification action
rollback/compensation
confidence
```

El reporte final debe incluir las writes materiales, no los payloads internos completos.

Formato:

```text
Action:
Target:
Before:
Mutation:
Result:
Verified by:
Residual risk:
```

### 52.9.20 Política específica de escritura para el repositorio objetivo

Defaults:

```text
repository: {{repository_full_name}}
default branch: {{default_branch}}
normal implementation: local edit + validation + local commit + push
normal PR state: draft
normal commit count: one per microphase
normal ref update: fast-forward only
normal merge: prohibited unless explicitly requested
normal auto-merge: disabled unless explicitly requested
normal CI rerun: prohibited until root cause is inspected
```

Prohibiciones por defecto:

- escribir archivos directamente sobre `{{default_branch}}`;
- crear múltiples commits Contents API para simular una microfase atómica;
- usar `update_ref(force=true)`;
- crear merge commits con `additional_parent_shas` fuera de un merge deliberado;
- responder o resolver review feedback sin pedido;
- aprobar el propio trabajo automáticamente;
- marcar ready con gates pendientes;
- mergear con head SHA no fijado;
- rerun repetitivo para buscar un pase casual;
- editar comments para ocultar contradicciones históricas;
- cerrar issues/PRs solo para limpiar estado;
- publicar source no validado cuando la validación era materialmente posible.

Fallback permitido cuando shell no puede resolver GitHub:

```text
connector remote reads
→ exact source/patch preparation
→ local validation if complete workspace exists
→ connector-native atomic commit on isolated branch
→ remote compare
→ CI discovery from exact SHA
→ draft PR
```

Si no existe workspace completo y el cambio es amplio, detener publicación y limitarse a plan/auditoría. La disponibilidad de writes remotas no justifica publicar código no validado.

### 52.9.21 Mapa exacto de acciones Write conocidas

Cuando estén expuestas en la sesión, usar los nombres y contratos exactos.

#### Comments and reactions

```text
add_comment_to_issue
update_issue_comment
reply_to_review_comment
update_review_comment
add_reaction_to_issue_comment
remove_reaction_from_issue_comment
add_reaction_to_pr
remove_reaction_from_pr
add_reaction_to_pr_review_comment
remove_reaction_from_pr_review_comment
```

#### Issues, labels, assignees and moderation

```text
create_issue
update_issue
add_issue_labels
remove_issue_label
add_issue_assignees
remove_issue_assignees
lock_issue_conversation
unlock_issue_conversation
```

#### Pull requests, reviews and lifecycle writes

```text
create_pull_request
update_pull_request
convert_pull_request_to_draft
mark_pull_request_ready_for_review
label_pr
request_pull_request_reviewers
remove_pull_request_reviewers
add_review_to_pr
dismiss_pull_request_review
resolve_review_thread
unresolve_review_thread
enable_auto_merge
merge_pull_request
```

#### Repository contents

```text
create_file
update_file
delete_file
```

#### Git Data and refs

```text
create_blob
create_tree
create_commit
create_branch
update_ref
```

#### GitHub Actions

```text
rerun_failed_workflow_run_jobs
rerun_workflow_job
```

Esta lista no reemplaza capability discovery. Una acción documentada pero no cargada no debe invocarse ni simularse con un nombre inventado.

### 52.9.22 Selección entre local Git, Contents API y Git Data API

| Situación | Ruta preferida |
|---|---|
| Implementación normal con red directa | local Git commit + push |
| PR/issue/review metadata | connector write específica |
| Cambio aislado de un solo archivo textual | local Git; Contents API solo si está aprobado |
| Cambio multiarchivo atómico sin push disponible | Git Data API connector-native aprobada |
| Recovery de commit conocido | Git Data API con parent/tree verificados |
| Branch creation remota | create_branch desde SHA exacto |
| Branch update normal | local push; update_ref fast-forward como fallback aprobado |
| Merge | connector merge con expected head SHA |
| CI transient rerun | connector rerun después de diagnóstico |

No mezclar rutas dentro de la misma publicación sin un plan explícito. Por ejemplo, no crear dos archivos con Contents API y completar el resto con un commit Git Data sobre una base que ya cambió sin reconstruir el parent y tree.

### 52.9.23 Write action completion gate

Una write action está cerrada solo cuando:

```text
request authorized
+ target exact
+ mutation executed
+ resulting object identified
+ remote state re-read
+ expected effect confirmed
+ unintended effect excluded as far as observable
+ residual limitation reported
```

Una respuesta del conector sin verificación posterior se reporta como:

```text
write accepted by connector; final state not independently verified
```

No como éxito completo.
