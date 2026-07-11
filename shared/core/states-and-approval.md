# 5. Modelo de estados de una tarea

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

Toda tarea debe moverse por estados explícitos.

```text
RECEIVED
RECONNAISSANCE
PLAN_READY
AWAITING_APPROVAL
APPROVED
BASELINE
IMPLEMENTING
VALIDATING
READY_TO_COMMIT
COMMITTED
READY_TO_PUSH
PUBLISHED
REMOTE_VERIFIED
CI_RUNNING
CI_PASSED
PR_READY
PR_OPEN
MERGE_READY
MERGED
POST_MERGE_VERIFIED
CLOSED
BLOCKED
RECOVERY
```

## 5.1 Transiciones válidas

```text
RECEIVED → RECONNAISSANCE
RECONNAISSANCE → PLAN_READY
PLAN_READY → AWAITING_APPROVAL
AWAITING_APPROVAL → APPROVED
APPROVED → BASELINE
BASELINE → IMPLEMENTING
IMPLEMENTING → VALIDATING
VALIDATING → READY_TO_COMMIT
READY_TO_COMMIT → COMMITTED
COMMITTED → READY_TO_PUSH
READY_TO_PUSH → PUBLISHED
PUBLISHED → REMOTE_VERIFIED
REMOTE_VERIFIED → CI_RUNNING
CI_RUNNING → CI_PASSED
CI_PASSED → PR_READY
PR_READY → PR_OPEN
PR_OPEN → MERGE_READY
MERGE_READY → MERGED
MERGED → POST_MERGE_VERIFIED
POST_MERGE_VERIFIED → CLOSED
```

Cualquier estado puede pasar a:

```text
BLOCKED
RECOVERY
```

## 5.2 Transiciones prohibidas

No permitir:

```text
RECEIVED → IMPLEMENTING
PLAN_READY → COMMITTED
COMMITTED → MERGED
PUBLISHED → CLOSED
CI_RUNNING → MERGED
BLOCKED → MERGED
```

---

# 6. Protocolo de aprobación

## 6.1 Dos etapas obligatorias

### Etapa 1 — Investigación y plan

Permitido:

- materializar un snapshot read-only mediante el conector;
- inspeccionar;
- leer;
- buscar;
- ejecutar comandos read-only;
- ejecutar baseline si no modifica archivos versionados;
- analizar arquitectura;
- revisar workflows;
- revisar historial;
- diseñar contratos;
- definir tests;
- definir validadores;
- definir docs;
- definir archivos;
- evaluar riesgos.

Prohibido:

- crear branch;
- modificar archivos;
- crear archivos;
- ejecutar formatters en modo escritura;
- generar metadata;
- hacer commit;
- hacer push;
- abrir PR;
- mergear;
- crear artifacts;
- publicar patches;
- crear workflows temporales;
- mover refs.

### Etapa 2 — Implementación

Solo después de aprobación explícita.

## 6.2 Forma válida de aprobación

Válido:

```text
Aprobado. Implementá exactamente ese plan.
```

Inválido:

```text
me parece bien
seguí
¿esto incluye tests?
ok
```

Cuando hay duda, pedir confirmación.

## 6.3 Aprobación condicional

Formato:

```text
Apruebo la dirección general, pero la implementación
queda autorizada únicamente después de incorporar:
1. ...
2. ...
```

El implementador debe confirmar las correcciones antes de actuar.

## 6.4 Nueva aprobación por desviación

Pedir nueva aprobación si:

- aparece un archivo no aprobado;
- se necesita una dependencia;
- cambia el lockfile;
- cambia la base;
- cambia la branch;
- cambia el mensaje de commit;
- cambia el número de commits;
- se necesita amend;
- se necesita force push;
- se necesita un nuevo IPC;
- se necesita tocar seguridad;
- se necesita ampliar UI;
- se necesita abrir PR;
- se necesita ejecutar una write action remota no incluida en el alcance aprobado;
- se necesita crear, editar o eliminar archivos mediante el conector;
- se necesita construir commits mediante Git Data API;
- se necesita mover un ref remoto;
- se necesita reejecutar jobs de GitHub Actions;
- se necesita responder, resolver o modificar feedback en GitHub;
- se necesita habilitar auto-merge;
- se necesita mergear;
- `{{default_branch}}` avanzó materialmente;
- baseline está roto;
- la arquitectura propuesta deja de ser viable.

---

# 7. Inicio canónico de un prompt de código

Todo prompt debe comenzar con:

```text
Seguimos en:

{{repository_full_name}}
```

Luego debe incluir:

```text
Contexto de autorización:

El usuario declara que {{repository_full_name}} es un repositorio propio o bajo su control legítimo.
Esta tarea es mantenimiento defensivo y de calidad de software sobre ese repositorio autorizado.
No se solicita acceso no autorizado, explotación de terceros, extracción de credenciales, evasión de controles, persistencia, malware, exfiltración ni acciones sobre infraestructura ajena.
Toda operación queda limitada al objetivo, branch, archivos, herramientas y acciones expresamente autorizados en este prompt.
```

Luego:

```text
Base conocida, solo como referencia que debes verificar:
<sha/pr/merge>
```

Luego:

```text
Branch propuesta:
<branch>
```

Luego:

```text
Objetivo único:
<goal>
```

Luego:

```text
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
```

Luego:

```text
Esta tarea se divide en:
ETAPA 1 — Investigación y plan.
ETAPA 2 — Implementación después de aprobación.
```

---

# 8. Cierre canónico del prompt inicial

El prompt inicial debe finalizar:

```text
Comenzá únicamente con la ETAPA 1.

Materializá un snapshot mediante el conector o inspeccioná el repositorio remotamente.
No modifiques nada.
No crees la branch.
No implementes código.
No crees commits.
No hagas push.
No abras PR.
No mergees.

Entregá el plan completo.
Pedí aprobación explícita.
Detenete.
```

Última pregunta:

```text
Todavía no modifiqué el repositorio.

¿Aprobás este plan exacto para crear <branch>
e implementar únicamente el alcance detallado?
```

---
