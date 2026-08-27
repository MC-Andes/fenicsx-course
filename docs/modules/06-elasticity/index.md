# Módulo 6 · Elasticidad lineal y posproceso

**Nivel:** intermedio · **Tiempo:** 4 h · **Prerrequisitos:** módulo 4, tensores y mecánica de sólidos.

## Objetivos

Resolverás un problema vectorial, diferenciarás tensión/deformación plana y
calcularás reacción, energía, desplazamiento y von Mises con significado físico.

## Modelo y unidades

Placa 1×0.2, (E=100), (\nu=0.3), empotrada a la izquierda y sometida a
tracción uniforme 1 a la derecha. Se usa un sistema de unidades consistente y
estado de tensión plana.

## Forma fuerte y condiciones

\[
-\nabla\cdot\sigma(u)=0,\quad u=0\text{ en }\Gamma_L,\quad
\sigma n=t\text{ en }\Gamma_R.
\]

Las caras superior/inferior tienen tracción natural cero.

## Derivación débil

\[
\int_\Omega\sigma(u):\varepsilon(v)\,dx
=\int_{\Gamma_R}t\cdot v\,ds,
\quad \varepsilon=\operatorname{sym}\nabla u.
\]

Para tensión plana se elimina la componente fuera del plano y se usa la
constante de Lamé efectiva, no la de deformación plana.

## Mapa matemático → software

| Concepto | Objeto |
| --- | --- |
| desplazamiento 2D | espacio P2 con `shape=(2,)` |
| deformación | `sym(grad(u))` |
| Hooke | función UFL `stress(u)` |
| tracción | `Constant` + `ds(marker)` |
| reacción | integral global de `dot(stress(u), n)` |

## Ejemplo e inspección

Ejecuta `python examples/06_linear_elasticity.py --quick --output results`. Revisa
etiquetas izquierda/derecha, vector de tracción, DOF restringidos y el signo de
la normal antes del solve.

## Solver

`LinearProblem` usa LU portable, prefijo único y error de KSP. Para mallas grandes
se sustituye por CG/GAMG con near-nullspace de modos rígidos.

## Verificación cuantitativa

La reacción horizontal debe ser opuesta a la carga total 0.2 con error relativo
<1e-8. La energía de deformación y el desplazamiento medio de la punta deben ser
positivos.

## Visualización

Exporta desplazamiento y, para von Mises, interpola la expresión en DG0. Una
escala deformada debe declarar su factor; no leas tensión nodal como continua.

## Errores frecuentes

- Mezclar parámetros de tensión/deformación plana.
- Integrar reacción solo en un rango o con normal equivocada.
- Restringir una componente cuando se pretendía empotramiento.
- Usar máximo nodal de tensión sin estudio de malla.

## Ejercicios graduados

1. Compara tensión y deformación plana.
2. Refina y estudia desplazamiento/reacción.
3. Calcula von Mises y verifica trabajo externo (=2U) en el caso lineal.

## Solución o guía

En carga proporcional lineal, (U=\frac12\int_{\Gamma_R}t\cdot u\,ds). La
reacción puede cambiar muy poco aunque el máximo de tensión todavía no converja.

## Fuentes, licencia, versión y cambios

El caso `AF-S-01` se reconstruyó independientemente desde la PDE. Véase su
[ficha](../../all-fem/af-s-01.md) y el demo oficial de elasticidad DOLFINx 0.11.
