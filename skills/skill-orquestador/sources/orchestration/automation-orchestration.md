# 79. Gestión de cambios incompatibles

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

## 79.1 API migration

```text
introduce new
adapt old
migrate consumers
deprecate
remove
```

## 79.2 Compatibility window

Definir si existe.

## 79.3 Schema evolution

Usar `schemaVersion`.

## 79.4 Removal

No eliminar contrato sin:

- grep consumers;
- tests;
- docs;
- migration.

---

# 80. Automation engineering

## 80.1 Scripts

Un script debe:

- tener CLI estricta;
- help;
- exit codes;
- no shell injection;
- idempotence;
- dry-run si es destructivo;
- errores claros;
- cleanup.

## 80.2 Destructive commands

Requerir:

- preview;
- explicit confirmation;
- repository verification;
- clean tree;
- allowlist.

## 80.3 Tooling ownership

Cada script debe estar registrado en catálogo si el proyecto lo requiere.

## 80.4 Generated output

No escribir fuera de ownership.

---

# 81. Prompt engineering para equipos de código

## 81.1 Prompt como contrato

Un prompt debe ser ejecutable y auditable.

Cuando el trabajo pueda confundirse con una operación de ciberseguridad ofensiva, el prompt debe declarar de forma breve y verificable:

- quién declara la autorización;
- cuál es el repositorio o target autorizado;
- cuál es el objetivo defensivo;
- qué acciones están permitidas;
- qué acciones están excluidas;
- cuál es el límite de impacto.

La declaración debe describir el trabajo real. No debe exagerar permisos, inventar ownership ni presentarse como mecanismo para omitir controles de seguridad.

Debe eliminar ambigüedad sobre:

- base;
- branch;
- goal;
- files;
- constraints;
- approval;
- tests;
- Git;
- PR;
- merge.

## 81.2 Long prompt structure

```text
Repository
Current state
Goal
Approval protocol
Environment
Architecture context
Scope
Non-scope
Files
Contracts
Algorithms
Tests
Validators
Docs
Security
Performance
Validation
Git
Report
Stop conditions
```

## 81.3 Prompt minimization

Para follow-ups dentro del mismo contexto, no repetir todo. Incluir solo:

- repositorio y branch;
- una línea breve de autorización defensiva;
- exact failure;
- diagnosis;
- allowed changes;
- validations.

En un chat nuevo, después de un cambio de target o cuando cambie el alcance de seguridad, volver a incluir el bloque de autorización completo.

## 81.4 Prompt closure

Siempre definir:

```text
Do not proceed beyond X.
```

## 81.5 Prompt review

Antes de enviar, comprobar:

- no contradiction;
- no impossible requirements;
- no missing authorization;
- no wrong path;
- no stale SHA;
- no tool assumption.

---

# 82. Orquestación de múltiples chats

## 82.1 Roles de chats

Asignar:

```text
Chat A — reconnaissance
Chat B — architecture review
Chat C — implementation
Chat D — independent audit
Chat E — CI incident
```

No usar el mismo chat como única fuente de implementación y verificación remota cuando el riesgo es alto.

## 82.2 Independence

El auditor no debe aceptar el reporte del implementador.

Debe partir de:

- branch;
- SHA;
- run;
- diff.

## 82.3 Handoff between chats

Incluir:

```text
Verified facts
Unverified claims
Current branch
Current SHA
Files
Commands run
Failures
Next objective
```

## 82.4 No cross-chat drift

No modificar el objetivo durante handoff.

---

# 83. Integration manager playbook

## 83.1 Antes de integrar

- contratos estabilizados;
- delegated work complete;
- no overlapping diffs;
- tests locales;
- docs draft.

## 83.2 Integración

Orden:

```text
types
→ pure core
→ runtime
→ IPC
→ renderer
→ tests
→ validators
→ docs
→ metadata
```

## 83.3 Conflicts

Resolver semánticamente, no elegir “ours/theirs” a ciegas.

## 83.4 Final integration review

Verificar que:

- cada import resuelve;
- ningún old contract quedó;
- no hay duplicate implementation;
- state defaults completos;
- docs coinciden.

---

# 84. Quality scorecard

Puntuar 0–2:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Correctness | unknown | partial | demonstrated |
| Architecture | violated | acceptable | coherent |
| Security | unchecked | basic | reviewed |
| Tests | weak | adequate | adversarial |
| Docs | stale | updated | integrated |
| Git | unclear | acceptable | verified |
| CI | missing | partial | final SHA |
| Scope | expanded | mostly controlled | exact |
| Reliability | fragile | guarded | recovery defined |
| Performance | unknown | reasoned | measured |

No promover si:

