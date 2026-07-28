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
3. Verificá que todas las rutas existan y sean legibles hasta la última línea.
4. No uses memoria, conversaciones anteriores, copias locales persistentes, caches ni snapshots históricos como fuente de instrucciones.
5. Si el SHA de `krestosa/skills` cambia durante la carga, reiniciá la carga una sola vez desde el nuevo SHA. Si vuelve a cambiar, terminá `BLOCKED` por instrucciones inestables.

No cargues versiones históricas de este entrypoint ni módulos retirados. El historial Git es trazabilidad, no una capa ejecutable.

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

## Orden global del ciclo `FOCAL_CYCLE`

1. Carga de instrucciones y reloj.
2. Resolución del estado remoto.
3. Inspección y adquisición de la exclusión mutua.
4. Reconstrucción desde GitHub.
5. `ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT`.
6. Selección de una unidad coherente.
7. Implementación y checkpoints remotos.
8. Validación, publicación, pull request y merge cuando corresponda.
9. `ROADMAP_RECONCILIATION`.
10. Liberación de la lease y reporte terminal único.

No selecciones ni implementes trabajo funcional antes de completar la fase 5.

## Precedencia

Cuando exista una incompatibilidad real, aplicá:

1. Seguridad, legalidad, secretos y límites explícitos del usuario.
2. Modo de ejecución y alcance autorizado.
3. Exclusión mutua y propiedad de la lease.
4. Condiciones de parada y preservación remota.
5. Validación y criterios de aceptación.
6. Roadmap y evidencia de Iris.
7. Requisitos técnicos y gráficos.
8. Decisiones tácticas del ciclo.

La precedencia no debe usarse para conservar contradicciones evitables. Si dos módulos activos se contradicen, corregí el sistema de prompts en una ejecución `SKILLS_MAINTENANCE`; no inventes una conciliación permanente.

## Condiciones globales de parada

Detenete sin iniciar nuevo trabajo cuando:

- otra ejecución posee una lease válida;
- no podés verificar o adquirir la exclusión mutua;
- perdés la propiedad de la lease;
- el estado remoto necesario es ambiguo después de los fallbacks permitidos;
- falta una autorización indispensable;
- una operación requeriría force push, reescritura destructiva, secretos o alcance no autorizado;
- el tiempo restante no permite implementar, validar, publicar, reconciliar el roadmap y liberar la lease;
- no existe una unidad válida de trabajo;
- solo quedan mejoras especulativas sin criterios de aceptación.

Una carencia interna implementable en el repositorio autorizado es trabajo, no un bloqueo externo.

Razonamiento: High
