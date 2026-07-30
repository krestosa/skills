# Focal — Flowchart integral del proceso autónomo

Este diagrama es una vista derivada del entrypoint y de los módulos normativos `01` a `10` y `12`. No crea reglas nuevas. Cuando exista una diferencia, la regla normativa es el módulo indicado en el nodo y la contradicción debe corregirse mediante `SKILLS_MAINTENANCE`.

```mermaid
flowchart TD
    START([Inicio]) --> LOAD_SHA[Resolver rama predeterminada y SHA actual de krestosa/skills]
    LOAD_SHA --> LOAD_ALL[Leer íntegramente entrypoint y módulos 01 a 11 desde el mismo SHA]
    LOAD_ALL --> LOAD_OK{¿Todos existen y se leyeron hasta la última línea?}
    LOAD_OK -- No --> BLOCKED_PROMPT[BLOCKED: prompt faltante, vacío, ilegible o inválido]
    LOAD_OK -- Sí --> SHA_CHANGED{¿Cambió el SHA durante la carga?}
    SHA_CHANGED -- Sí, primera vez --> RELOAD[Reiniciar una vez desde el nuevo SHA] --> LOAD_ALL
    SHA_CHANGED -- Sí, segunda vez --> BLOCKED_PROMPT
    SHA_CHANGED -- No --> MODE{Determinar modo autorizado}

    MODE -- SKILLS_MAINTENANCE --> SM1
    MODE -- FOCAL_CYCLE --> FC1
    LOAD_SHA -. error transitorio .-> CONNECTOR_ERROR
    LOAD_ALL -. cualquier fallo .-> ERROR_CAPTURE
    SM7 -. validación fallida .-> ERROR_CAPTURE
    CR_TEST -. prueba fallida .-> ERROR_CAPTURE
    HARNESS -. fallo gráfico .-> ERROR_CAPTURE
    VALIDATE -. fallo .-> ERROR_CAPTURE
    SM4 -. error transitorio .-> CONNECTOR_ERROR
    INSPECT -. error transitorio .-> CONNECTOR_ERROR
    MUTATION_GUARD -. error transitorio .-> CONNECTOR_ERROR
    RELEASE -. error transitorio .-> CONNECTOR_ERROR


    subgraph AUTONOMOUS_RECOVERY[Motor universal de recuperación — módulo 12]
        ERROR_CAPTURE[Capturar fallo y pausar solo dependencias]
        ERROR_CAPTURE --> ERROR_REMOTE[Releer estado remoto autoritativo]
        ERROR_REMOTE --> ERROR_CLASSIFY{¿Código específico conocido?}
        ERROR_CLASSIFY -- Sí --> ERROR_EVIDENCE[Reunir evidencia mínima reproducible]
        ERROR_CLASSIFY -- No --> ERROR_UNKNOWN[UNCLASSIFIED_INTERNAL_FAILURE: reducir, formular hipótesis y crear prueba]
        ERROR_UNKNOWN --> ERROR_EVIDENCE
        ERROR_EVIDENCE --> ERROR_ROUTE[Aplicar escalera: retry, read-after-write, ruta alternativa, repair, reconstruct, sanitize, degrade, checkpoint]
        ERROR_ROUTE --> ERROR_FIXED{¿Causa corregida y artefacto exacto validado?}
        ERROR_FIXED -- Sí --> ERROR_RESUME[Reanudar desde el primer gate invalidado]
        ERROR_FIXED -- No, hipótesis agotada --> ERROR_RECLASSIFY[Reunir evidencia nueva y cambiar hipótesis] --> ERROR_EVIDENCE
        ERROR_FIXED -- No, tiempo insuficiente --> ERROR_CHECKPOINT[Publicar checkpoint recuperable y continuar en siguiente ejecución]
        ERROR_FIXED -- No, capacidad externa imposible --> ERROR_EXTERNAL[EXTERNAL_BLOCKER exacto y mínimo]
    end

    subgraph CONNECTOR_RETRY[Safeguard transversal del conector — módulos 01, 03, 09 y 10]
        CONNECTOR_ERROR{¿Llamada remota devuelve error transitorio?}
        CONNECTOR_ERROR -- No --> CONNECTOR_CONTINUE[Continuar la misma tarea]
        CONNECTOR_ERROR -- Sí, lectura --> CONNECTOR_BACKOFF[Backoff 2, 5, 10 y 20 segundos; máximo 4 intentos]
        CONNECTOR_ERROR -- Sí, mutación --> READ_AFTER_WRITE[Marcar OUTCOME_UNKNOWN y ejecutar read-after-write]
        READ_AFTER_WRITE --> EFFECT_OBSERVED{¿Efecto remoto observado?}
        EFFECT_OBSERVED -- Sí --> CONNECTOR_CONTINUE
        EFFECT_OBSERVED -- No, guardas vigentes --> RETRY_SAME_OPERATION[Reintentar la misma operación, payload e identificador idempotente]
        RETRY_SAME_OPERATION --> CONNECTOR_BACKOFF
        CONNECTOR_BACKOFF --> CONNECTOR_ERROR
        EFFECT_OBSERVED -- No, presupuesto agotado --> CONNECTOR_RETRY_EXHAUSTED[Preservar checkpoint; PARTIAL o BLOCKED según evidencia]
    end

    subgraph HISTORY_SANITATION[Saneamiento histórico sin huellas — módulos 01, 09 y 10]
        HISTORY_SCAN{¿Hay commit no-op, transporte fallido o archivo basura alcanzable?}
        HISTORY_SCAN -- No --> HISTORY_CLEAR[Historia limpia]
        HISTORY_SCAN -- Sí --> HISTORY_CLASSIFY[Clasificar por tree, diff, refs y runs; nunca por mensaje]
        HISTORY_CLASSIFY --> HISTORY_GARBAGE{¿Commit solo basura o commit mixto?}
        HISTORY_GARBAGE -- Solo basura --> HISTORY_SAFE{¿Tramo lineal o parents de merge completamente mapeables?}
        HISTORY_GARBAGE -- Mixto --> HISTORY_REBUILD_MIXED[Reconstruir árbol sin paths basura y preservar diff funcional] --> HISTORY_SAFE
        HISTORY_SAFE -- No --> HISTORY_ABORT[Abortar sin mover refs]
        HISTORY_SAFE -- Sí --> HISTORY_REPLAY[GitHub Actions omite candidatos y reaplica cada diff posterior]
        HISTORY_REPLAY --> HISTORY_DATES[Preservar GIT_AUTHOR_DATE y GIT_COMMITTER_DATE exactos de cada commit posterior]
        HISTORY_DATES --> HISTORY_VERIFY_TREE[Verificar diffs semánticos y árbol final validado]
        HISTORY_VERIFY_TREE --> HISTORY_FORCE_LEASE[Actualizar ref con force-with-lease contra expectedOldHead]
        HISTORY_FORCE_LEASE --> HISTORY_DELETE_REFS[Eliminar workflow, scripts, ramas y tags temporales; sin commit de limpieza]
        HISTORY_DELETE_REFS --> HISTORY_REACHABILITY{¿Candidatos ausentes de refs/heads y refs/tags?}
        HISTORY_REACHABILITY -- No --> HISTORY_ABORT
        HISTORY_REACHABILITY -- Sí --> HISTORY_CLEAR
    end

    subgraph SKILLS[SKILLS_MAINTENANCE — módulo 09]
        SM1[Confirmar autorización expresa para modificar krestosa/skills]
        SM1 --> SM2[Leer referencias, manifest, validadores y archivos afectados]
        SM2 --> SM3[Detectar contradicciones, rutas rotas y sistemas paralelos]
        SM3 --> SM4[Crear rama desde el SHA remoto observado]
        SM4 --> SM5[Aplicar cambios cohesivos]
        SM5 --> SM6[Actualizar entrypoint, módulos, flowchart, README, validadores e integridad]
        SM6 --> SM7[Validar Markdown, referencias, contratos, privacidad y determinismo]
        SM7 --> SM_ARTIFACTS{¿La rama contiene artefactos históricos candidatos?}
        SM_ARTIFACTS -- No --> SM8[Abrir o actualizar PR]
        SM_ARTIFACTS -- Sí --> SM_SANITIZE[Ejecutar HISTORY_SANITATION sobre la rama propia] --> SM8
        SM8 --> SM9{¿CI del head exacto está aprobada?}
        SM9 -- No --> SM10[Corregir fallos causados] --> SM6
        SM9 -- Sí --> SM11[Mergear y verificar main]
        SM11 --> REPORT_SKILLS[Reporte terminal único]
    end

    subgraph PREFLIGHT[Preflight FOCAL_CYCLE — módulos 01 y 02]
        FC1[Generar runId y commandId opacos, tiempos UTC y reloj monotónico]
        FC1 --> PRIVACY[Prohibir procedencia: sin proveedor, modelo, app, cliente, conector, actor o plataforma]
        PRIVACY --> FC2[Fijar soft stop 50m, cleanup 55m y hard stop 58m30s]
        FC2 --> FC3[PRIMERA llamada remota a krestosa/Focal: leer issue #7 completo]
        FC3 --> FC4{¿Título, bloques v3 y schemaVersion 3 son válidos?}
        FC4 -- Sí --> FC5[Resolver únicamente rama predeterminada y SHA de main]
        FC4 -- No --> CR_GATE
    end

    subgraph COORDINATION[Gate de coordinación — módulos 01 y 03]
        FC5 --> INSPECT[Primera mutación: escribir inspect sin procedencia]
        INSPECT --> POLL1[Polling real cada 5 a 10 segundos]
        POLL1 --> OBSERVED{¿STATE_OBSERVED correlacionado?}
        OBSERVED -- No --> WAIT1{¿Pasaron 45 segundos reales?}
        WAIT1 -- No --> POLL1
        WAIT1 -- Sí --> SAFE_RETRY{¿Issue idle, runId null y sin actividad mutadora?}
        SAFE_RETRY -- No --> CR_GATE
        SAFE_RETRY -- Sí --> RETRY[Reenviar una sola vez con commandId y timestamps nuevos]
        RETRY --> POLL2[Segunda ventana de 45 segundos reales]
        POLL2 --> RETRY_OK{¿Comando correlacionado?}
        RETRY_OK -- Sí --> STATE_KIND
        RETRY_OK -- No --> FALLBACK{¿Existe schedule cada 5m y quedan al menos 10m?}
        FALLBACK -- Sí --> SCHEDULE_WAIT[Observar hasta 6 minutos el fallback programado]
        SCHEDULE_WAIT --> FALLBACK_OK{¿Comando correlacionado?}
        FALLBACK_OK -- Sí --> STATE_KIND
        FALLBACK_OK -- No --> CR_GATE
        FALLBACK -- No --> CR_GATE
        OBSERVED -- Sí --> STATE_KIND[Evaluar focal-state:v3]
        STATE_KIND --> FOREIGN{¿Existe lease ajena futura?}
        FOREIGN -- Sí --> NOOP[NO-OP: no analizar ni mutar trabajo funcional]
        FOREIGN -- No --> IDLE{¿status idle y runId null?}
        IDLE -- Sí --> ACQUIRE[Enviar acquire sin owner ni executionSource]
        IDLE -- No --> EXPIRED{¿Lease vencida y recuperable?}
        EXPIRED -- Sí --> RECOVER[Auditar referencias mínimas y enviar recover]
        EXPIRED -- No --> BLOCKED_LOCK[BLOCKED o NO-OP: propiedad insegura]
        ACQUIRE --> LOCK_DELIVERY[Aplicar polling, reenvío único y fallback programado]
        RECOVER --> LOCK_DELIVERY
        LOCK_DELIVERY --> OWNED{¿LEASE_ACQUIRED o LEASE_RECOVERED + working + runId propio?}
        OWNED -- No --> CR_GATE
        OWNED -- Sí --> LATE{¿El llamador ya terminó?}
        LATE -- Sí --> ORPHAN_RELEASE[Liberar lease huérfana con nota neutral] --> NOOP_RESULT
        LATE -- No --> HB_AUDIT[Heartbeat REMOTE_STATE_AUDIT]
        HB_AUDIT --> HB_OK{¿HEARTBEAT_ACCEPTED?}
        HB_OK -- No --> LOST
        HB_OK -- Sí --> REMOTE_AUDIT
    end

    subgraph REPAIR[COORDINATOR_REPAIR — módulo 10]
        CR_GATE{¿Se agotaron polling, retry y fallback; issue idle; sin actividad positiva; autorización vigente?}
        CR_GATE -- No --> BLOCKED_COORD[BLOCKED: no iniciar desarrollo funcional]
        CR_GATE -- Sí --> CR_DIAG[Diagnosticar evento, schedule, permisos, YAML, imports, PYTHONPATH, API e idempotencia]
        CR_DIAG --> CR_FIX[Aplicar fix mínimo por conector de GitHub o GitHub Actions]
        CR_FIX --> CR_PRIVACY[Eliminar procedencia legacy y prohibir logs de sender]
        CR_PRIVACY --> CR_TEST[Probar inspect, acquire, lease ajena, heartbeat, release, retry, schedule e idempotencia]
        CR_TEST --> CR_GREEN{¿Checks del árbol exacto están verdes?}
        CR_GREEN -- No --> CR_FIX
        CR_GREEN -- Sí --> CR_PUBLISH[Publicar árbol reparado]
        CR_PUBLISH --> HISTORY_SCAN
        HISTORY_CLEAR --> CR_SMOKE[Smoke test inspect y ciclo diagnóstico seguro]
        HISTORY_ABORT --> BLOCKED_COORD
        CR_SMOKE --> CR_IDLE{¿STATE_OBSERVED y luego LEASE_RELEASED en idle?}
        CR_IDLE -- No --> BLOCKED_COORD
        CR_IDLE -- Sí --> CR_RESTART[Generar runId funcional nuevo y volver al issue #7]
        CR_RESTART --> FC3
    end

    subgraph REMOTE[Auditoría remota autorizada]
        REMOTE_AUDIT[Releer SHA de main]
        REMOTE_AUDIT --> RA2[Inspeccionar ramas, PRs, commits, checks, workflows, releases, roadmap y matriz]
        RA2 --> RA3{¿Existe trabajo remoto incompleto compatible?}
        RA3 -- Sí --> RA4[Retomar y preservar; marcar REVALIDAR cuando corresponda]
        RA3 -- No --> ROADMAP_START
        RA4 --> ROADMAP_START
    end

    subgraph ROADMAP[ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT — módulos 04 y 05]
        ROADMAP_START[Leer o crear docs/ROADMAP.md]
        ROADMAP_START --> RI2[Leer o crear docs/IRIS-CAPABILITY-MATRIX.md]
        RI2 --> RI3[Auditar estados y evidencia contra main]
        RI3 --> RI4[Verificar capacidades con documentación primaria de Iris]
        RI4 --> RI5[Enlazar roadmap, matriz y campo Iris docs]
        RI5 --> WORK_SELECTION_PROOF[WORK_SELECTION_PROOF: evaluar al menos tres candidatos o todos los restantes]
        WORK_SELECTION_PROOF --> SLICE_FOUND{¿Existe un slice vertical observable y validable?}
        SLICE_FOUND -- Sí --> UNIT_RISK
        SLICE_FOUND -- Ítem demasiado amplio --> DECOMPOSE_VERTICAL[Descomponer por capacidad funcional y aceptación] --> UNIT_RISK
        SLICE_FOUND -- Prueba ausente o razón abierta --> ROADMAP_GRANULARITY_FAILURE[ROADMAP_GRANULARITY_FAILURE] --> ERROR_CAPTURE
        SLICE_FOUND -- No queda trabajo --> NOOP_CAUSE{¿Causa cerrada de NO-OP?}
        NOOP_CAUSE -- PROJECT_ALREADY_COMPLETE --> NOOP_RESULT
        NOOP_CAUSE -- NO_AUTHORIZED_WORK --> NOOP_RESULT
        NOOP_CAUSE -- ALL_REMAINING_WORK_EXTERNALLY_BLOCKED --> NOOP_RESULT
        NOOP_CAUSE -- Otra --> ROADMAP_GRANULARITY_FAILURE
    end

    subgraph IMPLEMENTATION[Selección adaptativa e implementación — módulos 01, 02 y 06]
        UNIT_RISK{Clasificar riesgo e impacto}
        UNIT_RISK -- Bajo, independiente y reversible --> LOW_RISK_BULK[LOW_RISK_BULK: agrupar correcciones compatibles]
        UNIT_RISK -- Arquitectura, runtime, compatibilidad o intención crítica --> HIGH_IMPACT_INCREMENT[HIGH_IMPACT_INCREMENT: definir incremento vertical observable]
        LOW_RISK_BULK --> UNIT_DEFINE[Definir lote cerrado, archivos, aceptación, pruebas y parada]
        HIGH_IMPACT_INCREMENT --> UNIT_DEFINE
        UNIT_DEFINE --> UNIT_BRANCH[Retomar o crear rama no forzada]
        UNIT_BRANCH --> MUTATION_GUARD[Antes de cada mutación: releer issue y comprobar runId propio + lease futura]
        MUTATION_GUARD --> MARGIN{¿Propiedad y margen ≥5m?}
        MARGIN -- No, margen bajo --> RENEW[Heartbeat con fase y checkpoint] --> RENEW_OK{¿HEARTBEAT_ACCEPTED?}
        RENEW_OK -- No --> LOST
        RENEW_OK -- Sí --> MARK_PROGRESS
        MARGIN -- No, propiedad perdida --> LOST
        MARGIN -- Sí --> MARK_PROGRESS[Marcar ítems EN PROGRESO y registrar carril]
        MARK_PROGRESS --> COMMIT_MODE{¿Qué carril se ejecuta?}
        COMMIT_MODE -- LOW_RISK_BULK --> LOW_COMMITS[Implementar lote: un archivo por commit y validación individual]
        COMMIT_MODE -- HIGH_IMPACT_INCREMENT --> HIGH_COMMITS[Implementar incremento: commits lógicos multarchivo cuando la atomicidad lo exige]
        LOW_COMMITS --> QUALITY_GATE[Revisar propósito, simplicidad, errores, deuda, placeholders, código muerto, abstracciones y tests]
        HIGH_COMMITS --> QUALITY_GATE
        QUALITY_GATE --> QUALITY_OK{¿Calidad e intención preservadas?}
        QUALITY_OK -- No --> QUALITY_FIX[Eliminar relleno y corregir diseño o pruebas] --> COMMIT_MODE
        QUALITY_OK -- Sí --> OPENGL{¿Requiere validación gráfica?}
        OPENGL -- Sí --> HARNESS[OPENGL_RUNTIME_HARNESS: focal-gl probe, compile, render y suite]
        OPENGL -- No --> VALIDATE_PREP
        HARNESS --> VALIDATE_PREP[Checkpoint solo ante contingencia real; nunca como objetivo planificado]
        VALIDATE_PREP --> VALIDATE
    end

    subgraph VALIDATION[Validación, PR y merge — módulo 07]
        VALIDATE[Ejecutar tests, contratos, OpenGL y pruebas aplicables]
        VALIDATE --> DIFF[Revisar diff, referencias, seguridad y rendimiento]
        DIFF --> PR[Crear o actualizar PR con contenido neutral]
        PR --> CI[Inspeccionar checks del head exacto]
        CI --> CI_RESULT{¿Checks requeridos aprobados?}
        CI_RESULT -- Fallo causado --> FIX[Corregir] --> MUTATION_GUARD
        CI_RESULT -- Pendiente o evidencia faltante --> PARTIAL_CAUSE{¿Existe causa objetiva para no cerrar?}
        PARTIAL_CAUSE -- No --> FIX
        PARTIAL_CAUSE -- Sí --> PARTIAL_CP[Preservar rama, PR y checkpoint recuperables] --> RECONCILE
        CI_RESULT -- Sí --> MERGE_GUARD[Releer issue y verificar head]
        MERGE_GUARD --> MERGE_OK{¿Propiedad y gates válidos?}
        MERGE_OK -- No --> LOST
        MERGE_OK -- Sí --> MERGE[Merge autónomo]
        MERGE --> POST_MERGE[Verificar main y CI post-merge]
        POST_MERGE --> RECONCILE
    end

    subgraph RECONCILIATION[ROADMAP_RECONCILIATION — módulos 04 y 05]
        RECONCILE[Releer estado remoto final]
        RECONCILE --> RC2[Actualizar roadmap según evidencia en main]
        RC2 --> RC3[Actualizar matriz Iris y enlaces]
        RC3 --> RC4[Asignar PENDIENTE, EN PROGRESO, COMPLETADO, REVALIDAR o BLOQUEADO]
        RC4 --> FINALIZE
    end

    subgraph FINALIZATION[Cierre obligatorio — módulos 01, 03 y 08]
        FINALIZE[Detener procesos y confirmar checkpoints remotos]
        FINALIZE --> FINAL_GUARD[Releer issue y confirmar propiedad]
        FINAL_GUARD --> CAN_RELEASE{¿Sigue siendo propietario?}
        CAN_RELEASE -- No --> LOST_NO_RELEASE[No liberar lease ajena]
        CAN_RELEASE -- Sí --> RELEASE[ÚLTIMA mutación: release]
        RELEASE --> RELEASE_POLL[Después de release: solo lecturas]
        RELEASE_POLL --> RELEASE_OK{¿idle + runId null + lastRunId propio + LEASE_RELEASED?}
        RELEASE_OK -- No --> RELEASE_UNKNOWN[Confirmación incompleta]
        RELEASE_OK -- Sí --> REPORT[Reporte terminal único sin procedencia del cliente]
    end

    LOST --> EVIDENCE_RESULT{¿Existe checkpoint remoto útil?}
    LOST_NO_RELEASE --> EVIDENCE_RESULT
    RELEASE_UNKNOWN --> EVIDENCE_RESULT
    EVIDENCE_RESULT -- Sí --> PARTIAL_RESULT([PARTIAL])
    EVIDENCE_RESULT -- No --> BLOCKED_RESULT([BLOCKED])
    REPORT --> RESULT_GATE{¿Lote o incremento seleccionado completo, mergeado y reconciliado?}
    RESULT_GATE -- Sí --> PASS_RESULT([PASS])
    RESULT_GATE -- No, causa objetiva y checkpoint útil --> PARTIAL_RESULT
    RESULT_GATE -- No, bloqueo externo sin alternativa --> BLOCKED_RESULT
    REPORT_SKILLS --> PASS_RESULT
    NOOP --> NOOP_RESULT([NO-OP])
    BLOCKED_PROMPT --> BLOCKED_RESULT
    BLOCKED_LOCK --> BLOCKED_RESULT
    BLOCKED_COORD --> BLOCKED_RESULT
    PASS_RESULT --> END([Fin])
    PARTIAL_RESULT --> END
    BLOCKED_RESULT --> END
    NOOP_RESULT --> END
```

