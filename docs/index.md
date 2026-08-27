# FEniCSx verificable, desde la ecuación hasta el resultado

Este curso enseña a construir simulaciones con **FEniCSx 0.11**, **DOLFINx
0.11.0.post0** y Python 3.12. La ruta empieza con variables, mallas y espacios;
termina con elasticidad, flujo, no linealidad, Cahn–Hilliard, PETSc y MPI.

<div class="grid cards" markdown>

-   :material-function-variant: **Forma débil explícita**

    ---

    Cada término matemático se conecta con su objeto UFL/DOLFINx.

-   :material-check-decagram: **Verificación antes de visualizar**

    ---

    Error, tasa, balance o invariante obligatorios en cada caso principal.

-   :material-server-network: **MPI desde el principio**

    ---

    Las métricas son reducciones globales y los ejemplos no suponen arreglos globales.

-   :material-school: **Dos rutas de lectura**

    ---

    Recorrido autoguiado inicial y ruta rápida para usuarios de FEM/FEniCS legado.

</div>

## Empieza aquí

1. Revisa los [prerrequisitos y el programa](syllabus.md).
2. Instala y valida el [entorno reproducible](setup.md).
3. Ejecuta `python examples/00_sanity_check.py --output results`.
4. Avanza por los módulos y conserva los JSON de evidencia.

!!! important "Criterio de corrección"
    Que una simulación termine o produzca una figura no demuestra que sea
    correcta. Un ejemplo se considera aprobado solamente si
    `solver_converged` y `validation_passed` son verdaderos en su resumen JSON.

## Alcance de esta versión

La versión 0.1.1 publica una experiencia autocontenida de doce módulos y trece
demostraciones. No requiere docente, sesiones ni calificaciones. El
[repertorio verificable](examples/index.md) incluye únicamente problemas cuyo
código, datos, tolerancias y comprobaciones viven en este repositorio. Python
es la interfaz de aprendizaje y los cuadernos Jupyter quedan fuera del alcance
base.
