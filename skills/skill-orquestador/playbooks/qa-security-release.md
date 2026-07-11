# 66. Testing strategy avanzada

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

## 66.1 Pirámide

```text
many unit tests
fewer integration tests
few end-to-end tests
```

## 66.2 Contract tests

Para:

- IPC;
- config schemas;
- serialization;
- process runner;
- filesystem adapter.

## 66.3 Property-based testing

Usar cuando hay invariants amplias:

- path normalization;
- range math;
- IDs deterministic;
- parser offsets.

Si no existe library, generar tablas controladas sin agregar dependencia.

## 66.4 Metamorphic tests

Ejemplos:

- cambiar `generatedAt` no cambia ID;
- cambiar un byte cambia revision;
- reordenar class tokens no cambia match;
- ejecutar sync dos veces no cambia tree.

## 66.5 Mutation testing conceptual

Revisar si un test fallaría al:

- eliminar una validación;
- cambiar `<=` por `<`;
- omitir stale check;
- aceptar fallback.

No es obligatorio agregar herramienta.

## 66.6 Golden tests

Usar con cuidado para outputs grandes.

Debe existir revisión semántica, no actualizar snapshot a ciegas.

## 66.7 Fuzzing limitado

Para parsers y validators:

- malformed strings;
- Unicode;
- null bytes;
- long inputs;
- nesting;
- invalid paths.

## 66.8 Race tests

Simular:

- target change durante read;
- reload durante response;
- watcher event durante build.

## 66.9 Security tests

Comprobar:

- traversal;
- absolute path;
- forged postMessage;
- unknown IPC fields;
- oversized payload;
- source leak.

---

# 67. QA gates

## 67.1 Gate A — Contract

- types compile;
- invariants documented;
- invalid states unrepresentable cuando sea viable.

## 67.2 Gate B — Unit

- core behavior;
- edge cases;
- negative cases.

## 67.3 Gate C — Integration

- main/core;
- IPC/preload/renderer;
- filesystem temp fixture.

## 67.4 Gate D — Regression

- validators anteriores;
- quick suite;
- tooling suite.

## 67.5 Gate E — Documentation

- markdown;
- architecture;
- guided docs;
- roadmap.

## 67.6 Gate F — Release

- build;
- typecheck;
- audit;
- clean diff;
- commit;
- CI final.

No avanzar si un gate crítico falla.

---

# 68. Code review industrial

## 68.1 Orden de review

1. Goal.
2. Scope.
3. Architecture.
4. Contracts.
5. Security.
6. Correctness.
7. Error handling.
8. Concurrency.
9. Performance.
10. Tests.
11. Docs.
12. Git hygiene.

## 68.2 Findings

```text
BLOCKER — riesgo de corrupción, seguridad o diseño inválido
MAJOR — comportamiento incorrecto o deuda significativa
MINOR — mejora necesaria no bloqueante
NIT — estilo
QUESTION — aclaración
```

## 68.3 Review questions

- ¿El código representa estados inválidos?
- ¿Se duplica source of truth?
- ¿Hay una race?
- ¿El error es accionable?
- ¿El test fallaría con una implementación incorrecta?
- ¿El cache se invalida?
- ¿El renderer recibe autoridad excesiva?
- ¿La documentación afirma demasiado?
- ¿El diff incluye scope extra?
- ¿El rollback existe?
- ¿La operación es idempotente?
- ¿El API es más amplio de lo necesario?

## 68.4 Approval bar

No aprobar con:

- BLOCKER;
- MAJOR;
- CI faltante;
- docs obsoletas;
- tests insuficientes;
- artifacts;
- branch contaminada.

---

# 69. Threat modeling

## 69.1 STRIDE

Revisar:

- Spoofing;
- Tampering;
- Repudiation;
- Information disclosure;
- Denial of service;
- Elevation of privilege.

## 69.2 Trust boundaries

```text
user project files
iframe Preview
renderer
preload
main
filesystem
GitHub Actions
external network
```

## 69.3 Threat questions

- ¿Puede el proyecto enviar un postMessage falso?
- ¿Puede escapar del project root?
- ¿Puede exponer path absoluto?
- ¿Puede disparar una escritura?
- ¿Puede bloquear con input enorme?
- ¿Puede inyectar shell args?
- ¿Puede contaminar logs?
- ¿Puede una PR no confiable acceder a secretos?

## 69.4 Security review output

```text
asset
threat
entry point
mitigation
residual risk
test
```

---

# 70. Dependency governance

## 70.1 Evaluación

Para cada dependencia propuesta:

```text
purpose
alternatives
license
maintainers
release cadence
security history
bundle/runtime cost
native binaries
postinstall
transitive dependencies
lockfile impact
```

## 70.2 Preferencia

```text
standard library
> existing dependency
> small focused dependency
> large framework
```

## 70.3 Pinning

Seguir política del proyecto.

No actualizar rangos no relacionados.

## 70.4 Supply chain

Revisar:

