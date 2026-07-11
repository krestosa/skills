## 52.10 Limitaciones resumidas de Contents API

La política completa se encuentra en `52.9.10`. En síntesis, las escrituras file-by-file suelen:

- reemplazar contenido completo;
- requerir blob/content SHA;
- crear un commit por operación;
- carecer de atomicidad multi-file;
- dificultar build-before-publish;
- producir historia no deseada.

Por eso el flujo normal sigue siendo:

```text
local edit
→ local validation
→ local commit
→ connector-native Git Data publication
→ connector PR
```

Para un único commit multiarchivo remoto, usar únicamente el protocolo connector-native de `52.9.12`, con autorización explícita.

## 52.11 Review follow-up

1. Resolver repo y PR.
2. Obtener metadata y patch.
3. Descubrir si existe lectura thread-aware del conector.
4. Si existe, usarla para `resolved`, `outdated`, anchors y comments.
5. Si falta información, usar otra acción del conector; si no existe, bloquear y reportar la capacidad ausente.
6. Agrupar threads accionables.
7. Confirmar scope.
8. Implementar localmente.
9. Validar.
10. Responder o resolver threads solo con autorización.

## 52.12 CI debug

1. Resolver commit SHA y PR.
2. Obtener combined status y runs.
3. Descubrir jobs, steps y logs mediante conector.
4. Si falta discovery, attempt o log completo, usar otra acción del conector o declarar verificación incompleta.
5. Identificar el primer fallo causal.
6. Proponer plan.
7. Implementar solo después de aprobación.
8. Revalidar localmente.
9. Publicar solo si se autoriza.
10. Verificar CI del SHA nuevo.

## 52.13 Publish workflow

1. Confirmar scope con `git status` y diff.
2. Confirmar branch strategy aprobada; no imponer `agent/` si el usuario definió naming propio.
3. Stage paths explícitos.
4. Commit con mensaje aprobado.
5. Ejecutar checks relevantes.
6. Preflight de red.
7. Push con tracking.
8. Verificar branch y commit mediante conector.
9. Crear draft PR mediante conector si se autorizó.
10. Crear el PR exclusivamente con `create_pull_request`; si no está disponible, bloquear.

## 52.14 Build, ejecución y screenshots

Una vez materializado un workspace completo, el agente puede intentar:

```text
install
validate
build
launch
interact
capture
```

Cada verbo tiene un gate independiente.

Para el repositorio objetivo, probar como mínimo:

```text
Node/npm versions
Electron binary
build outputs
runtime start
window readiness
fatal renderer/main errors
screenshot capability
clean shutdown
```

No usar screenshots como sustituto de tests. No usar tests como prueba de rendering visual.

## 52.15 Trust model

Orden para estado remoto:

```text
connector exact commit/branch/compare
> local Git después de fetch exitoso
> PR narrative
> chat report
```

Orden para contenido local:

```text
working tree at exact SHA
> connector fetch_file at exact ref
> PR patch
> search snippet
> docs
```

Orden para CI:

```text
run + job + step + log tied to final SHA
> combined status
> check summary
> badge
> narrative
```

Orden para ejecución:

```text
captured process output and exit code
> generated artifact
> screenshot
> assumption from build
```

## 52.16 Tool call journal

Mantener:

```text
tool/plane
purpose
repo/ref
input
result
write action
confidence
next gate
```

No repetir llamadas que ya produjeron evidencia suficiente.

## 52.17 Fallback ladder

```text
connector read
→ existing local checkout
→ direct Git if preflight passes
→ connector read/write capability explicitly discovered
→ block uncovered connector gaps
→ approved artifact recovery
→ BLOCKED
```

No saltar a Base64, trees, refs o contents API para simular un flujo Git normal.

## 52.18 Regla de no sobreafirmación

Usar estados exactos:

```text
remote inspected
source partially fetched
workspace materialized
validated locally
built locally
application launched
UI visually verified
published remotely
CI verified
```

Nunca colapsarlos en “terminado”.

---