## Lectura del diagrama

- `runId` y `commandId` son opacos. El proceso no registra la herramienta que originó la ejecución.
- Un retraso de evento no es un fallo inmediato: primero se completa polling, un reenvío y el fallback programado.
- `NO-OP` usa causas cerradas. Si el roadmap conserva trabajo, `WORK_SELECTION_PROOF` debe encontrar o crear un slice vertical; no hallar alcance es `ROADMAP_GRANULARITY_FAILURE`.
- Todo estado `IDLE` o `WORKING` del reporte lleva timestamp UTC de observación porque es una instantánea.
- Un error transitorio del conector tampoco es terminal: se reintenta la misma tarea, y toda mutación de resultado desconocido se reconcilia mediante `read-after-write` antes de repetirla.
- Un commit vacío, no-op, de transporte fallido o con archivos basura probados se sanea por GitHub Actions sin dejar commit de limpieza ni refs temporales. Esto incluye placeholders como `X`, tool output, dumps, truncados y paths accidentales solo cuando la evidencia conjunta confirma que no tienen función. Los commits posteriores conservan timestamps originales.
- Todo fallo conocido o futuro entra en `AUTONOMOUS_RECOVERY_LOOP`; lo no catalogado usa `UNCLASSIFIED_INTERNAL_FAILURE`, se diagnostica y se reanuda sin pedir al usuario decisiones técnicas ordinarias.
- `COORDINATOR_REPAIR` no es una lease ni una tercera modalidad funcional. Es una excepción bootstrap limitada al coordinador.
- Los commits funcionales ordinarios permanecen sujetos a rama, PR, CI y merge. En `LOW_RISK_BULK` cada archivo usa un commit dedicado; en `HIGH_IMPACT_INCREMENT` los commits pueden abarcar archivos relacionados para preservar atomicidad e intención.
- La calidad exige ausencia de código de relleno, placeholders, deuda oculta, abstracciones especulativas y tests superficiales. Un checkpoint es contingencia, no objetivo.
- Solo los artefactos temporales de reparación deben desaparecer de la historia alcanzable de `main`.
- `release` es siempre la última mutación remota de un ciclo funcional.
