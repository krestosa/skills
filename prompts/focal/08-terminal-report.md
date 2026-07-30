# Focal — Reporte terminal legible

Emití **un único reporte Markdown renderizado**. No uses un bloque de código, no vuelques una secuencia plana de `Campo: valor` y no repitas la misma información en varias secciones.

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
| **PR / merge** | <PR y estado del merge, o no aplicable> |
| **CI** | <icono y run exacto: aprobado, fallido, pendiente o no aplicable> |
| **Coordinador** | <🟢 `IDLE`, 🔵 `WORKING`, 🔴 desconocido o no adquirido> |
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
- **Rama final:** `<rama>`.
- **Checkpoint / SHA final:** `<SHA>`.
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
| **SHA remoto inicial** | `<SHA>` |
| **SHA remoto final** | `<SHA>` |
| **Commit(s)** | `<SHAs funcionales>` |
| **Pull request** | `<número o no aplicable>` |
| **Estado del merge** | `<estado y SHA>` |
| **Estado de CI** | `<run y conclusión>` |
| **Roadmap** | `docs/ROADMAP.md` o no aplicable |
| **Matriz de Iris** | `docs/IRIS-CAPABILITY-MATRIX.md` o no aplicable |

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
| **Estado final observado** | `idle`, `working` o desconocido |

### Alcance técnico

- **Lote o incremento seleccionado:** <detalle>.
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
- No declares que un archivo, prueba o merge existe si no fue observado remotamente.
- No incluyas nombres de proveedor, modelo, aplicación, cliente, conector, actor, producto o plataforma de conversación. No reproduzcas campos legacy `owner`, `executionSource` ni logins del emisor.
- `runId` y `commandId` son opacos; no derives ni expliques su origen.
- Un error transitorio aislado no justifica un resultado terminal.
- `PASS` requiere publicación, aceptación, reconciliación y liberación completas. En `LOW_RISK_BULK`, todos los archivos e ítems del lote deben estar cerrados; en `HIGH_IMPACT_INCREMENT`, debe estar cerrado el incremento vertical seleccionado.
- `PARTIAL` requiere una causa objetiva verificable y continuidad explícita de la misma unidad; un checkpoint planificado o trabajo preparatorio no alcanza.
- En `NO-OP` por lease activa, mostrale al usuario únicamente estado, fase, expiración y motivo; omití secciones sin contenido.
- En `SKILLS_MAINTENANCE`, roadmap y matriz de Iris son no aplicables salvo autorización adicional.
- En `COORDINATOR_REPAIR`, distinguí artefactos temporales observados de artefactos alcanzables al final.
- La imposibilidad de borrar auditoría interna de la plataforma no equivale a contenido controlado por el repositorio.
