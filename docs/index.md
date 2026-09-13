# FEniCSx verificable: aprende resolviendo

<span class="course-kicker">Curso abierto de MC-Andes</span>

Construye tu primera PDE y entiende cada decisión que la hace correcta. El
curso usa **FEniCSx 0.11**, **DOLFINx 0.11.0.post0** y Python 3.12; comienza con
la forma débil y un problema de Poisson completo, y después abre rutas de calor,
sólidos, fluidos y multifísica.

[Ver el mapa del curso](learning-path.md){ .md-button .md-button--primary }
[Instalar el entorno](setup.md){ .md-button }

<div class="grid cards" markdown>

<!-- markdownlint-disable MD030 -->

-   **Un ciclo que se repite**

    ---

    Malla → espacio → forma débil → condiciones → solve → verificación.

-   **Rutas por física**

    ---

    Tras el núcleo común, elige calor, sólidos, fluidos o multifísica.

-   **Verificación antes de visualizar**

    ---

    Cada caso conserva error, tasa, balance o invariante en un JSON.

-   **Scripts, no cuadernos**

    ---

    Todo se ejecuta desde archivos `.py`, en serial y con MPI cuando aplica.

<!-- markdownlint-enable MD030 -->

</div>

## Tus primeros 90 minutos

| Paso | Acción | Resultado |
| --- | --- | --- |
| 1 | revisa la [comprobación previa](practice/prior-knowledge.md) | sabes qué repasar |
| 2 | instala el [entorno reproducible](setup.md) | DOLFINx y MPI disponibles |
| 3 | ejecuta la [orientación](modules/00-orientation/index.md) | sanity check válido |
| 4 | estudia la [forma débil](foundations/weak-forms.md) | reconoces ensayo, prueba y BC |
| 5 | resuelve [Poisson](modules/04-poisson/index.md) | primer solve con error medido |

Después de Poisson, las lecciones de objetos, mallas y espacios explican con
detalle las piezas que ya viste en funcionamiento. Así no necesitas memorizar
una API descontextualizada antes de resolver algo.

## Elige una ruta

<div class="grid cards" markdown>

<!-- markdownlint-disable MD030 -->

-   **Transferencia de calor**

    ---

    De Poisson estacionario a difusión transitoria, estado previo y energía.

    [Ir a difusión](modules/05-diffusion/index.md)

-   **Mecánica de sólidos**

    ---

    Elasticidad, Gmsh, materiales múltiples y grandes deformaciones.

    [Ver ruta de sólidos](tracks/solids.md)

-   **Mecánica de fluidos**

    ---

    Stokes primero; convección y Navier–Stokes después.

    [Ver ruta de fluidos](tracks/fluids.md)

-   **Multifísica**

    ---

    Cahn–Hilliard combina tiempo, espacio mixto y solución no lineal.

    [Ir a multifísica](modules/10-multiphysics/index.md)

<!-- markdownlint-enable MD030 -->

</div>

!!! important "Criterio de corrección"
    Que una simulación termine o produzca una figura no demuestra que sea
    correcta. Un ejemplo se considera aprobado solamente si
    `solver_converged` y `validation_passed` son verdaderos en su resumen JSON.

## Qué contiene esta versión

El curso publica una experiencia autocontenida de trece lecciones y trece
demostraciones. La ruta actual añade una lección matemática, separa
Stokes/Navier–Stokes y ofrece rutas explícitas sin cambiar los resultados
numéricos. No requiere docente, sesiones ni calificaciones. El
[repertorio verificable](examples/index.md) incluye únicamente problemas cuyo
código, datos, tolerancias y comprobaciones viven en este repositorio. Python
es la interfaz de aprendizaje y los cuadernos Jupyter quedan fuera del alcance
base.

## Personas y créditos

El curso está vinculado al grupo del investigador principal y mantiene una
página explícita de [equipo y contribuciones](team.md). Los datos personales se
publican únicamente con confirmación de cada integrante.
