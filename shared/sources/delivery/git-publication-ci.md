# 26. Documentación

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

## 26.1 Documentación mínima por fase

- status;
- purpose;
- implemented;
- blocked;
- future;
- ownership;
- data flow;
- key files;
- boundaries;
- tests;
- validator;
- related docs;
- read next.

## 26.2 Roadmap

Actualizar:

- phase status;
- covered;
- blocked;
- next module;
- dependencies;
- completion criteria.

No dejar una fase ya integrada como “future”.

## 26.3 Guided reading

Mantener:

```text
Start here
Before this
Next
Related
Why this matters
```

## 26.4 ADR

Crear ADR cuando:

- cambia boundary;
- cambia ownership;
- cambia persistence model;
- cambia IPC authority;
- cambia source of truth;
- cambia strategy irreversible.

No crear ADR para una implementación trivial.

---

# 27. Review del diff

Antes de stage:

```bash
git status --short
git diff --stat
git diff --check
git diff --name-only
```

Después de stage:

```bash
git diff --cached --stat
git diff --cached --check
git diff --cached --name-only
```

Buscar:

```text
publish-
diagnostic-
.b64
run-id
validation-verbose
tmp
backup
secret
token
password
```

Revisar:

- lockfile;
- workflow;
- package.json;
- IPC;
- docs;
- validators;
- tests;
- generated files.

---

# 28. Commit

## 28.1 Regla por defecto

```text
Un commit por microfase.
```

## 28.2 Mensaje exacto

Debe definirse en el prompt.

## 28.3 Verificación

```bash
git show -s --format="%H%n%P%n%T%n%aI%n%cI%n%an <%ae>%n%cn <%ce>%n%B" HEAD
git status --short
git rev-list --count origin/{{default_branch}}..HEAD
git diff origin/{{default_branch}}...HEAD --stat
git diff origin/{{default_branch}}...HEAD --check
git diff origin/{{default_branch}}...HEAD --name-only
```

## 28.4 Prohibiciones

- no amend sin aprobación;
- no rebase;
- no squash;
- no force;
- no reset destructivo;
- no filter-repo;
- no alterar commits históricos.

---

# 29. Publicación remota mediante conector

La publicación remota se ejecuta mediante acciones del conector. El workspace y los commits locales sirven para edición y validación, pero no son un transporte remoto.

## 29.1 Prerrequisitos

Requerir:

```text
COMPLETE_LOCAL_WORKSPACE_OR_VERIFIED_SOURCE_SNAPSHOT
intended diff confirmed
working tree understood
remote branch and parent SHA confirmed through connector
local validation commit optional
connector publication capability confirmed
# GitHub authentication and access are resolved through the connector; do not use gh.
remote target verified
```

Antes:

```bash
git status --short
git diff --cached --check
# GitHub remote refresh: resolve refs and commits through the connector; do not use git fetch.
git merge-base --is-ancestor origin/{{default_branch}} HEAD
```

Si `fetch` falla por DNS o red:

- no intentar `push` a ciegas;
- no afirmar que la branch está actualizada;
- no reemplazar silenciosamente el flujo por escrituras file-by-file del conector;
- cambiar el estado a `BLOCKED` o solicitar una estrategia alternativa explícita.

## 29.2 Push normal

```bash
# GitHub remote publication: use connector Git Data API or connector write actions; do not use git push.
```

Después del push, verificar la branch y el commit con el conector, no solo con la salida del comando.

Si el prompt exige verificar GitHub Actions:

- no pedir al usuario el enlace del run;
- resolver CI desde el SHA publicado;
- aplicar el protocolo de la sección 31;
- observar el run hasta estado terminal dentro de la ejecución actual cuando la cobertura de herramientas lo permita;
- no cerrar la tarea como exitosa con CI pendiente o no vinculada al SHA final.

## 29.3 Escritura remota mediante conector

Las operaciones de contenido del conector pueden crear o reemplazar archivos y crear commits remotos, pero no son un sustituto general del flujo local.

Solo usarlas si:

- el usuario autorizó expresamente esa estrategia;
- el cambio es pequeño y text-only;
- se conoce el blob SHA actual;
- no se requiere atomicidad multi-file;
- no se requiere ejecutar tests sobre el tree final antes de publicar;
- se entiende que varias escrituras pueden producir varios commits.

No usar por defecto para:

- cambios multi-file;
- lockfiles;
- binarios;
- archivos generados;
- refactors;
- cambios que requieren build;
- cambios que deben quedar en un único commit;
- recuperación de un working tree completo.

Las operaciones low-level de commit, tree o ref son último recurso de recuperación y requieren autorización específica.

## 29.4 Force-with-lease

Solo con autorización explícita y SHA verificado:

```bash
# GitHub remote publication: use connector Git Data API or connector write actions; do not use git push.
  --force-with-lease=refs/heads/<branch>:<remote-sha> \
  origin HEAD:refs/heads/<branch>
```

Nunca:

```bash
# GitHub remote publication: use connector Git Data API or connector write actions; do not use git push.
```

---

# 30. Verificación remota connector-first

Después de publicar, usar el conector como fuente remota independiente del checkout local.

Verificar:

1. El commit existe.
2. La branch apunta al commit.
3. Parent y tree son los esperados.
4. Mensaje, author y committer son correctos.
5. La comparación con `{{default_branch}}` tiene el ahead count esperado.
6. La lista de archivos coincide con el alcance.
7. No existen artifacts operativos o archivos prohibidos.
8. El PR, si existe, apunta a head y base correctos.
9. Los checks o workflow runs pertenecen al SHA final.
10. La branch no se movió durante la verificación.

Preferir capacidades estructuradas del conector:

```text
fetch commit
compare commits
search branch
fetch branch head
fetch commit workflow runs by exact SHA
combined commit status and individual checks
workflow run jobs, steps, logs and artifacts
PR metadata, head SHA and patch
```

Criterio:

```text
commit exists
branch points to commit
parent and tree match
ahead count correct
file list correct
remote SHA stable
CI belongs to final SHA
```

Si local Git y conector discrepan:

```text
STOP-THE-LINE
```

El remoto verificable prevalece sobre el reporte local.

---

# 31. GitHub Actions y CI

## 31.1 Modelo connector-only sin fallback de red local

GitHub Actions debe investigarse desde el SHA exacto, no desde un enlace aportado manualmente.

Orden:

```text
connector Actions/read actions
→ connector combined status
→ block uncovered connector gaps
→ user-provided URL only as last disambiguation input
```

No asumir una lista fija basada en una versión anterior. Descubrir si la sesión expone:

```text
fetch commit workflow runs
get combined commit status
fetch run jobs
fetch job steps
fetch job logs
fetch run artifacts
download workflow artifact
rerun failed jobs
rerun one job
```

Cuando existe la función y su cobertura es suficiente, usarla. Cuando la cobertura sea parcial, registrar el gap y detener la parte no cubierta; no usar `gh` para completarla.

## 31.2 Limitaciones contractuales conocidas

Mantener explícitas:

```text
fetch_commit_workflow_runs:
- exact commit SHA input
- pull_request-triggered runs only
- first page only

fetch_workflow_run_jobs:
- run ID input
- latest attempt
- first page only

fetch_workflow_run_artifacts:
- run ID input
- first page only

fetch_workflow_job_steps:
- step summaries, not full logs

fetch_workflow_job_logs:
- decoded job logs

get_commit_combined_status:
- aggregate/check status
- may include external checks
- does not replace causal logs
```

No afirmar “no hubo workflow” únicamente porque `fetch_commit_workflow_runs` devolvió cero resultados. El commit puede tener:

- workflow disparado por `push`;
- run fuera de la primera página;
- check externo;
- run todavía no indexado;
- permisos insuficientes.

## 31.3 Requisitos de workflow

- actions pinneadas según política del proyecto;
- permisos mínimos;
- no credentials persistentes;
- no workspace upload indiscriminado;
- no `pull_request_target` para ejecutar código no confiable;
- no recursion dependiente de `GITHUB_TOKEN`;
- no workflow temporal en el commit final;
- artifacts limitados al objetivo;
- logs sin secretos.

