# Programa y rutas de aprendizaje

## Público y prerrequisitos

La ruta inicial presupone cálculo multivariable, álgebra lineal, PDE básicas y
Python elemental. Antes del módulo 1 debes poder crear un entorno, operar
arreglos NumPy, interpretar gradiente/divergencia, ejecutar comandos y usar Git.
La [comprobación previa](practice/prior-knowledge.md) sirve únicamente para que
decidas qué fundamentos repasar; no produce nota ni registro.

La ruta rápida está pensada para quien ya conoce FEM o `dolfin` legado: completa
los módulos 0–4, estudia los cambios de API y salta al fenómeno de interés. La
[guía de estudio autónomo](self-study-guide.md) explica cómo registrar avances,
usar las soluciones y retomar un tema sin acompañamiento.

## Resultados de aprendizaje

Al terminar podrás explicar UFL/Basix/FFCx/DOLFINx/PETSc/MPI, escoger el objeto
correcto para cada cantidad, crear y etiquetar mallas, formular condiciones de
frontera, resolver problemas lineales/no lineales/transitorios, comprobar el
solver, guardar campos y defender cuantitativamente un benchmark.

## Secuencia de 44 horas

| Nivel | Módulos | Tiempo | Producto verificable |
| --- | --- | ---: | --- |
| Fundamentos | 0–4 | 16 h | Poisson con tasas L2/H1 |
| Intermedio | 5–8 | 16 h | difusión, sólidos y flujo con balances |
| Avanzado | 9–10 | 8 h | SNES, hiperelasticidad y Cahn–Hilliard |
| Cierre | 11 + proyecto | 4 h | reproducción serial/MPI y reporte |

Cada módulo contiene prerrequisitos, objetivos, modelo/unidades, forma fuerte y
débil, mapa de software, ejemplo, inspección, solver, verificación,
visualización, diagnóstico, ejercicios, solución y fuentes/versiones.

## Práctica y seguimiento personal

No hay exámenes, calificaciones ni entregas. Cada práctica ofrece una comprobación
automática o una cantidad esperada. Para integrar lo aprendido puedes usar la
[lista de proyecto](practice/project-checklist.md): no asigna puntajes, solo ayuda
a detectar formulaciones, resultados o pasos de reproducción pendientes.
