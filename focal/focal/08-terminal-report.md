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

Usá la URL remota observada; no inventes enlaces para recursos no verificados. Los identificadores opacos, timestamps, estados y códigos no son enlaces. Nunca insertes URLs ni sintaxis Markdown en JSON, bloques administrados, payloads machine-readable, evidencias estructuradas o bloques de código. Conservá JSON, payloads estructurados y bloques de código sin Markdown ni URLs añadidas.

## Jerarquía obligatoria

La primera pantalla debe permitir entender, sin abrir detalles:

1. resultado;
2. entrega observable;
3. objetivo y modo;
4. PR, merge y CI cuando apliquen;
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

> **Entrega:** <qué quedó efectivamente disponible, mergeado, eliminado, preservado o previsualizado>

| Resumen | Estado |
|---|---|
| **Objetivo** | <objetivo solicitado> |
| **Modo** | `FOCAL_CYCLE`, `REPOSITORY_MAINTENANCE` o `SKILLS_MAINTENANCE` |
| **Carril / scope** | `LOW_RISK_BULK`, `HIGH_IMPACT_INCREMENT`, `RECOVERY`, `branches`, `garbage`, `temporary_workflows`, `all` o no aplicable |
| **PR / merge** | <link a PR, merge y subject con `#<n>`, o no aplicable> |
| **CI / workflow** | <link al workflow y run exactos> |
| **Coordinador** | <🟢 `IDLE`, 🔵 `WORKING`, 🔴 desconocido o no adquirido> |
| **Estado observado UTC** | <timestamp exacto de la lectura; instantánea, no garantía futura> |
| **Duración** | <inicio UTC → fin UTC> |

> [!IMPORTANT]
> **Siguiente acción:** <una acción concreta, ejecutable y priorizada>

## Cambios principales

Para `FOCAL_CYCLE` o `SKILLS_MAINTENANCE`:

- <capacidad o cambio entregado>;
- <segundo cambio relevante>;
- <reconciliación cuando corresponda>.

Para `REPOSITORY_MAINTENANCE`:

- scope ejecutado y `dryRun`;
- ramas o paths candidatos;
- ramas o paths efectivamente eliminados;
- recursos preservados por protección, PR abierta o trabajo no mergeado.

No describas una ejecución administrativa como implementación. Una limpieza que no creó código no tiene “rama final” ni “PR de entrega”.

## Validación

| Comprobación | Resultado | Evidencia |
|---|---|---|
| <test, contrato o invariancia> | ✅ Aprobado / ❌ Falló / ⚪ No ejecutado | <run, comando o motivo> |
| <CI o workflow del head/comando exacto> | <resultado> | <run, SHA o command ID> |

Después de la tabla, agregá únicamente las aclaraciones necesarias:

- **Pruebas fallidas:** <ninguna o lista concisa>.
- **Pruebas no ejecutadas:** <ninguna o prueba + motivo factual>.
- **Nivel de evidencia:** `STATIC`, `GL_COMPILE_LINK`, `GL_RENDER_READBACK`, `IRIS_PATCHED`, `IRIS_CLIENT` o no aplicable.

En `REPOSITORY_MAINTENANCE` verificá explícitamente:

- `lastRepositoryMaintenanceCommandId` correlacionado;
- scope exacto;
- `createdBranches == []`;
- `branchCountAfter <= branchCountBefore`;
- para scope `branches`, `defaultBranchHeadAfter == defaultBranchHeadBefore`;
- ausencia de PR o workflow creados por la operación.

## Estado del proyecto

En modos funcionales:

- **Roadmap:** <ítems modificados y estados finales>.
- **Iris:** <capacidades verificadas o actualizadas>.
- **Rama final:** <link Markdown a la rama>.
- **Checkpoint / SHA final:** <link Markdown al commit>.
- **Bloqueos:** <ninguno o bloqueo comprobado>.

En `REPOSITORY_MAINTENANCE`, omití roadmap, Iris, rama final, checkpoint funcional y merge. Informá en su lugar el head de `main` antes/después cuando aplique y los conteos de ramas.

## Riesgos y limitaciones

- <limitación real que siga vigente>.
- <riesgo residual o evidencia todavía no alcanzada>.

Cuando no exista ninguno, escribí: `- Ninguno conocido dentro del alcance validado.`

## Próximo paso

> <acción concreta, por qué sigue y qué evidencia debe producir>

## Trazabilidad

### Trazabilidad funcional

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

### Trazabilidad administrativa

Usá esta tabla solo en `REPOSITORY_MAINTENANCE`:

