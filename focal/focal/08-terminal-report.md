# Focal — Reporte terminal legible

Emití **un único reporte Markdown renderizado**. No uses un bloque de código, no vuelques una secuencia plana de `Campo: valor` y no repitas la misma información en varias secciones.

## Enlaces Markdown obligatorios

En la **capa Markdown visible**, todo recurso navegable debe presentarse como enlace Markdown. Esto incluye pull requests, ramas, commits, merges, checkpoints, issues, workflows, runs de GitHub Actions, archivos y documentación externa.

- Pull request: `[PR #<n>](https://github.com/<owner>/<repo>/pull/<n>)`.
- Rama: [`<rama>`](https://github.com/<owner>/<repo>/tree/<rama>).
- Commit, merge o checkpoint: [`<SHA corto>`](https://github.com/<owner>/<repo>/commit/<SHA completo>).
- Workflow: [`<nombre>`](https://github.com/<owner>/<repo>/actions/workflows/<archivo-workflow>).
- Run de Actions: [`run <id>`](https://github.com/<owner>/<repo>/actions/runs/<id>).
- Issue: [`issue #<n>`](https://github.com/<owner>/<repo>/issues/<n>).
- Archivo: [`<ruta>`](https://github.com/<owner>/<repo>/blob/<SHA-o-rama>/<ruta>).

Usá la URL remota observada; no inventes enlaces para recursos no verificados. Los identificadores opacos, timestamps, estados y códigos no son enlaces. **Nunca insertes URLs ni sintaxis Markdown en JSON, bloques `focal-command:v3`, bloques `focal-state:v3`, payloads machine-readable, evidencias estructuradas o bloques de código.**

## Jerarquía obligatoria

La primera pantalla debe permitir entender, sin abrir detalles:

1. resultado;
2. entrega observable;
3. objetivo;
4. PR, merge y CI;
5. estado final del coordinador;
6. siguiente acción.

Elegí exactamente una cabecera:

- `# ✅ PASS — <resultado observable en una línea>`
- `# 🟡 PARTIAL — <avance preservado y faltante principal>`
- `# 🔴 BLOCKED — <bloqueo externo comprobado>`
- `# ⚪ NO-OP — <motivo por el que no correspondía actuar>`

No uses un emoji distinto para esos cuatro resultados.

---

# <icono> <RESULTADO> — <resumen concreto>

> **Entrega:** <qué quedó efectivamente disponible, mergeado o preservado>

| Resumen | Estado |
|---|---|
| **Objetivo** | <objetivo seleccionado> |
| **Carril** | `LOW_RISK_BULK`, `HIGH_IMPACT_INCREMENT`, `RECOVERY` o no aplicable |
| **PR / merge** | <link a PR, link al commit de merge y subject exacto que contiene `#<n>`, o no aplicable> |
| **CI** | <icono, link al workflow/run exacto y conclusión, o no aplicable> |
| **Coordinador** | <🟢 `IDLE`, 🔵 `WORKING`, 🔴 desconocido o no adquirido> |
| **Estado observado UTC** | <timestamp exacto de la lectura que sustenta el estado; es una instantánea, no una garantía futura> |
| **Duración** | <inicio UTC → fin UTC; indicar si quedó dentro del runtime guard> |

> [!IMPORTANT]
> **Siguiente acción:** <una acción concreta, ejecutable y priorizada>

## Cambios principales

- <cambio o capacidad entregada>
- <segundo cambio relevante>
- <documentación, roadmap o matriz reconciliados cuando corresponda>

Mencioná archivos solo cuando ayuden a entender el cambio. No conviertas esta sección en un inventario técnico.

## Validación

| Comprobación | Resultado | Evidencia |
|---|---|---|
| <test, build o contrato> | ✅ Aprobado / ❌ Falló / ⚪ No ejecutado | <run, comando o motivo> |
| <CI del head exacto> | <resultado> | <run y SHA> |

Después de la tabla, agregá únicamente las aclaraciones necesarias:

- **Pruebas fallidas:** <ninguna o lista concisa>.
- **Pruebas no ejecutadas:** <ninguna o prueba + motivo factual>.
- **Nivel de evidencia:** `STATIC`, `GL_COMPILE_LINK`, `GL_RENDER_READBACK`, `IRIS_PATCHED` o `IRIS_CLIENT`, cuando aplique.

## Estado del proyecto

- **Roadmap:** <ítems modificados y estados finales>.
- **Iris:** <capacidades verificadas o actualizadas>.
- **Rama final:** <link Markdown a la rama>.
- **Checkpoint / SHA final:** <link Markdown al commit>.
- **Bloqueos:** <ninguno o bloqueo comprobado>.

Omití las filas que no apliquen en `SKILLS_MAINTENANCE` o `NO-OP`.

## Riesgos y limitaciones

- <limitación real que siga vigente>.
- <riesgo residual o evidencia todavía no alcanzada>.

Cuando no exista ninguno, escribí: `- Ninguno conocido dentro del alcance validado.`

## Próximo paso

> <acción concreta, por qué sigue y qué evidencia debe producir>

## Trazabilidad

| Recurso | Valor |
|---|---|
| **SHA remoto inicial** | <link Markdown al commit> |
| **SHA remoto final** | <link Markdown al commit> |
| **Commit(s)** | <links Markdown a los commits funcionales> |
| **Pull request** | <link Markdown a la PR o no aplicable> |
| **Estado del merge** | <estado y link Markdown al commit de merge> |
| **Título del merge** | <subject exacto observado> |
| **Referencia visible al PR** | <verificada: `#<n>` o defecto `MERGE_PR_REFERENCE_MISSING`> |
| **Estado de CI** | <link Markdown al workflow/run y conclusión> |
| **Roadmap** | <link Markdown a `docs/ROADMAP.md` o no aplicable> |
| **Matriz de Iris** | <link Markdown a `docs/IRIS-CAPABILITY-MATRIX.md` o no aplicable> |

<details>
<summary><strong>Detalles operativos y de recuperación</strong></summary>

### Ejecución

| Campo | Valor |
|---|---|
| **Modo** | `FOCAL_CYCLE` o `SKILLS_MAINTENANCE` |
| **Ruta excepcional** | no aplicable o `COORDINATOR_REPAIR` |
| **Runtime guard** | <soft stop, cleanup, hard stop y cumplimiento> |
| **Run ID** | `<identificador opaco>` |
| **Command ID de adquisición** | `<identificador opaco o no adquirido>` |
| **Último heartbeat confirmado** | <timestamp o no aplicable> |
| **Command ID de liberación** | `<identificador opaco o no aplicable>` |
| **Lock liberado** | sí, no o no adquirido |
| **Estado final observado** | `idle`, `working` o desconocido, con timestamp UTC exacto |

### Alcance técnico

- **Lote o incremento seleccionado:** <detalle>.
- **WORK_SELECTION_PROOF:** <al menos tres candidatos o todos los restantes, slices evaluados y códigos de descarte>.
- **Código de NO-OP:** <`ACTIVE_RUN`, `PROJECT_ALREADY_COMPLETE`, `NO_AUTHORIZED_WORK`, `ALL_REMAINING_WORK_EXTERNALLY_BLOCKED`, `LATE_ACQUIRE_ORPHANED` o no aplicable>.
- **Justificación de riesgo:** <detalle>.
- **Continuidad de un PARTIAL anterior:** <no o sí + referencia>.
- **Motivo objetivo de PARTIAL:** <no aplicable o evidencia>.
- **Revisión de calidad:** <hallazgos concretos sobre intención, simplicidad, deuda, placeholders, código muerto, errores y tests>.
- **Archivos creados, modificados, movidos o eliminados:** <lista compacta>.

### Recuperación e historia

- **Reintentos del conector:** <cantidad>.
- **Mutaciones con resultado desconocido reconciliadas mediante read-after-write:** <ninguna o detalle>.
- **Presupuesto de reintentos agotado:** sí o no.
- **Fallos autónomamente recuperados:** <ninguno o detalle>.
- **Ruta de recuperación aplicada:** <código o no aplicable>.
- **Fallos no clasificados convertidos en diagnóstico:** <ninguno o detalle>.
- **Commits temporales de reparación:** <ninguno o SHAs>.
- **Historia final de Focal:** <limpia, pendiente o no aplicable>.
- **Candidatos saneados:** <ninguno o clasificación>.
- **Paths basura retirados y clasificación:** <ninguno o detalle>.
- **SHAs excluidos y evidencia:** <ninguno o detalle>.
- **Commits posteriores reconstruidos:** <no aplicable o lista>.
- **Timestamps posteriores preservados:** <no aplicable, verificado o no verificado>.
- **Refs temporales eliminadas:** <no aplicable o lista>.
- **Candidatos alcanzables desde refs/heads o refs/tags:** <ninguno o detalle>.
- **Commit o merge de limpieza presente:** no, sí o no aplicable.
- **Árbol final verificado:** <sí/no + evidencia>.
- **Parent y metadata preservados:** <no aplicable o detalle>.
- **Workflow temporal ausente:** sí, no o no aplicable.

### Rutas y limitaciones completas

- **Flowchart:** `prompts/focal/11-process-flowchart.md` o no aplicable.
- **Limitaciones reales:** <lista factual completa>.
- **Resultado observable entregado:** <detalle técnico si requiere mayor precisión>.

</details>

## Reglas de redacción

- Priorizá conclusiones y estado; relegá identificadores y mecánica al bloque desplegable.
- Usá tablas únicamente para datos comparables y listas breves para cambios o riesgos.
- Omití campos vacíos o irrelevantes; no escribas veinte veces `no aplicable`.
- Usá SHA, PR, runs y rutas verificables.
- En el Markdown visible, convertí todo recurso navegable verificado en enlace; no dejes PR, rama, commit, workflow, run, issue o archivo como texto plano.
- Conservá JSON, payloads estructurados y bloques de código sin Markdown ni URLs añadidas.
- No declares que un archivo, prueba o merge existe si no fue observado remotamente.
- No declares `PASS` si el subject del commit de merge o squash no contiene el número exacto del PR; mostrale al usuario `MERGE_PR_REFERENCE_MISSING` sin sugerir una reescritura retrospectiva de `main`.
- No incluyas nombres de proveedor, modelo, aplicación, cliente, conector, actor, producto o plataforma de conversación. No reproduzcas campos legacy `owner`, `executionSource` ni logins del emisor.
- `runId` y `commandId` son opacos; no derives ni expliques su origen.
- Un error transitorio aislado no justifica un resultado terminal.
- `PASS` requiere publicación, aceptación, reconciliación y liberación completas. En `LOW_RISK_BULK`, todos los archivos e ítems del lote deben estar cerrados; en `HIGH_IMPACT_INCREMENT`, debe estar cerrado el incremento vertical seleccionado.
- `PARTIAL` requiere una causa objetiva verificable y continuidad explícita de la misma unidad; un checkpoint planificado o trabajo preparatorio no alcanza.
- Toda afirmación `IDLE` o `WORKING` debe incluir `Estado observado UTC`; presentala como una instantánea que puede cambiar después de la lectura.
- En `NO-OP` por lease activa, usá `ACTIVE_RUN` y mostrale al usuario únicamente estado, fase, expiración, timestamp observado y motivo; omití secciones sin contenido.
- Todo `NO-OP` debe declarar uno de los cinco códigos cerrados; una razón abierta como “no se encontró una unidad acotada” es inválida.
- En `SKILLS_MAINTENANCE`, roadmap y matriz de Iris son no aplicables salvo autorización adicional.
- En `COORDINATOR_REPAIR`, distinguí artefactos temporales observados de artefactos alcanzables al final.
- La imposibilidad de borrar auditoría interna de la plataforma no equivale a contenido controlado por el repositorio.
