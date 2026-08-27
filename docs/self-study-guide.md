# Cómo estudiar este curso por tu cuenta

El curso es autocontenido y asíncrono: no presupone docente, sesiones, entregas
ni calificaciones. Tú eliges el ritmo y toda la retroalimentación disponible
está en los scripts, JSON, pistas y soluciones del repositorio.

## Ciclo recomendado por módulo

1. Lee objetivos, forma fuerte y forma débil sin ejecutar código.
2. Predice signo, tendencia o valor de la métrica principal.
3. Ejecuta el ejemplo con `--quick` y abre su JSON.
4. Explica por qué pasaron `solver_converged` y `validation_passed`.
5. Resuelve al menos una práctica antes de consultar la solución.
6. Repite sin `--quick` o con una variación propia cuando el costo lo permita.

## Registro personal opcional

Conserva un archivo fuera del repositorio con fecha, módulo, comando, predicción,
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
4. Reduce a un caso mínimo y, si persiste, abre un issue con versiones/JSON.

## Proyecto libre

Al terminar, adapta un ejemplo a un problema que te interese y recorre la
[lista personal](practice/project-checklist.md). El objetivo es poder defender la
corrección y reproducción ante ti mismo o cualquier lector futuro, no obtener
una nota.
