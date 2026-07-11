### 52.9.10 Contents API: crear, reemplazar y eliminar archivos

Acciones:

```text
create_file
update_file
delete_file
```

Estas acciones escriben archivos mediante GitHub Contents API y crean commits remotos.

#### `create_file`

- Crea un archivo UTF-8 completo.
- La branch debe existir; la acción no crea la branch.
- Si `branch` se omite, puede escribir sobre la default branch. En el repositorio objetivo esto está prohibido salvo autorización explícita excepcional.
- Verificar antes que el path no exista en el ref target.
- La respuesta devuelve el commit SHA resultante, no el payload completo de content/commit. Releer el archivo y el commit para verificación independiente.

#### `update_file`

- Reemplaza el contenido UTF-8 completo.
- Requiere el blob/content SHA actual del archivo, normalmente obtenido con `fetch_file`.
- El `sha` funciona como control de versión del contenido; si cambió, no reintentar con un SHA nuevo sin revalidar el diff.
- Devuelve commit SHA y content blob SHA. Usar el nuevo `content_sha` para una actualización secuencial posterior.

#### `delete_file`

- Requiere el blob SHA actual.
- Elimina un path completo mediante un commit remoto.
- Verificar que el archivo está dentro del alcance y que no es generado/owned por otra fuente.
- La respuesta devuelve el commit SHA resultante; verificar luego ausencia del path y contenido del commit.

#### Reglas de concurrencia

- No ejecutar update/delete en paralelo sobre el mismo path.
- No ejecutar múltiples writes dependientes contra una branch mutable sin volver a resolver head.
- Cada operación suele crear su propio commit; no usar Contents API para una microfase multiarchivo que exige un único commit atómico.
- No usar `create_file`/`update_file` como sustituto silencioso de stage + commit.
- No editar `{{default_branch}}` directamente.

Uso aceptable en el repositorio objetivo:

```text
small isolated text fix
single-file emergency correction
explicit connector-native operation
branch already created
local or fixture validation possible
post-write remote verification
```

Uso no aceptable por defecto:

```text
large implementation
many files
lockfile changes
binary outputs
metadata generated across files
workflow rewrites without local validation
sequential commits that violate one-commit microphase
```

### 52.9.11 Git Data API: blobs, trees, commits y refs

Acciones:

```text
create_blob
create_tree
create_commit
create_branch
update_ref
```

Estas acciones permiten construir objetos Git remotos sin `git push`. Constituyen una vía válida pero sensible. No crean un checkout local y no ejecutan tests.

#### Modelo de objetos

```text
file bytes
→ create_blob
→ blob SHA

base tree + tree entries
→ create_tree
→ tree SHA

tree SHA + parent commit SHA + message
→ create_commit
→ commit SHA

commit SHA
→ create_branch or update_ref
→ published branch head
```

#### `create_blob`

- Usar `utf-8` para texto.
- Usar `base64` solo para bytes binarios reales.
- No versionar Base64 como contenido textual de transporte.
- Registrar path lógico, encoding, byte length y blob SHA.

#### `create_tree`

- Para modificar un tree existente, usar `base_tree_sha` exacto.
- Cada elemento debe definir correctamente path, mode, type y SHA/content conforme al schema expuesto.
- No crear tree “desde cero” para una modificación parcial salvo que se haya reconstruido el tree completo de forma verificable.
- Verificar que paths eliminados, renombrados y symlinks estén representados correctamente.

#### `create_commit`

- Requiere `tree_sha` y `parent_sha` exactos.
- `additional_parent_shas` solo corresponde a commits multi-parent deliberados. No crear merges artificiales.
- Crear el commit object no publica la branch.
- Verificar el commit resultante con `fetch_commit` antes de mover un ref cuando sea posible.

#### `create_branch`

- Debe recibir exactamente uno de `sha` o `base_ref`.
- Para una branch nueva de trabajo, preferir un SHA base exacto.
- No usar una branch mutable como base si el plan requiere reproducibilidad y ya se conoce el SHA.
- Verificar que el nombre cumple la convención aprobada y que no existe una branch conflictiva.

#### `update_ref`

- Mueve el head de una branch al commit dado.
- `force` debe ser `false` por defecto.
- `force=true` está prohibido salvo autorización explícita, SHA remoto esperado, justificación de recuperación y ausencia de alternativa segura.
- Resolver el head actual inmediatamente antes de mover el ref.
- La acción no expone necesariamente compare-and-swap por old SHA; por eso existe riesgo de carrera. Si otro actor movió la branch, detener y reconstruir el commit sobre la nueva base.

