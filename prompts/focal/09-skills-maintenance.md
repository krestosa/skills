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

## Procedimiento

1. Obtené rama predeterminada y SHA remoto actual de `krestosa/skills`.
2. Leé íntegramente el entrypoint, los módulos referenciados y cualquier archivo afectado directa o indirectamente.
3. Reconstruí referencias, precedencias y rutas activas.
4. Creá una rama desde el SHA observado.
5. Realizá cambios cohesivos y eliminá contradicciones en lugar de ocultarlas mediante precedencia.
6. No mantengas dos sistemas ejecutables en paralelo.
7. Conservá `prompts/focal-autonomous-development.md` como entrypoint estable.
8. Si retirás contenido, preferí el historial Git. Archivá solo cuando tenga valor operativo y marcá el archivo como no canónico y no ejecutable.
9. Actualizá todas las referencias.
10. Validá Markdown, rutas, términos canónicos, fases, estados y ausencia de referencias legacy activas.
11. Revisá el diff completo.
12. Publicá la rama y abrí una pull request.
13. Ejecutá o verificá CI disponible y corregí fallos causados.
14. No mergees con validaciones requeridas fallidas.

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

## Migración compatible

Una tarea programada que lea `prompts/focal-autonomous-development.md` debe recibir todas las instrucciones necesarias mediante su orden de carga.

Antes de finalizar, verificá:

- entrypoint existente y legible;
- todas las referencias resueltas;
- `ROADMAP_BOOTSTRAP_AND_IRIS_AUDIT`;
- `ROADMAP_RECONCILIATION`;
- roadmap y matriz de Iris obligatorios;
- evidencia para completado;
- pruebas obligatorias;
- exclusión mutua y recuperación de lock;
- reporte terminal único;
- autorización limitada de `krestosa/skills`;
- ausencia de referencias activas al estado legacy;
- ausencia de contradicciones activas.

## Pull request

El cuerpo debe explicar:

- problemas corregidos;
- arquitectura anterior y nueva;
- módulos creados, retirados o archivados;
- mecanismo de coordinación;
- comportamiento del roadmap y matriz de Iris;
- validaciones;
- riesgos de migración.
