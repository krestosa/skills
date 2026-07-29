# Focal — Mantenimiento autorizado de `krestosa/skills`

Este módulo se aplica solo en modo `SKILLS_MAINTENANCE`.

## Activación

El modo existe únicamente cuando la instrucción actual autoriza expresamente modificar `krestosa/skills` y define el objetivo. Una ejecución normal que solo invoca el entrypoint para desarrollar Focal permanece en `FOCAL_CYCLE`.

## Alcance

En este modo:

- `krestosa/skills` puede leerse y modificarse dentro del objetivo autorizado;
- `krestosa/Focal` y otros repositorios permanecen de solo lectura salvo autorización expresa adicional;
- no se adquiere la lease de Focal si no habrá mutaciones en Focal;
- no se heredan permisos de merge, release o mantenimiento hacia otros repositorios.

## Safeguard del conector en mantenimiento

`SKILLS_MAINTENANCE` no termina ante el primer fallo del conector.

- Reintentá lecturas y mutaciones transitorias hasta cuatro intentos totales con backoff de 2, 5, 10 y 20 segundos.
- Ante una mutación con respuesta de error, ejecutá `read-after-write` sobre la rama, archivo, commit o PR antes de repetirla.
- Si el efecto existe, continuá; si no existe y el SHA o head esperado sigue vigente, repetí exactamente la misma operación.
- No abras otra rama ni otra PR para compensar una operación de resultado desconocido.
- Solo detené el mantenimiento como `CONNECTOR_RETRY_EXHAUSTED` cuando los reintentos y verificaciones fueron agotados o el presupuesto ya no permite validar y publicar con seguridad.
- Una ejecución posterior debe retomar la misma rama o PR remota incompleta en vez de duplicar el trabajo.

## Procedimiento

1. Obtené rama predeterminada y SHA remoto actual de `krestosa/skills`.
2. Leé íntegramente el entrypoint, los módulos referenciados y cualquier archivo afectado directa o indirectamente.
3. Reconstruí referencias, precedencias y rutas activas.
4. Creá una rama desde el SHA observado.
5. Realizá cambios cohesivos y eliminá contradicciones en lugar de ocultarlas mediante precedencia.
6. No mantengas dos sistemas ejecutables en paralelo.
7. Conservá `prompts/focal-autonomous-development.md` como entrypoint estable.
8. Conservá `prompts/focal/11-process-flowchart.md` como representación derivada integral, nunca como fuente normativa paralela.
9. Si retirás contenido, preferí el historial Git. Archivá solo cuando tenga valor operativo y marcá el archivo como no canónico y no ejecutable.
10. Actualizá todas las referencias, el manifest, la integridad, el flowchart y la sección de troubleshooting del README.
11. Validá Markdown, Mermaid, rutas, términos canónicos, fases, estados y ausencia de referencias legacy activas.
12. Revisá el diff completo.
13. Publicá la rama y abrí una pull request.
14. Ejecutá o verificá CI disponible y corregí fallos causados.
15. No mergees con validaciones requeridas fallidas.

## Reglas de diseño del sistema

- Una fuente canónica por concepto.
- Entrypoint breve; módulos sin repetición integral.
- Política separada de procedimiento.
- Estado separado de documentación.
- Coordinación separada de especificación gráfica.
- Condiciones verificables y resultados no ambiguos.
- Sin snapshots históricos incorporados como instrucciones.
- Sin dependencias circulares.
- Sin negaciones superpuestas para reemplazar reglas legacy.
- Sin requerir releer contenido no relacionado en cada ciclo.
- Todo polling de GitHub Actions debe medir tiempo UTC o monotónico realmente transcurrido; varias lecturas inmediatas no prueban que un comando quedó sin procesar.
- El gate de lease debe observar comandos durante al menos 45 segundos, salvo que exista un run terminal fallido verificable.
- El gate de lease debe incluir una ruta bootstrap acotada para reparar el coordinador cuando `inspect` no se procesa y el issue está inequívocamente `idle`.
- Los workflows de coordinación deben ser compatibles con ediciones de GitHub Apps instaladas; no deben depender de una allowlist fija de `sender.login` incompatible con conectores autorizados.
- La reparación bootstrap nunca debe ampliar su alcance a desarrollo funcional sin lease.
- Toda reparación de Focal previa a la lease usa exclusivamente el conector de GitHub o GitHub Actions.
- Los commits, merges, workflows y refs temporales de `COORDINATOR_REPAIR` deben desaparecer de la historia alcanzable de `main` sin alterar el árbol funcional validado ni los metadatos que el contrato exige preservar.
- El workflow debe probar el modo real de invocación del coordinador, incluidos imports, checkout y `PYTHONPATH` cuando correspondan.
- El flowchart debe incluir carga de prompts, issue #7, inspect, polling, active lease, acquire, recover, coordinator repair, roadmap, Iris, implementación, OpenGL, CI, merge, reconciliación, release y todos los estados terminales.
- El README debe listar cada clase de bloqueo autónomo definida por el stack, evidencia mínima, solución y condición de reanudación.

## Migración compatible

Una tarea programada que lea `prompts/focal-autonomous-development.md` debe recibir todas las instrucciones necesarias mediante su orden de carga.

Antes de finalizar, verificá:

- entrypoint existente y legible;
- módulos `01` a `11` existentes y cargados en orden;
- todas las referencias resueltas;
- `ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT`;
- `ROADMAP_RECONCILIATION`;
- roadmap y matriz de Iris obligatorios;
- evidencia para completado;
- pruebas obligatorias;
- exclusión mutua y recuperación de lock;
- polling con demora real y ventana mínima explícita;
- `COORDINATOR_REPAIR` cargado y limitado a infraestructura de coordinación;
- compatibilidad con comandos emitidos por GitHub Apps autorizadas;
- ausencia de allowlists fijas de sender que bloqueen conectores autorizados;
- validación del modo real de ejecución del coordinador;
- limpieza obligatoria de commits temporales de reparación en Focal;
- flowchart Mermaid completo y consistente;
- sección de bloqueos y recuperación en `README.md`;
- reporte terminal único;
- autorización limitada de `krestosa/skills`;
- ausencia de referencias activas al estado legacy;
- ausencia de contradicciones activas;
- safeguard de reintentos, `read-after-write` y continuidad de la misma tarea ante fallos transitorios del conector.

## Pull request

El cuerpo debe explicar:

- problemas y contradicciones corregidos;
- arquitectura anterior y nueva;
- módulos creados, retirados o archivados;
- mecanismo de coordinación;
- política de historia temporal de Focal;
- comportamiento del roadmap y matriz de Iris;
- flowchart y troubleshooting;
- validaciones;
- riesgos de migración.