- install scripts;
- provenance;
- integrity;
- audit;
- action SHA pins.

---

# 71. Observabilidad y logging

## 71.1 Eventos estructurados

Preferir:

```ts
{
  event: "dom-snapshot.build.failed",
  code: "unsupported-source-encoding",
  target: "index.html",
  durationMs: 42
}
```

## 71.2 No loggear

- source text;
- secretos;
- tokens;
- paths absolutos hacia renderer;
- payloads completos;
- environment completo.

## 71.3 Correlation IDs

Usar:

- requestId;
- loadId;
- transactionId;
- workflow run ID solo para diagnóstico.

## 71.4 Metrics

Cuando corresponda:

- duration;
- count;
- size;
- failures;
- stale discards;
- cache hits.

No agregar infraestructura pesada sin necesidad.

---

# 72. Release engineering

## 72.1 Release readiness

Comprobar:

- changelog/roadmap;
- versioning si aplica;
- build;
- packaging;
- smoke;
- rollback;
- known issues.

## 72.2 Feature flags

Usar cuando:

- rollout gradual;
- riesgo alto;
- capacidad incompleta;
- fallback.

Una flag debe tener:

```text
owner
default
scope
removal date
tests
```

No dejar flags permanentes.

## 72.3 Dark launch

Puede usarse para medir sin UI, pero debe estar aprobado.

## 72.4 Rollback plan

Antes de merge:

```text
revert commit
disable flag
restore previous artifact
```

No depender de reescribir historia de `{{default_branch}}`.

---

# 73. Git strategy avanzada

## 73.1 Trunk-compatible

Branches pequeñas, vida corta, scope único.

## 73.2 Commit atomicity

Un commit debe:

- compilar;
- pasar tests relevantes;
- representar una unidad;
- tener docs coherentes.

## 73.3 Commit message

Imperativo, específico:

```text
Add source identity and node mapping hardening
```

No:

```text
fix stuff
updates
WIP
```

## 73.4 Revertability

El commit debe poder revertirse sin requerir arqueología.

## 73.5 History integrity

No fabricar timestamps ni parentage.

---

# 74. Gestión de documentación como código

## 74.1 Documentation debt

Registrar cuando:

- flow cambió;
- ownership cambió;
- next phase cambió;
- validator cambió;
- boundary cambió.

## 74.2 Docs review

Aplicar mismos niveles:

```text
BLOCKER — afirma capacidad inexistente
MAJOR — flujo incorrecto
MINOR — navegación incompleta
NIT — estilo
```

## 74.3 Diagramas

Mermaid debe:

- reflejar flujo real;
- mostrar trust boundaries;
- no ocultar errores;
- no afirmar write path inexistente.

## 74.4 Generated docs

Distinguir:

```text
generated facts
human-authored rationale
```

No generar razonamiento editorial automáticamente.

---

# 75. Gestión de roadmap y portfolio

## 75.1 Priorización

Evaluar:

```text
user value
risk reduction
dependency unlocking
effort
architecture leverage
maintenance cost
```

## 75.2 WSJF simplificado

```text
(cost of delay) / job size
```

No usar mecánicamente; sirve para comparar.

## 75.3 Technical debt

Clasificar:

- correctness debt;
- architecture debt;
- testing debt;
- documentation debt;
- operational debt;
- security debt.

## 75.4 Next phase

Una fase siguiente debe:

- depender de lo integrado;
- cerrar un gap;
- no contaminar roadmap;
- tener Definition of Ready.

---

# 76. Stop-the-line criteria

Detener inmediatamente si:

- `{{default_branch}}` remoto cambió materialmente;
- working tree no limpio;
- commit anunciado no existe;
- branch incorrecta;
- CI del SHA final no existe;
- security regression;
- data loss risk;
- path traversal;
- source write no aprobada;
- lockfile cambió inesperadamente;
- validator fue relajado;
- tests fueron deshabilitados;
- artifacts operativos entraron al diff;
- branch auxiliar contiene implementación real;
- PR es parcial;
- author/committer no puede cumplirse cuando es requisito;
- tool no puede garantizar la operación.

Emitir:

```text
STOP-THE-LINE
Reason:
Evidence:
Impact:
Required decision:
```

---

# 77. Gestión de incertidumbre

## 77.1 Assumption log

Registrar:

| ID | Assumption | Evidence | Confidence | Validation |
|---|---|---|---|---|

## 77.2 Confidence levels

```text
High — verified directly
Medium — inferred from multiple sources
Low — hypothesis
```

## 77.3 No hidden assumptions

Toda suposición que afecte diseño debe aparecer en el plan.

---

# 78. Architecture Decision Records

Crear ADR cuando la decisión:

- cruza capas;
- es difícil de revertir;
- establece source of truth;
- cambia seguridad;
- cambia persistence;
- cambia parser;
- cambia transaction model.

Formato:

```text
Title
Status
Context
Decision
Alternatives
Consequences
Risks
Validation
```

No crear ADR para cada helper.

---
