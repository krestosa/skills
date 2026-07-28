# Focal — Roadmap y reconciliación

Este módulo define `docs/ROADMAP.md`, la selección de trabajo y las dos fases obligatorias del ciclo.

## Documento canónico

```text
krestosa/Focal:docs/ROADMAP.md
```

No mantengas otro roadmap activo. Issues, proyectos y PRs pueden aportar evidencia, pero no reemplazan este documento.

## Estados canónicos

Usá exactamente:

```markdown
- [ ] ⚪ PENDIENTE
- [ ] 🟡 EN PROGRESO
- [x] 🟢 COMPLETADO
- [ ] 🟣 REVALIDAR
- [ ] 🔴 BLOQUEADO
```

No uses checkbox marcada para trabajo incompleto.

## Fase `ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT`

Después de adquirir la lease y antes de elegir trabajo funcional:

1. Resolvé nuevamente el SHA remoto actual de la rama predeterminada.
2. Inspeccioná el árbol, documentación, issues, ramas, PRs, commits, workflows, checks y releases relevantes.
3. Verificá si existe `docs/ROADMAP.md`.
4. Si no existe, crealo y publicalo antes de desarrollar una feature.
5. Si existe, leelo íntegramente.
6. Auditá duplicados, estados ambiguos, dependencias, evidencia y siguientes acciones.
7. Compará cada afirmación con el estado de la rama predeterminada.
8. Detectá funcionalidad implementada no registrada.
9. Desmarcá o mové a `REVALIDAR` cualquier completado sin evidencia suficiente.
10. Ejecutá la auditoría de Iris de `05-iris-capability-research.md`.
11. Verificá los vínculos entre roadmap y matriz de Iris.
12. Publicá el bootstrap o corrección documental si cambió.
13. Solo entonces seleccioná una unidad.

La ausencia o invalidez grave del roadmap es bloqueante para desarrollo funcional y constituye la unidad prioritaria del ciclo.

## Estructura de cada ítem

Cada ítem debe tener un identificador estable, por ejemplo `FOCAL-LIGHT-001`, y conservarlo al reordenarse.

Incluí, cuando corresponda:

- estado y prioridad;
- clasificación: obligatorio, deseable, experimental, descartado con fundamento o condicionado;
- título, alcance y resultado observable;
- dependencias;
- criterios de aceptación;
- pruebas requeridas;
- evidencia remota;
- capacidades de Iris relacionadas;
- passes, buffers, perfiles y fallbacks;
- archivos o subsistemas afectados;
- riesgos y presupuesto;
- siguiente acción concreta;
- motivo y evidencia del bloqueo.

No atomices en tareas microscópicas. Un ítem debe representar una unidad arquitectónica o funcional verificable.

## Cobertura mínima obligatoria

El roadmap debe cubrir, adaptado a la evidencia real:

1. **Fundación y distribución:** infraestructura del pack, versiones objetivo, estructura de programas y passes, buffers y render targets, CI, empaquetado, releases, licencias y atribuciones.
2. **Pipeline:** deferred o equivalente, shadow pipeline, composite/final, attachments, depth, historial, custom textures y gestión de recursos.
3. **Materiales:** PBR, mapas de normales y specular, roughness/metallic cuando correspondan, emisivos, AO, parallax y subsurface aproximado viable.
4. **Iluminación:** directa, indirecta, block light, skylight, GI aproximada, voxelización condicionada, oclusión ambiental y conservación de energía.
5. **Sombras:** mapas de sombra, cascaded shadow maps cuando sean viables, filtrado, penumbra, contacto, translucencia, estabilidad y fallbacks.
6. **Mundo:** cielo, nubes, atmósfera, niebla, clima, agua, hielo, vidrio, transparencias, partículas y volumetría.
7. **Temporal y postproceso:** exposición, tonemapping, gestión de color, bloom, reflejos, SSR, TAA, acumulación, reproyección, motion vectors, reducción de ghosting y sharpen.
8. **Cobertura de render:** terreno, entidades, block entities, mano, objetos sostenidos, partículas, clima, portales y escenas especiales.
9. **Dimensiones:** Overworld, Nether, End y dimensiones modificadas con fallback.
10. **Compatibilidad:** Iris, Sodium, resource packs con y sin materiales, integraciones confirmadas, GPU, drivers y degradación por hardware.
11. **Configuración:** perfiles de rendimiento, opciones, pantallas, traducciones, límites y defaults seguros.
12. **Calidad:** depuración, logs, análisis estático, compilación, capturas comparativas, benchmarks, pruebas visuales, regresiones y documentación técnica y de usuario.

Cada capacidad debe clasificarse; no presupongas que todas son obligatorias ni viables.

## Evidencia de completado

`🟢 COMPLETADO` exige simultáneamente:

- implementación presente en la rama predeterminada;
- criterios de aceptación satisfechos;
- pruebas requeridas aprobadas;
- workflow remoto exitoso cuando sea aplicable;
- documentación actualizada;
- evidencia enlazada;
- ausencia de bloqueo conocido que invalide el resultado.

No alcanza con código local, rama, commit sin merge, PR abierta, revisión parcial o impresión subjetiva.

## Prioridad de selección

Después de la fase inicial:

1. restaurar compilación, validación o estabilidad;
2. resolver bloqueos;
3. completar infraestructura compartida;
4. continuar `EN PROGRESO`;
5. revisar `REVALIDAR`;
6. implementar prioridad alta;
7. investigar documentación necesaria;
8. mejorar visual o rendimiento con medición.

No selecciones una unidad ausente del roadmap.

## Fase `ROADMAP_RECONCILIATION`

Después de implementación, pruebas, publicación, PR y merge disponible:

1. Obtené nuevamente el estado remoto.
2. Releé íntegramente `docs/ROADMAP.md`.
3. Compará plan, cambios, pruebas, PR, merge y rama predeterminada.
4. Actualizá todos los ítems afectados.
5. Usá `COMPLETADO` solo para evidencia ya presente en la rama predeterminada.
6. Conservá `EN PROGRESO` para avance remoto real todavía incompleto.
7. Volvé a `PENDIENTE` lo no iniciado.
8. Usá `REVALIDAR` para implementación sin validación suficiente o evidencia obsoleta.
9. Usá `BLOQUEADO` solo para restricción externa comprobada.
10. Agregá enlaces de evidencia y siguiente acción.
11. Actualizá la matriz de Iris cuando haya nueva evidencia.
12. Eliminá afirmaciones no respaldadas.
13. Confirmá coherencia con la rama predeterminada.

Si una implementación solo existe en una PR no mergeada, no puede figurar como completada.

Cuando el merge funcional ya ocurrió, realizá la reconciliación documental en una rama/PR posterior o equivalente y mergeala si los gates lo permiten. `PASS` exige que la reconciliación final esté publicada en la rama predeterminada. Si queda abierta, el ciclo es `PARTIAL`.
