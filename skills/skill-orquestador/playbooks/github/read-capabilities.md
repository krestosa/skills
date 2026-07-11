## 52.8 Catálogo normalizado de capacidades de lectura del conector

Las capacidades documentadas por el conector deben convertirse en decisiones operativas. No insertar una lista plana de acciones sin contexto.

Para cada acción, registrar:

```text
action family
exact capability discovered in this session
required identifiers
pagination behavior
freshness/ref semantics
possible blind spots
output used as evidence
fallback
```

Una capacidad descrita por la documentación no se considera disponible hasta que la sesión exponga la acción correspondiente. Si una acción no está cargada, usar una alternativa explícita o marcar el dato como no verificable.

### 52.8.1 Resolución del repositorio y de la identidad autenticada

Repositorio por defecto:

```text
repository_full_name = {{repository_full_name}}
repository_id = 1289676191, solo como identificador secundario verificado
repository_url = {{repository_url}}, solo cuando una acción requiera URL
```

Para acciones que permiten seleccionar el repositorio mediante:

```text
repository_full_name
repository_id
repository_url
```

poblar exactamente uno. Para el repositorio objetivo, preferir siempre:

```text
repository_full_name: {{repository_full_name}}
```

No enviar simultáneamente nombre, ID y URL.

Usar metadata del repositorio para verificar:

- que la instalación puede resolver `{{repository_full_name}}`;
- owner y nombre;
- visibilidad;
- default branch;
- permisos efectivos;
- estado archived;
- políticas de merge relevantes;
- clone URL solo como dato, no como prueba de que shell puede resolverla.

La comprobación realizada mediante el conector debe distinguir:

```text
REPOSITORY_CONNECTOR_RESOLVED
REPOSITORY_NOT_INSTALLED
REPOSITORY_ACCESS_DENIED
REPOSITORY_NOT_FOUND
REPOSITORY_SELECTOR_INVALID
```

Para identidad y autorización remota, usar cuando estén disponibles:

```text
get authenticated profile
get authenticated login
get collaborator permission
get installation/account scope
list installed accounts
list installations
list accessible repositories
list repositories by installation
list repositories by affiliation
list user organizations and memberships
```

No confundir:

```text
connector has admin/push permission
```

con:

```text
connector session can resolve the target repository
local git can reach github.com
shell can push
```

Son planos de autenticación y red distintos.

### 52.8.2 Resolución de refs, branches y commits

Toda operación debe converger a un SHA exacto.

Secuencia preferida:

```text
known repository
→ resolve or search branch/ref
→ exact commit SHA
→ fetch commit metadata
→ compare refs when relevant
```

Usar:

- resolución de branch, tag o commit-ish cuando la acción esté expuesta;
- búsqueda de branches dentro de `{{repository_full_name}}` para localizar nombres candidatos;
- búsqueda/listado de commits acotado al repositorio;
- `fetch_commit` para verificar un SHA exacto y recuperar metadata, diff y URL canónica;
- `compare_commits` para ahead/behind, base/head y estadísticas por archivo;
- raw commit diff/patch cuando la sesión exponga esa acción y se necesite evidencia textual completa.

Reglas:

- la búsqueda descubre candidatos; no sustituye `fetch_commit`;
- un SHA abreviado debe resolverse a SHA completo antes de publicación, CI o auditoría;
- una branch es mutable; volver a resolver su head antes y después de una write action;
- un compare debe registrar base y head exactos, no solo nombres narrativos;
- no inferir parentage a partir del orden de búsqueda;
- no asumir que el commit más reciente de la branch es el anunciado sin verificarlo.

Para listar commits recientes cuando la acción dedicada no esté expuesta, usar búsqueda de commits con query vacía y scope exacto al repositorio, respetando el orden descendente documentado.

### 52.8.3 Navegación de archivos, directorios, blobs y contenido

Jerarquía de lectura:

```text
fetch_file(repository, path, exact ref)
> fetch GitHub file URL
> fetch_blob(exact blob SHA)
> PR patch
> repository search result
```

Usar `fetch_file` cuando repo, path y ref son conocidos.

Reglas de `fetch_file`:

