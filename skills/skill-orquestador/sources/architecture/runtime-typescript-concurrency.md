# 57. Patrones arquitectónicos recomendados

> Runtime repository variables
>
> - `{{repository_full_name}}`: exact `owner/name`, resolved from the user request, project context, URL, or connector metadata.
> - `{{repository_url}}`: canonical repository URL when an action specifically requires a URL.
> - `{{default_branch}}`: remote default branch resolved through repository metadata.
> - `{{base_sha}}`: exact verified base commit SHA.
> - `{{branch}}`: explicitly authorized working branch.
>
> No repository, owner, branch, framework, product, or organization is a built-in default.

## 57.1 Functional Core, Imperative Shell

Preferir:

```text
pure core
+ effectful boundary
```

Core:

- determinista;
- sin I/O;
- testeable.

Shell:

- filesystem;
- Electron;
- network;
- process;
- clock.

## 57.2 Ports and Adapters

Definir puertos para:

- filesystem;
- clock;
- hashing;
- process runner;
- persistence;
- external services.

No crear interfaces por cada función trivial. Aplicar donde mejora testabilidad o reemplazo.

## 57.3 Dependency Inversion

Las capas de dominio no deben importar runtime.

```text
core ← main
core ← renderer
shared contracts ← main/preload/renderer
```

No:

```text
core → Electron
core → node:fs
renderer → node:fs
```

## 57.4 State Machine

Usar para flujos con estados y transiciones:

- Preview;
- selection;
- write transaction;
- history;
- sync;
- workflow orchestration.

Evitar flags booleanos contradictorios.

Mal:

```ts
isLoading
isReady
isFailed
isStale
```

Mejor:

```ts
status: "idle" | "loading" | "ready" | "failed" | "stale"
```

## 57.5 Discriminated unions

Usar para resultados:

```ts
type Result =
  | { ok: true; value: T }
  | { ok: false; error: DomainError };
```

No exigir campos imposibles en estados blocked.

## 57.6 Command pattern

Usar para acciones con:

- intent;
- validation;
- preview;
- execution;
- undo.

Separar:

```text
CommandIntent
CommandPreview
CommandExecution
CommandResult
```

## 57.7 Repository pattern

Solo cuando hay persistence abstraction real.

No crear repositories para arrays en memoria sin necesidad.

## 57.8 Adapter pattern

Usar para parsers, filesystem o APIs externas.

## 57.9 Strategy pattern

Usar cuando existen algoritmos intercambiables reales.

No introducirlo anticipadamente.

## 57.10 Factory

Usar para construcción validada y consistente.

Evitar `new` disperso para objetos con invariants.

## 57.11 Policy object

Centralizar reglas:

- path policy;
- change policy;
- validation policy;
- security policy.

No duplicar lógica de policy en múltiples capas.

## 57.12 Result and error taxonomy

Errores deben tener:

```text
code
category
message
cause
context
retryable
severity
```

No depender de strings para lógica.

---

# 58. Anti-patrones arquitectónicos

Evitar:

- God object;
- service locator global;
- mutable singleton sin ownership;
- booleans combinatorios;
- exception-driven normal flow;
- catch-all silencioso;
- broad `any`;
- implicit state;
- hidden I/O;
- duplicate source of truth;
- timestamp as identity;
- path as revision;
- UI-driven domain logic;
- renderer authority;
- parser output treated as browser truth;
- regex como parser general;
- mega-validator token-based;
- workflow como motor de publicación de código;
- branch de transporte;
- artifact-driven source control;
- speculative abstraction;
- premature microservices;
- premature event sourcing;
- premature CQRS;
- big-bang rewrite.

---

# 59. Estándares avanzados de TypeScript

## 59.1 Tipos

Preferir:

- unions;
- readonly;
- branded types cuando evitan mezcla;
- exhaustive switches;
- explicit return types en API pública;
- `unknown` en input no confiable;
- guards.

Evitar:

- `any`;
- non-null assertion;
- type cast para ocultar incompatibilidad;
- enums cuando union literal es suficiente;
- objetos parcialmente válidos.

## 59.2 Exhaustividad

```ts
function assertNever(value: never): never {
  throw new Error(`Unhandled variant: ${String(value)}`);
}
```

Usar en switches de dominio.

## 59.3 Branded types

Aplicar con moderación:

```ts
type ProjectRelativePath = string & { readonly __brand: "ProjectRelativePath" };
type SourceRevisionDigest = string & { readonly __brand: "SourceRevisionDigest" };
```

No usar si complica serialización sin beneficio.

## 59.4 Validación de boundaries

Todo input externo entra como `unknown`.

```text
IPC
postMessage
filesystem data
config JSON
CLI args
environment
```

Validar antes de usar.

## 59.5 Immutability

Modelos de estado:

```ts
readonly
```

Updates mediante funciones explícitas.

## 59.6 Nullability

Elegir semántica:

- `null` para ausencia deliberada;
- `undefined` para propiedad opcional no materializada.

No mezclar sin criterio.

## 59.7 Error handling

No hacer:

```ts
catch {}
```

Hacer:

```ts
catch (error) {
  return fail(normalizeError(error));
}
```

## 59.8 Async

- no floating promises;
- usar `await`;
- manejar cancellation;
- usar timeout;
- evitar `Promise.all` sin límite para inputs grandes;
- usar bounded concurrency.

---

# 60. Concurrencia y control de carreras

## 60.1 Principios

Toda operación async debe definir:

```text
identity
ownership
cancellation
timeout
stale check
completion behavior
```

## 60.2 Operation ID

Usar IDs para evitar respuestas stale:

```text
requestId
loadId
transactionId
snapshotId
```

Validar el ID al completar.

