## 52.9 Catálogo operativo de capacidades Write del conector

Las acciones Write modifican estado remoto. Su disponibilidad técnica no constituye autorización para ejecutarlas.

Toda write action debe satisfacer:

```text
explicit user intent
+ exact repository
+ exact target object
+ current state read
+ mutation semantics understood
+ permission available
+ conflict/race gate
+ post-write verification
```

Para el repositorio objetivo, el target por defecto es:

```text
repository_full_name = {{repository_full_name}}
```

No extender esta autorización a otros repositorios, forks, organizaciones, packages, deployments o infraestructura.

### 52.9.1 Niveles de riesgo de escritura

Clasificar cada operación antes de ejecutarla:

| Level | Clase | Ejemplos | Autorización |
|---|---|---|---|
| W1 | interacción reversible | reactions, comment edits, labels, assignees | explícita para el objeto o lote definido |
| W2 | coordinación y estado | issue create/update, reviews, reviewers, draft/ready, thread resolve | explícita y con target verificado |
| W3 | publicación de contenido | create/update/delete file, branch creation, PR creation/update | plan aprobado + preflight + post-verificación |
| W4 | historia Git remota | blobs, trees, commits, ref movement | autorización específica para publicación connector-native |
| W5 | promoción o ejecución remota | rerun CI, auto-merge, merge, force ref | autorización inmediata y gates críticos completos |

Una aprobación para implementar código no incluye automáticamente W1–W5. Una aprobación para publicar una branch puede cubrir las operaciones de branch/commit/push definidas en el plan, pero no comentarios, reviews, merge, auto-merge ni reruns salvo que estén incluidos de forma expresa.

### 52.9.2 Preflight universal de escritura

Antes de cualquier write action, registrar:

```text
repository_full_name
operation name
risk level
target type
target identifier
current object state
expected branch/head SHA
requested mutation
additive vs replacement semantics
reversibility
rollback action
user authorization evidence
```

Gates obligatorios:

1. Resolver `{{repository_full_name}}` mediante el conector.
2. Confirmar permisos relevantes de la instalación.
3. Leer el objeto actual con una acción Read exacta.
4. Verificar que IDs y refs pertenecen al repositorio esperado.
5. Verificar que la mutación coincide con el alcance aprobado.
6. Detectar si la acción agrega, reemplaza o elimina estado.
7. Evitar writes paralelos sobre el mismo recurso.
8. Ejecutar una sola mutación lógica por vez cuando exista dependencia secuencial.
9. Recuperar el objeto final y comparar intención contra resultado.
10. Registrar SHA, ID o estado remoto resultante.

No usar datos narrativos como sustituto de IDs remotos. No adivinar `comment_id`, `thread_id`, `review_id`, `artifact_id`, `job_id`, `run_id`, `content SHA`, `tree SHA`, `commit SHA` ni branch head.

### 52.9.3 Comentarios top-level, replies y actualización de comentarios

Superficies:

```text
PR Conversation comment = issue comment top-level
inline review comment    = comentario anclado al diff
review reply             = respuesta dentro del thread inline
review submission        = review COMMENT/APPROVE/REQUEST_CHANGES
```

Acciones:

```text
add_comment_to_issue
reply_to_review_comment
update_issue_comment
update_review_comment
```

Reglas:

- `add_comment_to_issue` crea un comentario top-level en la conversación del PR; aunque use la infraestructura de Issues, el target se identifica por `pr_number`.
- No usar un comentario top-level para simular una respuesta inline cuando existe un thread específico.
- `reply_to_review_comment` requiere el ID del comentario inline top-level del thread. No usar el ID de una reply-to-reply.
- `update_issue_comment` reemplaza el cuerpo completo del comentario top-level. Leer el cuerpo actual antes de reemplazarlo.
- `update_review_comment` reemplaza el cuerpo completo de un comentario inline o reply. Verificar el tipo y el ID antes de editar.
- No publicar mensajes vacíos, placeholders, diagnósticos internos, secretos, paths locales, logs masivos ni texto de source innecesario.
- Cuando el usuario pide “responder”, preparar el texto y ejecutar la write action solo si el pedido incluye publicación inmediata.
- Después de publicar o actualizar, recuperar la conversación/thread y comprobar autor, body y ubicación.

### 52.9.4 Reactions

Acciones:

```text
add_reaction_to_issue_comment
add_reaction_to_pr
add_reaction_to_pr_review_comment
remove_reaction_from_issue_comment
remove_reaction_from_pr
remove_reaction_from_pr_review_comment
```

Reglas:

- Agregar una reaction requiere el identificador de reaction admitido por GitHub, por ejemplo `+1` o `eyes`.
- Quitar una reaction requiere `reaction_id`, no solo el tipo de reaction.
- Leer reactions cuando sea necesario identificar la reaction exacta del usuario autenticado.
- No retirar reactions de terceros.
- No usar reactions como sustituto de una review formal, una aprobación de plan o una confirmación técnica.
- Tratar las reactions como writes W1, pero igualmente exigir autorización cuando la acción no sea parte explícita del pedido.

### 52.9.5 Issues, labels, assignees y conversation locking

Acciones:

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

Semántica crítica:

- `create_issue` crea title y body, y puede incluir assignees, labels y milestone.
- `add_issue_labels` es aditiva.
- `remove_issue_label` quita una etiqueta exacta.
- `add_issue_assignees` es aditiva y admite hasta el límite del endpoint.
- `remove_issue_assignees` quita usuarios específicos.
- `update_issue(labels=...)` reemplaza el conjunto completo de labels.
- `update_issue(assignees=...)` reemplaza el conjunto completo de assignees.
- `update_issue` puede cambiar title, body, state, state reason y milestone.
- `lock_issue_conversation` admite únicamente reasons soportados: `off-topic`, `too heated`, `resolved`, `spam`.

Antes de `update_issue`:

```text
fetch issue
→ preserve fields not intended to change
→ distinguish omitted field from replacement value
→ confirm state transition and state_reason
```

No usar `update_issue` para agregar una única label o assignee si existe una acción aditiva. Esto evita borrar accidentalmente el conjunto previo.

Cerrar, reabrir, marcar duplicate/not planned, lockear o desbloquear requiere autorización específica porque cambia workflow y visibilidad de colaboración.

Después de la mutación, verificar:

- title/body cuando se modificaron;
- state y state reason;
- labels finales;
- assignees finales;
- milestone;
- lock state cuando pueda recuperarse.

### 52.9.6 Pull requests: creación, metadata y lifecycle

Acciones:

```text
create_pull_request
update_pull_request
convert_pull_request_to_draft
mark_pull_request_ready_for_review
enable_auto_merge
merge_pull_request
```

#### Crear PR

Antes de `create_pull_request`:

1. Verificar que la head branch existe remotamente.
2. Resolver head SHA exacto.
3. Resolver base branch y base SHA.
4. Comparar base/head.
5. Verificar que el diff no esté vacío.
6. Verificar que la branch contiene solo el alcance aprobado.
7. Definir draft state.
8. Construir title y body a partir del diff real y validaciones reales.

Por defecto en el repositorio objetivo:

```text
draft = true
base = {{default_branch}}, salvo base apilada aprobada
head = branch exacta publicada
```

No crear PR contra una base inferida si el plan definió una base apilada.

#### Actualizar PR

`update_pull_request` puede modificar:

```text
title
body
state open/closed
base branch
maintainer_can_modify
```

Cambiar base branch invalida comparaciones, review context y CI assumptions. Tratarlo como W3 y volver a auditar el diff.

Cerrar o reabrir un PR no equivale a mergearlo. Verificar el estado final.

#### Draft y ready

- `convert_pull_request_to_draft` requiere PR abierto.
- `mark_pull_request_ready_for_review` cambia el estado de revisión, no la corrección técnica.
- No marcar ready si CI, docs, review o scope gates están incompletos.
- No convertir a draft como forma de ocultar un fallo; documentar el motivo operativo.

### 52.9.7 Review submissions, reviewers y review lifecycle

Acciones:

```text
add_review_to_pr
dismiss_pull_request_review
request_pull_request_reviewers
remove_pull_request_reviewers
```

`add_review_to_pr` admite:

```text
COMMENT
APPROVE
REQUEST_CHANGES
```

Reglas:

- `review` es obligatorio para `COMMENT` y `REQUEST_CHANGES`.
- Para `APPROVE`, incluir texto solo si aporta contexto.
- Las inline file comments deben anclarse a paths y líneas/positions válidas del diff actual.
- Usar `commit_id` para anclar una review cuando se necesita garantizar el head revisado.
- Volver a leer head SHA inmediatamente antes de aprobar o solicitar cambios.
- No aprobar si existen BLOCKER/MAJOR, CI crítico faltante, diff no revisado o head cambiado.
- No emitir `REQUEST_CHANGES` por preferencias menores.
- `dismiss_pull_request_review` requiere el GraphQL `review_id` exacto y un mensaje de dismissal; no usar el número del PR o un comment ID como sustituto.
- No dismiss una review sin autorización específica y motivo claro.
- Request reviewers debe diferenciar usernames individuales y team slugs.
- Remove reviewers solo debe quitar solicitudes exactas; no retirar reviewers por conveniencia.

Una review emitida por el agente es una acción de gobernanza. Nunca se deriva automáticamente de haber analizado el PR.

### 52.9.8 Review threads: reply, resolve y reopen

Acciones:

```text
reply_to_review_comment
resolve_review_thread
unresolve_review_thread
```

Workflow:

```text
list_pull_request_review_threads
→ identify exact thread ID
→ verify unresolved/resolved and outdated state
→ inspect all comments
→ determine whether code or explanation satisfies request
→ reply if authorized
→ resolve only if authorized and actually addressed
```

Reglas:

- Resolver un thread no demuestra que el cambio sea correcto.
- No resolver un thread ambiguo, conflictivo o parcialmente atendido.
- No resolver threads outdated automáticamente; primero determinar si el problema sigue vigente.
- `unresolve_review_thread` se usa cuando reaparece el problema o la resolución fue incorrecta, no para generar actividad artificial.
- Después de resolve/unresolve, volver a listar threads y verificar `isResolved`.

### 52.9.9 Labels específicos de PR

Acción:

```text
label_pr
```

Usar para agregar una label individual a un PR cuando la acción específica esté disponible.

Alternativas:

```text
add_issue_labels     = agregar una o más labels a issue/PR
remove_issue_label   = quitar una label exacta
update_issue labels  = reemplazar todo el conjunto; evitar para operaciones aditivas
```

Antes de etiquetar:

- verificar que la label existe o que el endpoint la acepta;
- verificar labels actuales;
- evitar duplicados;
- no usar labels para afirmar CI, aprobación o merge state que no exista.