| Recurso | Valor |
|---|---|
| **Issue de estado** | [issue #7](https://github.com/krestosa/Focal/issues/7) |
| **Issue administrativo** | [issue #101](https://github.com/krestosa/Focal/issues/101) |
| **Command ID** | `<identificador opaco>` |
| **Scope / dry-run** | <scope y boolean> |
| **Workflow / run** | <links observados> |
| **Ramas antes / después** | <conteos> |
| **Ramas creadas** | `[]` |
| **Ramas eliminadas** | <lista enlazada o ninguna> |
| **Paths eliminados** | <lista enlazada o ninguna> |
| **Head de main antes / después** | <links; iguales para scope branches> |

<details>
<summary><strong>Detalles operativos y de recuperación</strong></summary>

### Ejecución

| Campo | Valor |
|---|---|
| **Modo** | `FOCAL_CYCLE`, `REPOSITORY_MAINTENANCE` o `SKILLS_MAINTENANCE` |
| **Ruta excepcional** | no aplicable o `COORDINATOR_REPAIR` |
| **Runtime guard** | <límites y cumplimiento o no aplicable> |
| **Run ID funcional** | `<identificador opaco o no adquirido>` |
| **Command ID de adquisición** | `<identificador opaco o no adquirido>` |
| **Command ID de liberación** | `<identificador opaco o no aplicable>` |
| **Command ID administrativo** | `<identificador opaco o no aplicable>` |
| **Lock liberado** | sí, no o no adquirido |
| **Estado final observado** | `idle`, `working` o desconocido, con timestamp UTC exacto |

### Alcance técnico

- **Lote, incremento o scope:** <detalle>.
- **WORK_SELECTION_PROOF:** <detalle o no aplicable a mantenimiento administrativo>.
- **Código de NO-OP:** <código cerrado o no aplicable>.
- **Motivo objetivo de PARTIAL:** <no aplicable o evidencia>.
- **Revisión de calidad:** <hallazgos concretos>.
- **Archivos creados, modificados, movidos o eliminados:** <lista compacta>.

### Recuperación e historia

- **Reintentos del conector:** <cantidad>.
- **Mutaciones con resultado desconocido reconciliadas mediante read-after-write:** <ninguna o detalle>.
- **Fallos autónomamente recuperados:** <ninguno o detalle>.
- **Commits temporales de reparación:** <ninguno o SHAs>.
- **Historia final de Focal:** <limpia, pendiente o no aplicable>.
- **Candidatos saneados:** <ninguno o clasificación>.
- **Paths basura retirados y clasificación:** <ninguno o detalle>.
- **Refs temporales eliminadas:** <no aplicable o lista>.
- **Commit o merge de limpieza presente:** no, sí o no aplicable.
- **Árbol final verificado:** <sí/no + evidencia>.
- **Workflow temporal ausente:** sí, no o no aplicable.

### Rutas y limitaciones completas

- **Flowchart:** `prompts/focal/11-process-flowchart.md` o no aplicable.
- **Limitaciones reales:** <lista factual completa>.
- **Resultado observable entregado:** <detalle técnico>.

</details>

## Reglas de redacción

- Priorizá conclusiones y estado; relegá identificadores y mecánica al bloque desplegable.
- Usá tablas únicamente para datos comparables y listas breves para cambios o riesgos.
- Omití campos vacíos o irrelevantes.
- Usá SHA, PR, runs, issues y rutas verificables.
- En el Markdown visible, convertí todo recurso navegable verificado en enlace.
- No declares que un archivo, prueba, cleanup o merge existe si no fue observado remotamente.
- No declares `PASS` funcional si el subject de merge no contiene el número exacto del PR.
- No incluyas procedencia del cliente de ejecución.
- `runId` y `commandId` son opacos.
- Un error transitorio aislado no justifica un resultado terminal.
- `PASS` funcional requiere publicación, aceptación, reconciliación y cierre terminal completos.
- `PASS` administrativo requiere comando correlacionado, workflow exitoso, scope exacto e invariantes aprobadas.
- Toda afirmación `IDLE` o `WORKING` debe incluir `Estado observado UTC`.
- En `NO-OP` por lease activa, usá `ACTIVE_RUN` y omití secciones sin contenido.
- En `SKILLS_MAINTENANCE`, roadmap y matriz de Iris son no aplicables salvo autorización adicional.
- En `REPOSITORY_MAINTENANCE`, no inventes una rama, PR, commit o merge de entrega.
- La imposibilidad de borrar auditoría interna de la plataforma no equivale a contenido controlado por el repositorio.