### 52.9.12 Publicación connector-native atómica

Usar esta ruta solo cuando:

- la publicación remota debe realizarse mediante Git Data API del conector;
- el conector expone las acciones Git Data necesarias;
- el source exacto fue materializado o el cambio es completamente conocido;
- las validaciones locales relevantes se ejecutaron sobre el tree que se publicará;
- el usuario aprobó explícitamente esta estrategia;
- se requiere un único commit multiarchivo coherente.

Procedimiento:

```text
1. Resolve target repository.
2. Resolve exact base branch head SHA.
3. Fetch base commit and base tree SHA.
4. Confirm branch strategy and expected parent.
5. Produce final file bytes locally.
6. Run relevant local validation against those bytes.
7. Create one blob per changed/new file.
8. Build one tree from exact base_tree_sha.
9. Create one commit with exact parent_sha.
10. Fetch and inspect the created commit.
11. Create new branch at commit SHA, or fast-forward approved branch with update_ref(force=false).
12. Re-fetch branch head.
13. Compare base SHA against published commit.
14. Verify changed file list and stats.
15. Discover CI from the published SHA.
```

Pre-publication manifest:

```text
base commit SHA
base tree SHA
branch name
commit message
expected parent count
file action: add/modify/delete/rename
path
mode/type
old blob SHA
new blob SHA
local checksum
validation commands
```

Abortar si:

- base branch cambió;
- branch target apareció inesperadamente;
- un path no coincide;
- no puede determinarse el base tree;
- hay binaries/symlinks/submodules no representados correctamente;
- el tree creado contiene scope extra;
- la validación se ejecutó sobre bytes distintos;
- el commit parent no coincide;
- se requeriría `force=true` no autorizado.

Esta ruta puede sustituir técnicamente el push de un commit preparado, pero no sustituye clone, checkout, build ni tests.

### 52.9.13 Rerun de GitHub Actions

Acciones:

```text
rerun_failed_workflow_run_jobs
rerun_workflow_job
```

Requisitos:

- Actions write permission;
- run/job ID exacto;
- estado actual leído;
- root cause o hipótesis documentada;
- autorización explícita para rerun.

No rerun ciego.

Usar `rerun_failed_workflow_run_jobs` cuando:

- se desea reejecutar solo los jobs fallidos del run;
- los exitosos no necesitan repetición;
- el fallo puede ser transitorio o ya se corrigió una dependencia externa.

Usar `rerun_workflow_job` cuando:

- existe un job específico failed/cancelled;
- reejecutar todos los fallidos sería innecesario;
- el job puede ejecutarse aisladamente según GitHub.

Antes:

```text
fetch run/jobs/steps/logs
→ identify failure
→ distinguish deterministic failure vs flake/infrastructure
→ verify no new commit is required
```

Después:

```text
resolve latest attempt
→ observe terminal state
→ fetch jobs/steps/logs
→ report whether failure reproduced
```

Si el fallo es determinista en el código, corregir y publicar un SHA nuevo en lugar de usar rerun como bypass.

### 52.9.14 Merge y auto-merge

Acciones:

```text
enable_auto_merge
merge_pull_request
```

#### Auto-merge

`enable_auto_merge` infiere el método según settings del repositorio y puede devolver solo `success`.

Antes:

- verificar que el repositorio permite auto-merge;
- verificar PR abierto;
- verificar expected head SHA;
- verificar reviews/checks requeridos;
- confirmar que el usuario desea auto-merge, no merge inmediato.

Después:

- recuperar PR;
- confirmar auto-merge state si la respuesta lo expone;
- no afirmar método exacto si la acción no lo devuelve.

#### Merge inmediato

`merge_pull_request` puede aceptar:

```text
merge method
commit title
commit message
expected head SHA
```

Gates críticos:

```text
explicit merge authorization
PR open and not draft
head SHA unchanged
base branch correct
mergeable state acceptable
required CI terminal and green
no unresolved BLOCKER/MAJOR
no unresolved required review
final diff audited
no branch contamination
```

Usar siempre `expected_head_sha` cuando la acción lo permita. Si el head cambió, GitHub debe rechazar la operación y el agente debe volver a revisar; no reintentar automáticamente.

Después del merge:

```text
verify merged=true
record merge SHA
fetch merge commit
verify default branch head or containment
observe post-merge CI when required
update roadmap/docs state
clean branch only if separately authorized
```

No habilitar auto-merge ni mergear como consecuencia implícita de “publicá” o “abrí PR”.
