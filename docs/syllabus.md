# Programa por etapas

## Público y prerrequisitos

La ruta inicial presupone cálculo multivariable, álgebra lineal, PDE básicas y
Python elemental. Antes de la lección 1 debes poder crear un entorno, operar
arreglos NumPy, interpretar gradiente/divergencia, ejecutar comandos y usar Git.
La [comprobación previa](practice/prior-knowledge.md) sirve únicamente para que
decidas qué fundamentos repasar; no produce nota ni registro.

La ruta rápida está pensada para quien ya conoce FEM o `dolfin` legado: completa
las lecciones 0, 2 y 3, estudia los cambios de API y salta al fenómeno de interés. La
[guía de estudio autónomo](self-study-guide.md) explica cómo registrar avances,
usar las soluciones y retomar un tema sin acompañamiento.

## Resultados de aprendizaje

Al terminar podrás explicar UFL/Basix/FFCx/DOLFINx/PETSc/MPI, escoger el objeto
correcto para cada cantidad, crear y etiquetar mallas, formular condiciones de
frontera, resolver problemas lineales/no lineales/transitorios, comprobar el
solver, guardar campos y defender cuantitativamente un benchmark.

## Secuencia común

| Lección | Tema | Tiempo | Depende de | Producto |
| ---: | --- | ---: | --- | --- |
| 0 | ecosistema, entorno y MPI | 1 h | instalación | sanity check |
| 1 | campos, operadores y forma débil | 1.5 h | cálculo | derivación de Poisson |
| 2 | primer problema completo: Poisson | 3 h | 0–1 | solve y error L2/H1 |
| 3 | objetos de DOLFINx y UFL | 2 h | 2 | interpolación P1/P2 |
| 4 | mallas, etiquetas y fronteras | 3 h | 2–3 | medidas verificadas |
| 5 | elementos, espacios y convergencia | 3 h | 3–4 | comparación de DOF/tasas |

La primera vuelta muestra el ciclo completo. La segunda desarma cada pieza para
que puedas modificarla con criterio.

## Rutas de especialización

| Ruta | Lecciones | Tiempo | Resultado |
| --- | --- | ---: | --- |
| calor | 6 | 4 h | difusión transitoria y energía |
| sólidos | 7 → 8 → 9 | 14 h | elasticidad, geometría y no linealidad |
| fluidos | 10 → 11 | 6 h | Stokes y Navier–Stokes separados |
| multifísica | 6 → 9 → 12 | 10 h | Cahn–Hilliard conservativo |

Completar todas las rutas, las herramientas transversales y un proyecto requiere
aproximadamente 44 horas. Para una primera experiencia basta el núcleo común y
una ruta.

Cada lección contiene objetivos, conexión con la página anterior, modelo,
forma débil, mapa de software, ejemplo, solver, verificación, errores frecuentes,
práctica y enlaces de continuidad.

## Práctica y seguimiento personal

No hay exámenes, calificaciones ni entregas. Los
[ejercicios](practice/exercises.md) indican en qué momento de la ruta aparecen y
ofrecen una comprobación automática o una cantidad esperada. Para integrar lo
aprendido puedes usar la [lista de proyecto](practice/project-checklist.md): no
asigna puntajes, solo ayuda a detectar formulaciones, resultados o pasos de
reproducción pendientes.

Consulta el [mapa del curso](learning-path.md) para rutas abreviadas y criterios
de avance.
