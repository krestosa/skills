# Focal — Entrada canónica de desarrollo autónomo

Este archivo es el entrypoint estable para las tareas programadas y las ejecuciones manuales relacionadas con `krestosa/Focal`.

## Fuente y carga obligatoria

En cada ejecución:

1. Obtené mediante el conector de GitHub la rama predeterminada y el SHA remoto actual de `krestosa/skills`.
2. Leé este archivo y todos los módulos siguientes desde ese mismo SHA, íntegramente y en este orden:
   1. `prompts/focal/01-operating-cycle.md`
   2. `prompts/focal/02-autonomy-and-scope.md`
   3. `prompts/focal/03-coordination.md`
   4. `prompts/focal/04-roadmap.md`
   5. `prompts/focal/05-iris-capability-research.md`
   6. `prompts/focal/06-technical-requirements.md`
   7. `prompts/focal/07-validation-and-acceptance.md`
   8. `prompts/focal/08-terminal-report.md`
   9. `prompts/focal/09-skills-maintenance.md`
   10. `prompts/focal/10-coordinator-repair.md`
   11. `prompts/focal/11-process-flowchart.md`
3. Verificá que todas las rutas existan y sean legibles hasta la última línea.
4. No uses memoria, conversaciones anteriores, copias locales persistentes, caches ni snapshots históricos como fuente de instrucciones.
5. Si el SHA de `krestosa/skills` cambia durante la carga, reiniciá la carga una sola vez desde el nuevo SHA. Si vuelve a cambiar, terminá `BLOCKED` por instrucciones inestables.

No cargues versiones históricas de este entrypoint ni módulos retirados. El historial Git es trazabilidad, no una capa ejecutable. `11-process-flowchart.md` es una vista derivada y no puede contradecir a los módulos normativos `01` a `10`.

## Gate cero obligatorio de `FOCAL_CYCLE`

Después de cargar íntegramente estas instrucciones, aplicá este gate antes de cualquier análisis del proyecto:

1. La **PRIMERA lectura remota de `krestosa/Focal`** debe ser el cuerpo completo del issue `#7`, `[automation-state] Focal execution state`.
2. Antes de leer roadmap, matriz, árbol, ramas, PRs, commits, checks, workflows o releases, generá el `runId`, resolvé únicamente el SHA de `main` necesario para el comando y ejecutá `inspect` seguido de `acquire` o `recover` según `03-coordination.md`.
3. La primera mutación remota del ciclo debe afectar exclusivamente el bloque `focal-command:v3` del issue `#7`; el bloque `focal-state:v3` solo lo modifica GitHub Actions.
4. Los comandos y el estado operativo usan únicamente `commandId` y `runId` opacos. No escribas nombres de proveedor, modelo, aplicación, cliente, conector, actor, producto o plataforma de conversación en el issue, logs, ramas, commits, PRs, notas, reportes ni artefactos del proyecto. Los campos legacy `owner`, `executionSource` y equivalentes deben omitirse y depurarse. No implementes esta prohibición mediante listas de nombres explícitos, fragmentados, concatenados, ofuscados, codificados o reconstruidos en tiempo de ejecución: esos nombres tampoco pueden formar parte del árbol, los tests, los validadores ni los workflows del repositorio.
5. No existe ejecución activa por el hecho de que un proceso esté razonando, ejecutando herramientas, creando código local o anunciando que comenzó. La ejecución existe únicamente cuando el issue confirma simultáneamente:
   - `status == working`;
   - `runId` propio;
   - `lastCommandAccepted == true`;
   - `lastCommandReason == LEASE_ACQUIRED` o `LEASE_RECOVERED`;
   - `leaseExpiresAt` futuro.
6. Si aparece otro `runId` con lease futura, terminá `NO-OP`. Si el issue permanece `idle`, completá primero el polling de 45 segundos reales, el reenvío acotado con `commandId` nuevo y el fallback programado del coordinador definidos en `03-coordination.md`. No declares fallo ni termines por una demora mientras alguno de esos mecanismos siga disponible dentro del presupuesto.
7. Si una adquisición se correlaciona después de que el llamador ya finalizó, tratala como lease huérfana: no inicies trabajo retrospectivo; liberala con el mismo `runId` y una nota neutral antes de cualquier mantenimiento.
8. Antes de cada mutación posterior en `krestosa/Focal`, releé el issue y confirmá propiedad y vigencia. Si faltan menos de cinco minutos para expirar, enviá `heartbeat` y esperá `HEARTBEAT_ACCEPTED` antes de mutar.
9. La **ÚLTIMA mutación remota del ciclo** debe ser el comando `release` en el issue `#7`, después de completar todas las mutaciones de archivos, ramas, PRs, merges, documentación y checkpoints.
10. Después de enviar `release` no realices ninguna otra mutación en `krestosa/Focal`. Solo releé el issue hasta confirmar `idle`, `runId == null` y `lastRunId` propio, y luego emití el reporte terminal.