- especificar `ref` cuando la tarea depende de una branch, tag o commit particular;
- omitir `ref` solo cuando se desea explícitamente la default branch actual;
- usar rangos de líneas para archivos grandes cuando la acción lo permita;
- usar UTF-8 para texto;
- usar Base64 solo para preservar bytes o formatos no textuales y nunca para versionar payloads de transporte.

Usar fetch por URL solo cuando:

- el usuario entregó una URL de archivo válida;
- el path/ref no puede resolverse limpiamente;
- se trata de `github.com/.../blob/...`, `raw.githubusercontent.com` o una URL Contents API compatible.

Usar `fetch_blob` cuando ya existe un blob SHA verificable, especialmente para:

- contenido exacto de una entrada de tree;
- archivos no recuperables por path;
- validación de objetos Git;
- preservación binaria controlada.

Cuando la sesión exponga listado de directorios:

- listar el directorio antes de intentar materializar múltiples paths;
- registrar tipo de entrada, path y SHA;
- manejar paginación o límites;
- no asumir que un listado parcial representa todo el árbol.

`download_user_content` se usa exclusivamente para URLs `private-user-images.githubusercontent.com` provenientes de issues o PRs. No usarlo para archivos del repositorio.

### 52.8.4 Búsqueda e índice sincronizado

La búsqueda del conector sirve para descubrimiento, no para confirmar el contenido final de una ref.

Usar search de archivos:

- acotado a `{{repository_full_name}}`;
- con términos de filename, symbol, error o behavior;
- sin qualifiers incompatibles como `is:pr` en la acción de búsqueda de archivos;
- con `topn` suficiente pero limitado.

Después de encontrar un resultado:

```text
search hit
→ exact path
→ exact ref/SHA
→ fetch_file
→ inspect actual content
```

Cuando se use el índice RAG sincronizado:

- tratarlo como potencialmente desfasado hasta aproximadamente dos horas;
- usar boosts `+(entity)` solo para mejorar recall;
- usar QDF para priorización temporal, no como sustituto de ref/SHA;
- nunca usar un resultado del índice como prueba de que el archivo sigue igual en el SHA final;
- seguir links mediante fetch exacto antes de afirmar contenido.

No usar búsqueda global de repositorios cuando `{{repository_full_name}}` ya está identificado.

### 52.8.5 Issues

Para un issue conocido:

```text
fetch issue
→ fetch all issue comments
→ fetch reactions only if material
```

En acciones que aceptan múltiples selectores de repo, poblar exactamente uno.

Usar:

- fetch de issue para title, body, state, labels, assignees y metadata;
- fetch de comments paginado para reconstruir conversación;
- search de issues acotado al repositorio para descubrir candidates;
- recent issues solo para triage general.

No mezclar issue comments con review threads de PR. Aunque GitHub trate PRs como issues para ciertas APIs, conservar la semántica correcta.

### 52.8.6 Pull requests, diffs y patches

Elegir la acción según la pregunta:

```text
get_pr_info
```

para metadata, refs, estado, head/base y descripción sin traer código.

```text
fetch_pr
```

para una vista integrada con metadata, diff y opcionalmente comments.

```text
list_pr_changed_filenames
```

para obtener la lista paginada completa de paths modificados.

```text
fetch_pr_file_patch
```

para inspeccionar un path exacto devuelto por la lista de changed filenames.

```text
fetch_pr_patch / get_pr_diff
```

para recuperar el patch/diff completo del PR.

Reglas obligatorias:

1. Para patch por archivo, ejecutar primero `list_pr_changed_filenames`.
2. Pasar un path exacto retornado; no adivinar paths.
3. `patch = null` significa que el PR válido no contiene patch disponible para ese path o tipo de cambio; no equivale automáticamente a error.
4. Un 404 al pedir patch por archivo significa que repo o PR no pudo resolverse; no probar paths aleatorios.
5. Verificar `head SHA` y `base SHA` antes de usar un diff para revisión final.
6. Si el PR cambia durante la revisión, invalidar patches previos.
7. Para el alcance total, no depender solo de un patch truncado o de una primera página.

### 52.8.7 Comentarios, reviews y review threads

Las superficies no son equivalentes:

```text
issue/PR conversation comments
inline review comments
review submissions
review threads
```

Usar:

- timeline/comentarios del PR para conversación general;
- review submissions para estados `APPROVED`, `CHANGES_REQUESTED`, `COMMENTED`;
- review threads para `isResolved`, `isOutdated`, anchors, file/line y replies;
- reactions solo cuando sean relevantes para triage.

Preferir `list_pull_request_review_threads` cuando esté disponible. Esta capacidad preserva estado de resolución y reduce la necesidad de GraphQL manual.

Usar una acción thread-aware del conector solo si:

- falta un campo requerido;
- la acción está ausente;
- hay paginación incompleta;
- se necesita información de thread no preservada.

No tratar una lista plana de comentarios como representación completa de threads.

### 52.8.8 GitHub Actions: descubrimiento por SHA

Las acciones disponibles deben usarse desde el SHA final, sin exigir al usuario que proporcione el enlace del run.

Cadena primaria:

```text
final commit SHA
→ fetch_commit_workflow_runs
→ select run bound to exact head SHA
→ fetch_workflow_run_jobs
→ fetch_workflow_job_steps
→ fetch_workflow_job_logs when needed
→ fetch_workflow_run_artifacts when needed
→ download_workflow_artifact when required
```

Complementar con:

```text
get_commit_combined_status
```

para combined status y checks individuales del commit.

Limitaciones conocidas que deben registrarse:

- `fetch_commit_workflow_runs` actualmente filtra runs disparados por `pull_request`;
- devuelve solo la primera página;
- `fetch_workflow_run_jobs` devuelve la última attempt y solo la primera página;
- `fetch_workflow_run_artifacts` devuelve solo la primera página;
- combined status no sustituye logs ante un fallo;
- un check externo puede no tener jobs/logs de GitHub Actions;
- ausencia de run en esta acción no prueba que no exista un workflow `push`.

Por lo tanto:

```text
PR-triggered CI
→ connector-first end-to-end when discoverable

push-only CI
→ combined status first
→ connector run discovery if exposed
→ report incomplete connector coverage and stop that verification
```

No pedir al usuario una URL de run mientras el repositorio, SHA y branch permitan resolverla mediante el conector.

### 52.8.9 Artifacts y attachments

Para artifacts de Actions:

```text
run ID
→ list run artifacts
→ validate artifact name/id/expiry/digest metadata
→ download artifact ZIP
→ inspect locally
```

No descargar todos los artifacts por defecto. Seleccionar los relevantes para el fallo, auditoría o entrega.

Verificar:

- run ID;
- artifact ID;
- name;
- source SHA/run;
- attempt cuando pueda determinarse;
- expiration;
- size;
- digest si GitHub lo proporciona.

Un artifact no es source control y no sustituye branch/commit.

Para imágenes privadas adjuntas en issues/PRs, usar exclusivamente la acción específica de private user content.

### 52.8.10 Paginación, first-page constraints y completitud

Toda acción debe clasificarse como:

```text
FULLY_PAGINATED
FIRST_PAGE_ONLY
CURSOR_AVAILABLE
LIMITED_BY_TOPN
UNKNOWN_COMPLETENESS
```

Cuando una acción es first-page-only:

- no afirmar que “no existen más”;
- registrar el límite;
- usar otra acción del conector si existe; si no, bloquear la operación incompleta;
- priorizar por SHA, name o status para reducir ambigüedad;
- no cerrar una auditoría global con evidencia parcial.

Para listas paginadas completas declaradas por la acción, igualmente registrar el resultado total y cualquier truncamiento comunicado.

### 52.8.11 Semántica de errores

Clasificar errores del conector:

```text
NOT_FOUND
ACCESS_DENIED
INVALID_SELECTOR
INVALID_REF
RATE_LIMITED
PAGINATION_INCOMPLETE
ACTION_NOT_AVAILABLE
STALE_INDEX
TRANSIENT_CONNECTOR_ERROR
WRITE_PERMISSION_MISSING
UNKNOWN_CONNECTOR_FAILURE
```

No convertir automáticamente un 404 en “el objeto nunca existió”. Puede significar:

- repo no visible para la instalación;
- selector incorrecto;
- PR/run/commit inexistente;
- endpoint sin acceso;
- ref no resoluble.

Verificar repo y selector antes de concluir.