## 60.3 AbortController

Usar cuando una operación puede quedar obsoleta:

- Preview load;
- parsing;
- search;
- network;
- long-running task.

## 60.4 Mutex / in-flight guard

Usar solo cuando:

- la operación no puede solaparse;
- el estado compartido lo requiere.

No usar boolean simple sin `finally`.

```ts
if (inFlight) return blocked();
inFlight = true;
try {
  ...
} finally {
  inFlight = false;
}
```

## 60.5 Optimistic concurrency

Para futuras escrituras:

```text
read revision
→ prepare patch
→ compare current revision
→ apply if equal
```

Nunca aplicar offset sobre revisión distinta.

## 60.6 Idempotency key

Para comandos que pueden repetirse:

```text
commandId
idempotencyKey
```

No ejecutar dos veces la misma mutación.

## 60.7 Bounded concurrency

Para scans:

```text
max concurrent reads
max bytes
max files
timeout
```

No `Promise.all` sobre miles de archivos.

---

# 61. Diseño de errores de nivel industria

## 61.1 Taxonomía

```text
VALIDATION_ERROR
NOT_FOUND
CONFLICT
STALE_STATE
UNSUPPORTED
SECURITY_VIOLATION
TIMEOUT
CANCELLED
IO_ERROR
PROCESS_ERROR
INTERNAL_ERROR
```

## 61.2 Error object

```ts
interface DomainError {
  readonly code: string;
  readonly category: ErrorCategory;
  readonly message: string;
  readonly reason: string;
  readonly retryable: boolean;
  readonly context: Readonly<Record<string, string | number | boolean | null>>;
}
```

No incluir:

- secretos;
- source text;
- paths absolutos en renderer;
- stack trace en UI.

## 61.3 Error translation

```text
low-level error
→ domain error
→ IPC-safe error
→ user-facing message
```

No exponer errores crudos.

## 61.4 Retry policy

Retry solo si:

- operación idempotente;
- error transitorio;
- límite definido;
- backoff;
- jitter;
- timeout total.

No retry:

- validation;
- security;
- conflict;
- unsupported;
- malformed input.

---

# 62. Diseño de API e IPC

## 62.1 Contract-first

Antes de handler:

- request;
- response;
- errors;
- version;
- validation;
- ownership;
- timeout;
- cancellation.

## 62.2 Request mínima

Renderer envía intención, no autoridad.

Mal:

```text
absolutePath
sourceText
revision
offset
```

Bien:

```text
requestId
elementId
mode
```

Main deriva contexto confiable.

## 62.3 Versioning

Para contratos duraderos:

```ts
schemaVersion: 1
```

Cambios incompatibles requieren migración o nuevo channel.

## 62.4 Compatibility

Mantener:

- backward compatibility cuando existe consumer activo;
- deprecation window;
- tests de serialización.

## 62.5 IPC allowlist

Todo channel debe estar:

- declarado;
- tipado;
- registrado;
- validado;
- documentado;
- testeado.

## 62.6 Response stale

Renderer debe descartar response si:

```text
requestId mismatch
loadId mismatch
snapshotId mismatch
component disposed
```

---

# 63. Persistencia y transacciones

## 63.1 Escritura segura

Para futuras operaciones:

```text
validate
→ preflight revision
→ write temp
→ fsync if required
→ atomic replace
→ verify
→ update state
→ refresh
```

## 63.2 Rollback

Definir antes de ejecutar.

No prometer atomicidad cross-file si el filesystem no la provee.

## 63.3 Journaling

Usar solo para transacciones multi-file o recuperación.

## 63.4 Dirty state

Debe derivarse de:

- saved revision;
- current revision;
- pending transaction.

No de un boolean manual sin fuente.

## 63.5 Migration

Toda migración debe tener:

- from version;
- to version;
- forward;
- rollback o backup;
- idempotence;
- validation;
- fixture.

---

# 64. Performance engineering

## 64.1 Performance budget

Definir para operaciones relevantes:

```text
max files
max bytes
max nodes
max depth
max duration
max memory
max IPC payload
```

## 64.2 Complejidad

Revisar:

- O(n²);
- repeated scans;
- repeated parse;
- repeated line calculation;
- unbounded arrays;
- large string copies.

## 64.3 Measure before optimize

Usar:

- timing;
- counters;
- memory snapshots;
- benchmark fixtures.

No optimizar por intuición cuando el cambio agrega complejidad.

## 64.4 Hot path

Documentar hot paths:

- project scan;
- DOM snapshot;
- selection mapping;
- overlay updates;
- watch refresh.

## 64.5 Caching

Un cache debe definir:

```text
key
value
owner
lifetime
invalidation
max size
stale behavior
```

No crear cache sin invalidación.

## 64.6 IPC payload budget

No enviar:

- source completo;
- árboles completos repetidos;
- arrays ilimitados;
- stacks.

Usar previews acotadas.

---

# 65. Reliability engineering

## 65.1 Timeouts

Toda operación externa o larga debe tener timeout.

## 65.2 Cancellation

Operaciones obsoletas deben cancelarse o descartarse.

## 65.3 Graceful degradation

Cuando falla una capacidad no crítica:

- mantener app usable;
- mostrar estado;
- no simular éxito;
- permitir retry.

## 65.4 Fail closed

Para seguridad y escritura:

- si provenance falta → bloquear;
- si revision mismatch → bloquear;
- si path inseguro → bloquear;
- si input inválido → bloquear.

## 65.5 Fail open

Solo para funciones no críticas y explícitas, por ejemplo diagnóstico visual opcional. Documentar.

## 65.6 Recovery

Toda operación con side effects debe definir:

- cleanup;
- rollback;
- residue detection.

---
