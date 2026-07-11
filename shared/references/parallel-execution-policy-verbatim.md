# Política obligatoria de ejecución paralela y control de concurrencia

Debes maximizar la ejecución paralela de tareas, llamadas a herramientas, skills, análisis y modificaciones de archivos siempre que no existan dependencias reales entre ellas.

Tu comportamiento por defecto debe ser:

1. Identificar todas las tareas necesarias.
2. Construir un grafo de dependencias.
3. Agrupar las tareas independientes en lotes paralelos.
4. Ejecutar simultáneamente todos los trabajos que no compitan por el mismo recurso.
5. Serializar únicamente las operaciones que tengan una dependencia directa o que modifiquen el mismo archivo o recurso compartido.

## Regla principal

No trabajes archivo por archivo de forma secuencial cuando varios archivos puedan modificarse independientemente.

Ejemplo:

* `src/auth.ts` puede modificarse en paralelo con `src/database.ts`.
* `tests/auth.test.ts` puede modificarse en paralelo con `docs/auth.md` si ninguna tarea depende del resultado de la otra.
* Dos operaciones que escriban sobre `src/auth.ts` no pueden ejecutarse al mismo tiempo.
* Si un mismo archivo requiere varias modificaciones, debes combinarlas en una sola edición cuando sea posible.
* Si no pueden combinarse de forma segura, debes aplicar las modificaciones de ese archivo secuencialmente y verificar su estado después de cada operación.

## Exclusión mutua por archivo

Cada archivo debe tratarse como un recurso con bloqueo exclusivo de escritura.

Mientras una tarea esté modificando un archivo:

* ninguna otra tarea puede escribir sobre ese mismo archivo;
* ninguna otra tarea puede aplicar un parche basado en una versión anterior del archivo;
* las operaciones posteriores sobre ese archivo deben esperar a que termine la operación activa;
* después de cada modificación, las operaciones siguientes deben leer o utilizar la versión actualizada.

Las tareas que modifiquen archivos diferentes deben ejecutarse en paralelo siempre que no exista una dependencia lógica entre ellas.

La unidad mínima de bloqueo es la ruta canónica completa del archivo.

Ejemplo conceptual:

```text
Lock(src/auth.ts)     → tarea A
Lock(src/database.ts) → tarea B
Lock(README.md)       → tarea C
```

Las tareas A, B y C pueden ejecutarse simultáneamente.

Si las tareas A y D modifican `src/auth.ts`, deben ejecutarse así:

```text
A → D
```

Mientras que una tarea B sobre otro archivo puede correr en paralelo:

```text
A ─→ D
B ─────────→
```

## Planificación por grafo de dependencias

Antes de ejecutar cambios relevantes:

* divide el trabajo en unidades independientes;
* identifica qué archivos, herramientas y recursos utiliza cada unidad;
* establece dependencias explícitas;
* ejecuta primero todos los nodos sin dependencias pendientes;
* al completar un nodo, habilita inmediatamente los nodos dependientes;
* evita barreras globales innecesarias.

No esperes a que termine un lote completo si una tarea dependiente ya puede comenzar con los resultados disponibles.

## Llamadas a herramientas

Cuando varias llamadas a herramientas sean independientes, debes emitirlas o ejecutarlas en paralelo.

Ejemplos:

* leer varios archivos;
* buscar símbolos en diferentes directorios;
* consultar metadatos independientes;
* ejecutar linters separados;
* cargar varias skills;
* analizar diferentes módulos;
* ejecutar tests no dependientes;
* inspeccionar varios errores;
* obtener estados de distintos recursos.

No ejecutes llamadas independientes una por una.

Usa ejecución secuencial solamente cuando:

* una llamada necesita el resultado de otra;
* ambas modifican el mismo recurso;
* existe una limitación explícita de la herramienta;
* la operación tiene efectos externos que exigen orden;
* la concurrencia podría producir condiciones de carrera;
* la segunda llamada debe operar sobre el estado actualizado por la primera.

## Uso de skills

Las skills independientes deben cargarse, analizarse o ejecutarse en paralelo cuando la infraestructura lo permita.

Antes de usar varias skills:

1. determina qué información necesita cada una;
2. identifica si comparten archivos o estado mutable;
3. ejecuta en paralelo las que no tengan conflictos;
4. serializa solo las que dependan de resultados previos o escriban sobre el mismo recurso.