### 52.8.12 Matriz de selección de acciones de lectura

| Necesidad | Acción primaria | Verificación secundaria | Fallback |
|---|---|---|---|
| Verificar repo | repository metadata | authenticated identity/permissions | installed repositories |
| Resolver branch | branch/ref resolution | search branches | block if canonical resolution is unavailable |
| Verificar commit | fetch commit | compare / raw diff | local `git show` |
| Comparar branch | compare commits | fetch both commits | local `git diff` |
| Leer archivo | fetch file at exact ref | blob SHA/content | local checkout |
| Descubrir símbolo | repository search | fetch exact file | local ripgrep |
| Inspeccionar PR | PR metadata + patch | changed filenames | block if required PR detail is unavailable |
| Revisar thread | review threads | reviews/comments | GraphQL script |
| Verificar CI | commit runs + combined status | jobs/steps/logs | block if required run detail is unavailable |
| Descargar artifact | list run artifacts | artifact metadata | block if artifact download action is unavailable |
| Auditar issue | issue + all comments | reactions | block if required issue detail is unavailable |

### 52.8.13 Mapa exacto de acciones Read conocidas

Cuando estas acciones estén expuestas en la sesión, usar sus nombres y contratos exactos:

#### Repository, identity and installations

```text
get_repo
get_profile
get_user_login
get_repo_collaborator_permission
list_installations
list_installed_accounts
list_repositories
list_repositories_by_affiliation
list_repositories_by_installation
list_user_org_memberships
list_user_orgs
search_repositories
search_installed_repositories_streaming
search_installed_repositories_v2
```

#### Refs, commits and comparison

```text
compare_commits
fetch_commit
search_branches
search_commits
```

#### Files and blobs

```text
fetch
fetch_file
fetch_blob
search
```

#### Issues

```text
fetch_issue
fetch_issue_comments
list_recent_issues
search_issues
get_issue_comment_reactions
```

#### Pull requests and reviews

```text
get_pr_info
fetch_pr
fetch_pr_comments
list_pr_changed_filenames
fetch_pr_file_patch
fetch_pr_patch
get_pr_diff
get_users_recent_prs_in_repo
list_pull_request_review_threads
list_pull_request_reviews
get_pr_reactions
get_pr_review_comment_reactions
search_prs
```

#### GitHub Actions and artifacts

```text
fetch_commit_workflow_runs
get_commit_combined_status
fetch_workflow_run_jobs
fetch_workflow_job_steps
fetch_workflow_job_logs
fetch_workflow_run_artifacts
download_workflow_artifact
```

#### Private attachments

```text
download_user_content
```

Esta lista registra acciones conocidas, pero no reemplaza capability discovery. La sesión puede agregar, retirar o cambiar cobertura.

### 52.8.14 Capacidades documentadas pero no necesariamente cargadas

El usuario puede aportar documentación de acciones que no estén visibles en la sesión actual, por ejemplo:

```text
check repository setup
get GitHub App installation ID for repository
list commits dedicated action
list repository directory
resolve ref to exact SHA
fetch raw commit diff/patch dedicated action
mfetch link following
synced RAG semantic search
```

Tratamiento:

1. buscar primero una acción exacta cargada con ese propósito;
2. si no existe, mapear a una alternativa segura;
3. registrar que se usó equivalencia, no la acción original;
4. no inventar el nombre ni el schema de una función ausente.

Equivalencias habituales:

| Capacidad documentada | Equivalencia cuando la acción no está cargada |
|---|---|
| Check repository setup | `get_repo` + clasificación de error/instalación |
| Installation ID for repo | `list_installations` + `list_repositories_by_installation` |
| List commits | `search_commits` con query vacía y repo exacto |
| List directory | fetch/list action si aparece; de lo contrario search + exact fetch, sin afirmar completitud |
| Resolve ref | branch search + exact commit fetch; block if canonical resolution is unavailable |
| Raw commit diff | diff incluido por `fetch_commit`, compare o local Git |
| mfetch | usar solo para seguir el documento/URL devuelto, no como source of truth Git |
| Synced RAG | discovery semántico seguido de fetch exacto por path/ref |

No degradar una necesidad de evidencia completa a una equivalencia incompleta sin declararlo.