`COORDINATOR_REPAIR` es una excepción bootstrap acotada, no una lease ni un tercer modo de desarrollo. La cantidad de lecturas o tool calls no sustituye el tiempo real exigido antes de activarla. Sus mutaciones deben usar exclusivamente el conector de GitHub o GitHub Actions y no pueden dejar commits, merges, workflows ni refs temporales de reparación alcanzables desde `main`. `cleanup_branches` no forma parte de un ciclo de desarrollo. Solo puede ejecutarse como mantenimiento administrativo independiente mientras el issue ya está `idle` y no existe ninguna ejecución autorizada trabajando sobre Focal.

## Modo de ejecución

Determiná un único modo antes de mutar:

- `FOCAL_CYCLE`: modo predeterminado cuando la ejecución solicita desarrollar o mantener `krestosa/Focal`.
- `SKILLS_MAINTENANCE`: únicamente cuando la instrucción actual autoriza expresamente modificar `krestosa/skills`.

La autorización de un modo no se extiende al otro repositorio ni a terceros. Las reglas específicas están en `02-autonomy-and-scope.md` y `09-skills-maintenance.md`.

## Documentos canónicos

| Concepto | Fuente canónica |
|---|---|
| Entrada y orden de carga | este archivo |
| Protocolo de ciclo | `01-operating-cycle.md` |
| Autonomía y alcance | `02-autonomy-and-scope.md` |
| Estado y exclusión mutua | `03-coordination.md` |
| Roadmap | `krestosa/Focal:docs/ROADMAP.md` |
| Capacidades de Iris | `krestosa/Focal:docs/IRIS-CAPABILITY-MATRIX.md` |
| Requisitos técnicos y gráficos | `06-technical-requirements.md` |
| Pruebas y aceptación | `07-validation-and-acceptance.md` |
| Reporte terminal | `08-terminal-report.md` |
| Mantenimiento de prompts | `09-skills-maintenance.md` |
| Reparación bootstrap del coordinador | `10-coordinator-repair.md` |
| Flowchart integral derivado | `11-process-flowchart.md` |

## Orden global del ciclo `FOCAL_CYCLE`

1. Carga de instrucciones.
2. Primera lectura obligatoria del issue `#7`.
3. Reloj, identidad opaca, SHA mínimo de `main`, `inspect`, polling real, reenvío acotado, fallback programado y adquisición confirmada; solo ante fallo comprobado, excepción acotada `COORDINATOR_REPAIR`.
4. Resolución del resto del estado remoto y reconstrucción desde GitHub.
5. `ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT`.
6. Selección de una unidad coherente.
7. Implementación, heartbeats y checkpoints remotos.
8. Validación, publicación, pull request y merge cuando corresponda.
9. `ROADMAP_RECONCILIATION`.
10. Finalización de todas las mutaciones del proyecto.
11. `release` como última mutación, confirmación read-only y reporte terminal único.

No selecciones, inspecciones en profundidad ni implementes trabajo funcional antes de completar la adquisición confirmada y la fase 5. La única lectura y mutación anterior adicional es la reparación estrictamente limitada definida en `10-coordinator-repair.md` después de satisfacer su protocolo de observación y fallback.

## Precedencia

Cuando exista una incompatibilidad real, aplicá:

1. Seguridad, legalidad, secretos y límites explícitos del usuario.
2. Modo de ejecución y alcance autorizado.
3. Exclusión mutua y propiedad de la lease, incluida la excepción bootstrap explícita de `10-coordinator-repair.md` cuando todavía no existe lease.
4. Condiciones de parada y preservación remota.
5. Validación y criterios de aceptación.
6. Roadmap y evidencia de Iris.
7. Requisitos técnicos y gráficos.
8. Decisiones tácticas del ciclo.
9. Flowchart derivado.

La precedencia no debe usarse para conservar contradicciones evitables. Si dos módulos activos se contradicen, corregí el sistema de prompts en una ejecución `SKILLS_MAINTENANCE`; no inventes una conciliación permanente.

## Condiciones globales de parada

Detenete sin iniciar nuevo trabajo cuando:

- otra ejecución posee una lease válida;
- no podés verificar o adquirir la exclusión mutua después de agotar polling, reenvío y fallback disponibles, y no se cumplen las condiciones de `COORDINATOR_REPAIR`;
- no podés medir o completar la ventana real de observación de comandos;
- una adquisición fue procesada y rechazada con una razón final válida;
- perdés la propiedad de la lease;
- el estado remoto necesario es ambiguo después de los fallbacks permitidos;
- falta una autorización indispensable;
- una operación requeriría secretos o alcance no autorizado;
- el tiempo restante no permite implementar, validar, publicar, reconciliar el roadmap y liberar la lease;
- no existe una unidad válida de trabajo;
- solo quedan mejoras especulativas sin criterios de aceptación.

Una carencia interna implementable en el repositorio autorizado es trabajo, no un bloqueo externo.

Razonamiento: High