No cargues ni ejecutes skills secuencialmente por costumbre.

## Modificación de varios archivos

Cuando una tarea requiera editar múltiples archivos para producir un commit:

1. inspecciona en paralelo todos los archivos relevantes;
2. agrupa las modificaciones por archivo;
3. asigna como máximo un escritor activo por archivo;
4. modifica en paralelo los archivos independientes;
5. espera a que terminen todas las escrituras necesarias;
6. ejecuta validaciones parciales en cuanto sus dependencias estén disponibles;
7. ejecuta validaciones globales después de integrar todos los cambios;
8. revisa el diff completo;
9. corrige los errores utilizando nuevamente paralelismo seguro;
10. crea el commit únicamente después de que las verificaciones requeridas hayan finalizado correctamente.

## Agrupación de cambios sobre un mismo archivo

Si varias tareas requieren modificar el mismo archivo, no debes lanzar ediciones simultáneas.

Debes elegir una de estas estrategias, en este orden:

1. Fusionar todas las modificaciones compatibles en una única edición atómica.
2. Asignar el archivo a una única tarea responsable de aplicar todos los cambios.
3. Aplicar una secuencia de parches ordenados, leyendo siempre el estado actualizado.
4. Esperar entre modificaciones cuando exista una dependencia semántica.

Nunca permitas que dos tareas generen parches simultáneos contra la misma versión base de un archivo.

## Lecturas concurrentes

Se permiten múltiples lecturas simultáneas sobre el mismo archivo siempre que no haya una escritura activa que pueda invalidar los resultados.

Si una lectura se utilizará para producir un parche:

* registra o comprueba la versión, hash o contenido base;
* antes de escribir, verifica que el archivo no haya cambiado;
* si cambió, vuelve a leerlo y recalcula el parche;
* nunca sobrescribas silenciosamente una modificación más reciente.

## Escrituras atómicas

Siempre que sea posible:

* escribe mediante archivos temporales y reemplazo atómico;
* aplica parches con contexto;
* verifica que el contexto esperado siga existiendo;
* evita reescribir archivos completos cuando un parche localizado sea suficiente;
* conserva formato, codificación y finales de línea;
* detecta conflictos antes de guardar.

## Paralelismo de validaciones

Después de editar:

* ejecuta en paralelo tests, linters, análisis estático, verificaciones de tipos y validaciones que sean independientes;
* ejecuta primero validaciones específicas de los archivos modificados;
* inicia validaciones globales cuando todos sus prerrequisitos estén completos;
* no repitas verificaciones costosas sin una modificación que pueda afectar su resultado.

Ejemplo:

```text
lint módulo A ─────┐
tests módulo A ────┤
lint módulo B ─────┤→ validación global → revisión de diff → commit
tests módulo B ────┘
```

## Corrección de errores

Si varias validaciones fallan por causas independientes:

* analiza los fallos en paralelo;
* corrige en paralelo cuando afecten archivos diferentes;
* serializa las correcciones que afecten el mismo archivo;
* vuelve a ejecutar solamente las validaciones relacionadas;
* después ejecuta las verificaciones globales necesarias.

## Control de recursos

Maximiza el paralelismo sin saturar el entorno.

Debes considerar:

* cantidad de CPU;
* memoria disponible;
* límites de procesos;
* límites de herramientas o APIs;
* rate limits;
* costo de contexto;
* bloqueos de archivos;
* duración estimada de las tareas;
* posibilidad de que una operación genere mucho output.

Usa un límite razonable de concurrencia cuando existan muchas tareas.

No confundas “máximo paralelismo” con “cantidad ilimitada de procesos”.

## Operaciones con efectos externos

Las operaciones irreversibles o con efectos externos deben tratarse por separado.

No ejecutes en paralelo sin control:

* commits concurrentes;
* pushes concurrentes sobre la misma rama;
* creación simultánea de ramas con el mismo nombre;
* migraciones sobre la misma base de datos;
* despliegues sobre el mismo entorno;
* modificaciones concurrentes del mismo issue, pull request o recurso remoto;
* comandos destructivos;
* publicaciones, envíos o acciones que requieran autorización.

Debe existir un único punto de commit o integración final.

## Estado compartido

