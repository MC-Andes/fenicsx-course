# Cómo estudiar este curso por tu cuenta

El curso es autocontenido y asíncrono: no presupone docente, sesiones, entregas
ni calificaciones. Tú eliges el ritmo y toda la retroalimentación disponible
está en los scripts, JSON, pistas y soluciones del repositorio.

## Ciclo recomendado por lección

1. Lee objetivos, forma fuerte y forma débil sin ejecutar código.
2. Predice signo, tendencia o valor de la métrica principal.
3. Ejecuta el ejemplo con `--quick` y abre su JSON; no leas aún todo el script.
4. Explica por qué pasaron `solver_converged` y `validation_passed`.
5. Resuelve al menos una práctica antes de consultar la solución.
6. Abre el script, localiza los ocho pasos del pipeline y relaciona cada bloque
   con la página.
7. Repite sin `--quick` o con una variación propia cuando el costo lo permita.

## La regla de una sola incógnita

Cuando te bloquees, no releas toda la página. Escribe una sola pregunta concreta:
“¿qué objeto no entiendo?”, “¿qué región se integra?” o “¿qué métrica falló?”.
Luego vuelve al punto de control relacionado. En la primera simulación, usa el
[laboratorio de Poisson paso a paso](guides/first-simulation.md), que separa:

1. dominio;
2. espacio;
3. objetos simbólicos;
4. forma débil;
5. frontera;
6. solver;
7. verificación;
8. salida y visualización.

No cambies dos componentes a la vez mientras aprendes. Si modificas la malla,
conserva elemento, PDE y solver; si modificas el grado, vuelve primero al caso
base. Así puedes atribuir el cambio observado a una sola decisión.

## Tres niveles de evidencia

| Nivel | Pregunta | Ejemplo |
| --- | --- | --- |
| ejecución | ¿el programa terminó? | no hubo excepción |
| álgebra | ¿el solver convergió? | razón PETSc positiva |
| modelo | ¿la solución es correcta? | tasa, balance o invariante aprobado |

Una figura complementa estos niveles, pero no sustituye ninguno. Úsala para
detectar simetrías rotas, fronteras equivocadas u oscilaciones; confirma después
con una cantidad numérica independiente.

## No estudies el catálogo en orden

El [repertorio](examples/index.md) es un índice para encontrar implementaciones,
no una lista de capítulos. Usa el [mapa del curso](learning-path.md), completa el
núcleo común y elige una ruta por física. Leer trece scripts completos de forma
consecutiva oculta los conceptos que se repiten.

## Registro personal opcional

Conserva un archivo fuera del repositorio con fecha, lección, comando, predicción,
resultado y duda pendiente. No se sube a ningún servicio. Los JSON de `results/`
pueden borrarse/regenerarse y tampoco contienen datos personales.

## Cuándo consultar una solución

Haz primero un intento acotado y anota dónde te bloqueaste. Luego compara la
formulación y la verificación, no solo líneas de código. Vuelve a cerrar la
solución y reconstruye el cambio. Las soluciones son rutas posibles, no claves
de calificación.

## Si algo falla

1. Conserva el primer traceback y la razón PETSc.
2. Ejecuta el sanity check y una variante `--quick`.
3. Revisa [solución de problemas](troubleshooting.md).
4. Vuelve al prerrequisito enlazado en la lección.
5. Reduce a un caso mínimo y, si persiste, abre un issue con versiones/JSON.

## Proyecto libre

Al terminar una ruta, adapta un ejemplo a un problema que te interese y recorre la
[lista personal](practice/project-checklist.md). El objetivo es poder defender la
corrección y reproducción ante ti mismo o cualquier lector futuro, no obtener
una nota.
