# Módulo 10 · Acoplamiento y multifísica

**Nivel:** avanzado · **Tiempo:** 5 h · **Prerrequisitos:** módulos 5 y 9.

## Objetivos

Compararás acoplamiento monolítico/particionado, formularás Cahn–Hilliard mixto
y verificarás conservación de masa/disipación de energía.

## Modelo y unidades

Separación de fases adimensional en cuadrado unidad: movilidad 1,
(\lambda=10^{-2}), (dt=5\times10^{-6}), perturbación analítica determinista
alrededor de concentración 0.63.

## Forma fuerte y condiciones

\[
\partial_tc-\nabla\cdot(M\nabla\mu)=0,\quad
\mu-f'(c)+\lambda\nabla^2c=0,
\]

con flujo normal cero de (c) y (\mu). La masa total debe conservarse.

## Forma débil temporal

\[
(c^{n+1}-c^n,q)+dt(M\nabla\mu^{n+1},\nabla q)=0,
\]
\[
(\mu^{n+1},v)-(f'(c^{n+1}),v)-\lambda(\nabla c^{n+1},\nabla v)=0.
\]

Se resuelve monolíticamente en P1×P1.

## Mapa matemático → software

| Concepto | Objeto |
| --- | --- |
| (c,\mu) | `mixed_element([P1, P1])` |
| potencial (f'(c)) | `variable` + `diff` |
| estado previo | segunda `Function` mixta |
| sistema acoplado | `NonlinearProblem` |
| masa/energía | integrales globales por paso |

## Ejemplo e inspección

Ejecuta `python examples/12_cahn_hilliard.py --quick --output results`. Inspecciona
las listas de masa/energía e iteraciones, no solo el campo final.

## Solver

SNES monolítico con line search y LU en el modo de práctica. La condición inicial usa
función trigonométrica, no RNG dependiente de partición; la ficha conserva
`seed: 42` para futuras variantes aleatorias reproducibles.

## Verificación cuantitativa

La deriva máxima de masa debe ser <1e-9 y el mayor incremento de energía libre
<1e-8. La energía es (\int[f(c)+\lambda|\nabla c|^2/2]dx).

## Visualización

La concentración debe acompañarse de curva masa/energía. Usa paleta divergente
centrada y límites fijos entre tiempos para no inventar contraste.

## Errores frecuentes

- Inicialización aleatoria distinta por partición.
- Actualizar el estado previo antes de medir invariantes.
- Confundir conservación de masa con acotamiento puntual (0\le c\le1).
- Aceptar una energía creciente por “apariencia física”.

## Ejercicios graduados

1. Cambia amplitud de perturbación y conserva masa.
2. Compara Euler/Crank–Nicolson y monotonicidad.
3. Diseña un termofluido particionado y enumera balances de cada subproblema.

## Solución o guía

Evalúa invariantes antes de copiar `current` a `previous`. En un acoplamiento
particionado define criterio de interfaz además de criterios internos.

## Fuentes, licencia, versión y cambios

[Demo Cahn–Hilliard 0.11](https://docs.fenicsproject.org/dolfinx/v0.11.0.post0/python/demos/demo_cahn-hilliard.html)
y ficha [AF-M-01](../../all-fem/af-m-01.md). Se cambió la perturbación aleatoria
por una analítica MPI-determinista y se añadieron invariantes obligatorios.
