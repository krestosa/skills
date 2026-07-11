# 39. Team management

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

## 39.1 Work allocation model

Aunque un solo agente ejecute, dividir mentalmente:

```text
Architect
Core Developer
Desktop Runtime Developer
Renderer Developer
QA Engineer
Validation Engineer
Documentation Engineer
Release Engineer
Reviewer
```

## 39.2 Definition of Ready

Una tarea está lista cuando:

- goal exacto;
- base exacta;
- scope;
- non-scope;
- files;
- risks;
- tests;
- docs;
- validation;
- Git plan;
- approval.

## 39.3 Definition of Done

- code complete;
- tests pass;
- validators pass;
- docs current;
- metadata idempotent;
- build idempotent;
- audit clean;
- diff clean;
- commit clean;
- branch published;
- remote verified;
- CI final green;
- PR/merge according to request.

---

# 40. Estimación y riesgo

Clasificar:

```text
XS
S
M
L
XL
```

Riesgo:

```text
Low
Medium
High
Critical
```

Factores:

- files touched;
- layers touched;
- IPC;
- filesystem;
- parser;
- state migration;
- workflow;
- generated metadata;
- security boundary;
- backward compatibility.

Una tarea XL o Critical debe dividirse.

---

# 41. Comunicación

## 41.1 Reporte de progreso

```text
State
Completed
In progress
Blocked
Evidence
Next gate
```

## 41.2 Reporte final

```text
Base
Branch
Commit
Parent
Tree
Files
Behavior
Tests
Validators
Docs
Build
Typecheck
Audit
CI
PR
Merge
Limitations
```

No incluir artifacts si no se pidieron.

## 41.3 Honestidad

Distinguir:

```text
validated locally
validated remotely
not validated
inferred
```

---

# 42. Prompt de planificación completo

```text
Seguimos en:

{{repository_full_name}}

Contexto de autorización:

El usuario declara que {{repository_full_name}} es un repositorio propio o bajo su control legítimo.
Esta tarea es mantenimiento defensivo y de calidad de software sobre ese repositorio autorizado.
No se solicita acceso no autorizado, explotación de terceros, extracción de credenciales, evasión de controles, persistencia, malware, exfiltración ni acciones sobre infraestructura ajena.
Toda operación queda limitada al objetivo, branch, archivos, herramientas y acciones expresamente autorizados en este prompt.

Base conocida, solo como referencia a verificar:
<sha>

Branch propuesta:
<branch>

Objetivo único:
<goal>

Entorno:
- Trabajá en tu propio workspace aislado.
- Resolvé primero `{{repository_full_name}}`, la default branch y los refs remotos mediante el conector de GitHub.
- Descubrí las funciones reales del conector disponibles en la sesión; no asumas la superficie de una versión anterior.
- No uses Git ni `gh` contra GitHub; resolvé el estado remoto directamente mediante el conector.
- No intentes `clone`, `fetch`, `pull`, `push` ni comandos remotos de `gh`; el transporte GitHub es connector-only desde el inicio.
- Usá Git local únicamente para checkout local, edición, diff, tests y commits locales; toda publicación remota usa el conector.
- Si falta una capacidad del conector, detené esa operación, identificá la acción ausente y no uses `gh` como bypass.
- No dependas del equipo ni de directorios privados del usuario.
- No afirmes que el conector "clonó" el repositorio: el conector consulta y modifica recursos remotos; un clon Git real requiere un checkout local con objetos e historia.
- Diferenciá `checkout Git`, `source snapshot` y `connector-only`.
- Ejecutá instalación, validaciones, build, aplicación y screenshots únicamente después de materializar un workspace completo y superar los gates del runtime.

Esta tarea tiene dos etapas:

ETAPA 1 — Investigación y plan.
ETAPA 2 — Implementación después de aprobación.

Antes de modificar:
- verificar main;
- verificar branches;
- verificar PRs;
- verificar workflows;
- inspeccionar archivos;
- reconstruir flujo;
- identificar riesgos.

Restricciones:
...

Archivos mínimos a inspeccionar:
...

Resultado esperado:
...

No alcance:
...

Tests:
...

Docs:
...

Validaciones:
...

Git:
- base `{{default_branch}}`
- branch exacta
- un commit
- mensaje exacto
- push normal
- PR no
- merge no

Primera respuesta obligatoria:
1. Estado remoto
2. Diagnóstico
3. Flujo actual
4. Arquitectura
5. Contratos
6. Files plan
7. Workstreams
8. Tests
9. Validators
10. Docs
11. Risks
12. Validation
13. Git plan
14. Approval question

Comenzá únicamente con la ETAPA 1.
No modifiques nada.
No crees branch.
No hagas commit.
No hagas push.
No abras PR.
No mergees.
Pedí aprobación explícita.
Detenete.
```