Todo recurso mutable compartido debe tener un mecanismo de coordinación.

Esto incluye:

* archivos;
* directorios generados;
* índices;
* bases de datos;
* caches;
* archivos de lock;
* ramas Git;
* staging area;
* configuraciones;
* procesos de build que escriban en la misma carpeta;
* herramientas que modifiquen el workspace.

Dos tareas no deben escribir simultáneamente sobre el mismo estado compartido, aunque modifiquen archivos fuente distintos.

Por ejemplo, dos builds que escriben sobre la misma carpeta `dist/` deben serializarse o utilizar directorios de salida separados.

## Git

Para tareas que terminan en un commit:

* permite análisis y edición paralela;
* evita ejecutar múltiples operaciones simultáneas sobre el índice de Git;
* serializa `git add`, `git reset`, `git commit`, rebase, merge y operaciones equivalentes;
* revisa el estado del repositorio antes de modificarlo;
* no sobrescribas cambios preexistentes del usuario;
* no incluyas archivos ajenos a la tarea;
* revisa `git diff` y `git diff --cached`;
* crea un único commit coherente salvo que se solicite otra estructura.

## Prohibiciones

No debes:

* procesar tareas independientes secuencialmente por simplicidad;
* editar dos veces el mismo archivo en paralelo;
* lanzar parches concurrentes basados en contenido obsoleto;
* sobrescribir cambios realizados por otra tarea;
* usar paralelismo cuando existe una dependencia real;
* esperar innecesariamente a que termine una tarea no relacionada;
* crear barreras globales cuando basta con dependencias locales;
* ejecutar varios commits simultáneamente;
* afirmar que hubo paralelismo si las tareas fueron ejecutadas secuencialmente.

## Estrategia de ejecución requerida

Para cada tarea compleja, utiliza este procedimiento:

```text
1. Descubrir
2. Descomponer
3. Detectar dependencias
4. Detectar recursos compartidos
5. Asignar locks por recurso
6. Agrupar operaciones independientes
7. Ejecutar grupos en paralelo
8. Serializar conflictos locales
9. Validar en paralelo
10. Integrar
11. Revisar
12. Confirmar resultado
13. Crear commit
```

## Pseudocódigo de referencia

```javascript
const tasks = buildDependencyGraph(request);
const fileLocks = new Map();
const completed = new Set();

while (!allTasksCompleted(tasks)) {
  const runnable = tasks.filter(task =>
    dependenciesCompleted(task, completed) &&
    resourcesAvailable(task, fileLocks)
  );

  const selected = applyConcurrencyLimit(runnable);

  await Promise.all(
    selected.map(async task => {
      acquireLocks(task.resources, fileLocks);

      try {
        await execute(task);
        completed.add(task.id);
      } finally {
        releaseLocks(task.resources, fileLocks);
      }
    })
  );
}
```

Para modificaciones sobre múltiples archivos:

```javascript
const changesByFile = groupChangesByFile(plannedChanges);

await Promise.all(
  Object.entries(changesByFile).map(async ([file, changes]) => {
    await withExclusiveFileLock(file, async () => {
      const current = await readFile(file);
      const updated = applyAllCompatibleChanges(current, changes);
      await atomicWrite(file, updated);
    });
  })
);
```

## Criterio de decisión

Antes de ejecutar dos tareas en paralelo, verifica:

```text
¿Una necesita el resultado de la otra?
¿Escriben sobre el mismo archivo?
¿Modifican el mismo recurso compartido?
¿Una invalida el estado leído por la otra?
¿La herramienta impone ejecución secuencial?
¿Existe un efecto externo que requiera orden?
```

Si todas las respuestas son “no”, debes ejecutarlas en paralelo.

Si alguna respuesta es “sí”, serializa únicamente ese segmento del trabajo, no todo el proceso.

## Objetivo operativo

El objetivo es reducir el tiempo total de ejecución mediante paralelismo seguro, manteniendo:

* consistencia;
* determinismo;
* aislamiento entre tareas;
* ausencia de condiciones de carrera;
* protección de cambios existentes;
* validación completa;
* un resultado final integrado y coherente.

La ejecución paralela debe ser el comportamiento predeterminado. La ejecución secuencial debe ser una excepción justificada por dependencias, conflictos de recursos o restricciones explícitas.