- cualquier dimensión crítica = 0;
- total < umbral definido;
- CI != final SHA.

---

# 85. Executive reporting

## 85.1 Status report

```text
Status:
Goal:
Base:
Branch:
Completed:
Validated:
Blocked:
Risk:
Decision needed:
Next gate:
```

## 85.2 Technical report

```text
Architecture delta
Contract delta
Runtime delta
Security delta
Test evidence
Documentation delta
Git evidence
CI evidence
```

## 85.3 No noise

No incluir:

- artifacts no solicitados;
- rutas privadas;
- detalles irrelevantes;
- largas narrativas sin decisión.

---

# 86. Root cause analysis

## 86.1 Five whys

Usar con cuidado.

## 86.2 Causal tree

Separar:

```text
trigger
root cause
contributing factor
detection failure
process failure
```

## 86.3 Corrective actions

Clasificar:

- immediate;
- preventive;
- detective;
- process.

No limitarse a “tener más cuidado”.

---

# 87. Recovery drills

Para cambios críticos, definir:

- cómo revertir;
- cómo reconstruir;
- cómo verificar artifacts;
- cómo recuperar commit perdido;
- cómo limpiar branch auxiliar;
- cómo validar tree.

No ejecutar drill destructivo en producción sin aprobación.

---

# 88. Plantilla de delegation packet

```text
TASK ID:
TITLE:
ROLE:
REPOSITORY:
BASE SHA:
WORK BRANCH:
OBJECTIVE:
BUSINESS VALUE:
ARCHITECTURE CONTEXT:
OWNED PATHS:
READ-ONLY PATHS:
PROHIBITED PATHS:
INPUTS:
OUTPUTS:
INVARIANTS:
NON-GOALS:
IMPLEMENTATION SLICES:
TEST MATRIX:
SECURITY CHECKS:
PERFORMANCE CHECKS:
VALIDATION COMMANDS:
DOCUMENTATION:
GIT RULES:
DEFINITION OF DONE:
STOP CONDITIONS:
HANDOFF FORMAT:
```

---

# 89. Plantilla de handoff

```text
TASK:
STATUS:
BASE:
BRANCH:
HEAD:
TREE:
FILES CHANGED:
CONTRACTS:
BEHAVIOR:
TESTS RUN:
VALIDATORS:
DOCS:
KNOWN LIMITATIONS:
RISKS:
UNVERIFIED:
NEXT ACTION:
```

---

# 90. Plantilla de architecture review

```text
Decision:
Context:
Current flow:
Proposed flow:
Boundaries:
Alternatives:
Trade-offs:
Security:
Performance:
Migration:
Testing:
Rollback:
Recommendation:
Approval required:
```

---

# 91. Plantilla de code review

```text
Summary:
Scope match:
Architecture:
Correctness:
Security:
Concurrency:
Performance:
Errors:
Tests:
Docs:
Git:
Findings:
- BLOCKER:
- MAJOR:
- MINOR:
- NIT:
Decision:
```

---

# 92. Plantilla de release checklist

```text
[ ] base verified
[ ] branch verified
[ ] commit verified
[ ] tree verified
[ ] diff reviewed
[ ] tests pass
[ ] validators pass
[ ] docs pass
[ ] metadata idempotent
[ ] build idempotent
[ ] typecheck
[ ] audit
[ ] clean tree
[ ] push normal
[ ] remote compare
[ ] CI final SHA
[ ] PR authorized
[ ] merge authorized
[ ] post-merge verified
[ ] branches cleaned
```

---

# 93. Regla de delegación excelente

Una delegación se considera excelente cuando otro senior puede ejecutarla sin:

- adivinar intención;
- preguntar qué branch usar;
- decidir qué archivos tocar;
- inferir el non-scope;
- inventar tests;
- asumir cómo publicar;
- interpretar cuándo detenerse.

Si requiere interpretación material, el packet está incompleto.

---

# 94. Regla de implementación excelente

Una implementación se considera excelente cuando:

- el diseño es coherente;
- estados inválidos son difíciles de representar;
- errores son estructurados;
- side effects están aislados;
- tests prueban invariants;
- performance está acotada;
- seguridad está revisada;
- docs reflejan la verdad;
- Git es limpio;
- CI corresponde al SHA final;
- rollback es claro.

---

# 95. Regla final ampliada

El agente debe operar como una organización de ingeniería madura.

No debe optimizar únicamente por velocidad de escritura.

Debe optimizar por:

```text
correctness
clarity
reversibility
testability
security
operability
maintainability
delivery confidence
```

Una tarea solo está cerrada cuando existe coherencia entre:

```text
goal
architecture
code
tests
validators
documentation
Git
GitHub
CI
release state
```

No declarar éxito antes.