## 31.4 Identidad canónica de una verificación CI

Toda verificación debe registrar:

```text
repository
final commit SHA
branch
PR number, si aplica
workflow/run ID
workflow name
event
attempt
run status
run conclusion
job ID
job name
step number/name
artifact IDs, si aplican
```

No aceptar un run sin confirmar:

```text
run.headSha == final commit SHA
```

Cuando el evento es `pull_request`, verificar también que el PR head actual siga apuntando al SHA esperado o entender la semántica de merge ref usada por el workflow.

## 31.5 Descubrimiento automático después de un push

Cuando el prompt exige publicar y verificar CI, el agente no debe detenerse después de la publicación connector-native ni pedir al usuario el enlace del workflow.

Procedimiento obligatorio:

1. Capturar el SHA local publicado.
2. Verificar con el conector que el commit existe.
3. Verificar que la branch remota apunta al SHA.
4. Consultar combined status para el SHA.
5. Consultar workflow runs asociados al SHA.
6. Si existe PR, verificar metadata/head SHA y priorizar runs `pull_request` del PR correcto.
7. Seleccionar el run cuya identidad coincida con SHA, branch, event y workflow esperado.
8. Continuar observando el run hasta estado terminal.
9. Recuperar jobs y steps.
10. Si falla, recuperar logs del job causal y artifacts relevantes.
11. Entregar el resultado solicitado con evidencia y limitaciones.

Estados de observación:

```text
CI_DISCOVERY_PENDING
CI_RUN_QUEUED
CI_RUN_IN_PROGRESS
CI_TERMINAL_SUCCESS
CI_TERMINAL_FAILURE
CI_TERMINAL_CANCELLED
CI_TERMINAL_SKIPPED
CI_NO_MATCHING_RUN_YET
CI_NOT_DISCOVERABLE_WITH_CONNECTOR
CI_PARTIALLY_VERIFIED
```

## 31.6 Polling síncrono y acotado

“Esperar a que termine” significa observar dentro de la ejecución actual. No significa prometer una respuesta futura ni ejecutar trabajo en background.

Polling:

```text
resolve final SHA once
→ query status/runs
→ if queued/in_progress, poll same run ID
→ stop only at terminal state or execution/tool boundary
```

Reglas:

- usar backoff razonable y no saturar el conector;
- no cambiar de run ID sin justificar por qué;
- si aparece un nuevo attempt, registrar el cambio;
- emitir actualizaciones breves al usuario durante observaciones largas;
- no declarar éxito mientras el run siga queued/in_progress;
- si la sesión termina antes del estado terminal, informar estado actual exacto y no afirmar CI completa;
- no crear una automatización salvo que el usuario la solicite.

El polling debe finalizar cuando:

```text
status/conclusion is terminal
or
run identity becomes invalid because branch/PR head moved
or
tool/session no longer permits observation
```

## 31.7 Ruta connector-first para PR-triggered workflows

Cuando el CI se dispara por PR:

1. Resolver repo y PR.
2. Recuperar head SHA actual.
3. Usar `fetch_commit_workflow_runs(final SHA)`.
4. Filtrar por exact head SHA y workflow esperado.
5. Recuperar jobs del run seleccionado.
6. Reconsultar hasta que todos los jobs relevantes estén terminales.
7. Recuperar steps para localizar el primer step fallido.
8. Recuperar logs decodificados del job fallido.
9. Recuperar artifacts solo si ayudan al diagnóstico o son parte del entregable.
10. Verificar combined status como control cruzado.

Si hay múltiples runs válidos:

- preferir el intento más reciente del workflow requerido;
- distinguir reruns de workflows distintos;
- no mezclar jobs de runs diferentes;
- reportar workflows opcionales/required por separado cuando esa información esté disponible.

## 31.8 Ruta para push-only workflows o cobertura incompleta

Debido a que `fetch_commit_workflow_runs` puede filtrar solo `pull_request`, para CI disparado por `push`:

1. Consultar `get_commit_combined_status(final SHA)`.
2. Identificar checks asociados y sus estados/URLs si están presentes.
3. Intentar cualquier acción connector-native de run discovery adicional expuesta en la sesión.
4. Si no puede resolverse run/job/log mediante el conector, informar la cobertura insuficiente y detener esa verificación.
5. No pedir el link al usuario salvo que el conector sea insuficiente y exista ambigüedad real que el usuario deba resolver.

Cobertura insuficiente del conector:

```bash
# No GitHub CLI network path: use the connector session.
# GitHub authentication and access are resolved through the connector; do not use gh.
# Pull request access: use the connector; do not use gh pr.
# GitHub Actions access: use the connector; do not use gh run.
# GitHub Actions access: use the connector; do not use gh run.
# GitHub Actions access: use the connector; do not use gh run.
# GitHub API access: use the connector; do not use gh api.
```

Si el conector no expone la capacidad necesaria:

- conservar evidencia obtenida por el conector;
- marcar `CI_NOT_DISCOVERABLE_WITH_CONNECTOR` o `CI_PARTIALLY_VERIFIED`;
- explicar exactamente qué campo falta;
- no inventar run ID, jobs ni logs.

## 31.9 Inspección causal de fallos

Para cada run fallido:

```text
run
→ jobs
→ failing job
→ steps
→ first causal failing step
→ logs around failure
→ artifact if needed
```

Separar:

```text
root cause
propagated failure
cleanup failure
artifact upload result
cancelled dependents
```

No usar exclusivamente la última línea del log.

El reporte debe incluir:

- workflow/check name;
- run ID y URL canónica cuando estén disponibles;
- final SHA;
- event;
- status/conclusion;
- failing job;
- first causal step;
- extracto breve y suficiente del log;
- diagnóstico con nivel de confianza;
- si el fallo pertenece o no al diff local;
- artifacts inspeccionados;
- elementos no verificados.

## 31.10 Artifacts de CI

Cuando sean relevantes:

1. Listar artifacts del run.
2. Filtrar por nombre esperado.
3. Confirmar artifact ID y run ID.
4. Descargar ZIP mediante el conector.
5. Inspeccionar en workspace separado.
6. Verificar manifest/digest si existe.
7. No ejecutar binarios no confiables.
8. No tratar el artifact como sustituto del commit.

Registrar limitación first-page-only. Si el artifact esperado no aparece y la lista puede estar truncada, usar fallback antes de concluir ausencia.

## 31.11 Reruns

No rerun ciego.

Antes de rerun:

- diagnosticar causa;
- decidir si es flaky, infraestructura o código;
- verificar que el SHA siga siendo el final;
- obtener autorización explícita, porque rerun es write action.

Preferir:

```text
rerun one failed job
```

cuando el fallo esté aislado y la API lo permita.

Usar rerun de todos los failed jobs solo cuando sea necesario.

Después del rerun:

- capturar attempt nuevo;
- volver a observar hasta terminal;
- no mezclar logs del attempt anterior;
- informar si pasó sin cambios de código y por qué se considera flaky o transitorio.

## 31.12 CI correcto

CI final es válida solo si:

```text
remote branch points to final SHA
+ run/check belongs to final SHA
+ required workflows are identified sufficiently
+ terminal status observed
+ failures have causal logs when available
```

No aceptar:

```text
run de branch auxiliar
run de commit previo
run 404
run con headSha distinto
run de otro event no equivalente
artifact de otro attempt
combined status pending presentado como success
status agregado sin logs cuando hay fallo
run no terminal
link narrado sin verificación
```

## 31.13 Resultado después de publicación

Cuando el prompt solicita verificar el workflow, el reporte final debe incluir:

```text
Published SHA
Remote branch head
PR head, si aplica
Workflow/check discovery method
Run ID / URL
Event
Attempt
Status
Conclusion
Jobs summary
First failing step, si aplica
Log evidence, si aplica
Artifacts, si aplica
Coverage limitations
Final CI classification
```

Clasificación final:

```text
CI_VERIFIED_PASS
CI_VERIFIED_FAIL
CI_VERIFIED_CANCELLED
CI_STILL_RUNNING
CI_PARTIAL_CONNECTOR_COVERAGE
CI_UNVERIFIED
```

---
