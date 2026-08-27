# Módulo 9 · Formulaciones no lineales

**Nivel:** avanzado · **Tiempo:** 5 h · **Prerrequisitos:** módulo 6, cálculo tensorial.

## Objetivos

Definirás energía, residuo/Jacobiano automático, SNES y carga incremental;
diagnosticarás divergencia e inversión de elementos.

## Modelo y unidades

Bloque 1×0.2 neo-Hookeano, (E=100), (\nu=0.3), empotrado a la izquierda y
carga final 5 a la derecha, aplicada en 3/6 incrementos.

## Forma fuerte y condiciones

En configuración de referencia, (\operatorname{Div}P=0), con desplazamiento
cero a la izquierda y (PN=T) a la derecha. (F=I+\nabla u), (J=\det F>0).

## Energía y forma débil

\[
\psi=\frac\mu2(I_C-2)-\mu\ln J+\frac\lambda2(\ln J)^2,
\quad R(u;v)=D_u\left[\int\psi\,dX-\int T\cdot u\,dS\right][v]=0.
\]

El Jacobiano tangente es (D_uR(u;\delta u,v)) y UFL lo deriva.

## Mapa matemático → software

| Concepto | Objeto |
| --- | --- |
| estado no lineal | `fem.Function` |
| (F) diferenciable | `ufl.variable(I + grad(u))` |
| residuo | `ufl.derivative(Pi, u, v)` |
| Newton | `fem.petsc.NonlinearProblem` / SNES |
| carga incremental | `Constant.value` |

## Ejemplo e inspección

Ejecuta `python examples/11_hyperelasticity.py --quick --output results`. Revisa
iteraciones por incremento, (J_{min}), energía, reacción y desplazamiento.

## Solver

SNES Newton con backtracking, tolerancias explícitas, máximo 40 iteraciones y
error ante divergencia. Cada incremento parte del estado convergido anterior.

## Verificación cuantitativa

Se exige razón SNES positiva, (J_{min}>0.5), energía positiva, balance <2e-6 y
desplazamiento de punta positivo. Ninguna figura sustituye (J_{min}).

## Visualización

Exporta desplazamiento/J en campos separados y no extrapoles DG0 como si fuera
continuo. Marca cualquier celda con (J\le0) como fallo, no como dato extremo.

## Errores frecuentes

- Resolver carga completa desde estado cero.
- Usar `ln(J)` con (J\le0) y ocultar NaN.
- Derivar respecto de una expresión que no fue declarada `variable`.
- Medir solo residuo absoluto en variables mal escaladas.

## Ejercicios graduados

1. Compara 1, 3 y 6 incrementos.
2. Aumenta (\nu\to0.499) y observa bloqueo.
3. Formula desplazamiento–presión mixto casi incompresible.

## Solución o guía

Si Newton falla, reduce incremento, conserva el último estado convergido y
activa monitor SNES. Para incompresibilidad usa formulación mixta; no “arregles”
el bloqueo relajando una tolerancia.

## Fuentes, licencia, versión y cambios

[API `NonlinearProblem` 0.11](https://docs.fenicsproject.org/dolfinx/v0.11.0.post0/python/generated/dolfinx.fem.petsc.html).
La implementación hiperelástica y sus verificaciones son originales del curso
y están disponibles bajo MIT.