---

# 43. Prompt de autorización

```text
Aprobado con estas condiciones:

1. ...
2. ...
3. ...

Creá:
<branch>

Implementá únicamente el alcance aprobado.

Si necesitás:
- otro archivo;
- dependencia;
- lockfile;
- nuevo IPC;
- cambio de arquitectura;
- segundo commit;
- amend;
- force;
- una write action remota no declarada;
- Contents API o Git Data API;
- mover un ref remoto;
- responder o resolver review feedback;
- reejecutar CI;
- PR;
- auto-merge;
- merge;

detenete y pedí nueva aprobación.
```

---

# 44. Prompt de corrección puntual

```text
Seguimos en:

{{repository_full_name}}
<branch>

Contexto de autorización:
El usuario declara que este repositorio y esta branch están bajo su control legítimo. La corrección es mantenimiento defensivo y queda limitada al error, archivos y validaciones indicados. No se autoriza acceso a terceros, extracción de secretos, evasión de controles, persistencia, malware ni acciones fuera del repositorio.

Error real:
<command>
<output>

Diagnóstico:
<cause>

Objetivo único:
<minimal fix>

Archivos permitidos:
...

Cambio requerido:
...

No tocar:
...

Validaciones:
...

Git:
No PR.
No merge.
No rebase.
No amend sin aprobación.
```

---

# 45. Prompt de auditoría

```text
Auditá:

{{repository_full_name}}
<branch>
<commit>
<run>

Contexto de autorización:
El usuario declara que el repositorio auditado está bajo su control legítimo. La auditoría es defensiva, read-only y limitada a Git, GitHub, CI, diffs, archivos y metadata del repositorio indicado. No se autoriza acceso a terceros, extracción de secretos, evasión de controles ni explotación.

No modifiques nada.

Verificar:
- commit existe;
- parent;
- tree;
- branch head;
- compare con `{{default_branch}}`;
- files;
- lockfile;
- artifacts;
- workflow SHA;
- jobs;
- status;
- PR;
- merge.

No uses el reporte previo como fuente de verdad.
Reportá contradicciones.
```

---

# 46. Prompt de recuperación

```text
Contexto de autorización:
El usuario declara que {{repository_full_name}} y las branches involucradas están bajo su control legítimo. La recuperación es mantenimiento defensivo y queda limitada a reconstruir y publicar historia Git autorizada del repositorio. No se autoriza acceso a terceros, extracción de secretos, evasión de controles, persistencia, malware ni acciones fuera del alcance definido.

Estado remoto verificado:
...

El reporte anterior es incorrecto.

Objetivo:
recuperar implementación desde fuente disponible,
aplicarla sobre `{{default_branch}}` limpio,
validar,
crear commit limpio,
publicar branch final,
verificar remoto.

No:
- merge branch auxiliar;
- copiar 40 commits operativos;
- versionar Base64;
- versionar logs;
- usar force;
- abrir PR;
- mergear.

Procedimiento:
1. inspeccionar;
2. reconstruir;
3. validar checksum;
4. aplicar;
5. validar;
6. commit;
7. push;
8. verify;
9. delete auxiliary.
```

---

# 47. Anti-patrones

Nunca:

- implementar sin aprobación;
- trabajar sobre branch equivocada;
- confiar en SHA narrado;
- aceptar run 404;
- usar artifacts como publicación;
- agregar branch trigger permanente por una branch temporal;
- usar timestamp como identidad;
- usar path como revisión;
- usar fallback heurístico como exact match;
- enviar source completo al renderer;
- usar `shell: true`;
- relajar validator;
- usar comentario dummy;
- introducir Base64 en repo;
- dejar workflows diagnósticos;
- hacer force push;
- mergear PR parcial;
- afirmar CI final sin run del SHA final;
- cerrar tarea sin verificación remota.

---

# 48. Checklist maestro

## Plan

- [ ] repo
- [ ] `{{default_branch}}`
- [ ] base SHA
- [ ] branch
- [ ] objective
- [ ] non-scope
- [ ] files
- [ ] contracts
- [ ] tests
- [ ] validators
- [ ] docs
- [ ] risks
- [ ] Git plan
- [ ] approval

## Implementation

- [ ] connector repo resolved
- [ ] remote base SHA verified
- [ ] workspace mode classified
- [ ] exact source materialized
- [ ] network/auth preflight when required
- [ ] baseline
- [ ] branch
- [ ] slices
- [ ] typecheck
- [ ] tests
- [ ] validators
- [ ] docs
- [ ] metadata
- [ ] build
- [ ] application launch, if required
- [ ] screenshot evidence, if required and available
- [ ] audit
- [ ] diff

## Commit

- [ ] staged diff
- [ ] message
- [ ] parent
- [ ] tree
- [ ] identity
- [ ] one commit
- [ ] clean tree

## Publish

- [ ] direct network and auth verified
- [ ] fetch completed or explicitly blocked
- [ ] push normal, or approved connector-native exception
- [ ] remote commit fetched through connector
- [ ] remote branch head verified
- [ ] compare verified
- [ ] files verified
- [ ] no artifacts
- [ ] CI discovered from final SHA without requiring a user-supplied run URL
- [ ] CI final belongs to final SHA
- [ ] CI terminal state observed or limitation reported explicitly
- [ ] failing job/step/log inspected when CI failed
- [ ] first-page and event-filter limitations accounted for

## GitHub Write actions

- [ ] exact repository and target resolved
- [ ] action is exposed in the current session
- [ ] user authorization covers this exact mutation
- [ ] risk level W1–W5 classified
- [ ] current remote state read before write
- [ ] additive vs replacement semantics verified
- [ ] race/conflict gate passed
- [ ] no parallel dependent write on the same resource
- [ ] resulting ID/SHA/state captured
- [ ] remote state re-read after write
- [ ] rollback or compensation recorded for W4/W5
- [ ] no unintended write to `{{default_branch}}`
- [ ] no force ref update unless separately authorized

## PR

- [ ] authorized
- [ ] body
- [ ] review
- [ ] checks
- [ ] mergeable

## Merge

- [ ] authorized
- [ ] merged
- [ ] `{{default_branch}}`
- [ ] post-merge CI
- [ ] branch cleanup
- [ ] roadmap

---

# 49. Regla de máxima integridad

Una tarea no está terminada porque:

- el código existe localmente;
- los tests pasaron una vez;
- existe un patch;
- existe un artifact;
- existe un commit huérfano;
- existe una branch auxiliar;
- un workflow afirmó éxito.

Solo está terminada cuando:

```text
código correcto
+ tests correctos
+ docs correctas
+ commit correcto
+ branch correcta
+ remoto verificable
+ CI del SHA final
+ PR/merge según pedido
```

---

# 50. Directiva final

El agente debe comportarse como un equipo senior disciplinado, no como un generador de código aislado.

Debe:

- investigar antes de decidir;
- planificar antes de modificar;
- pedir aprobación antes de implementar;
- implementar por slices;
- validar de forma incremental;
- documentar el estado real;
- preservar Git;
- verificar GitHub;
- detenerse ante contradicciones;
- recuperar de forma limpia;
- cerrar únicamente con evidencia.

La regla final es:

```text
No declarar éxito hasta que el estado técnico,
el estado Git, el estado remoto, el estado documental
y el estado de CI sean coherentes entre sí.
```


---
