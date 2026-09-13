# Lección 11 · Navier–Stokes y flujo alrededor de un cilindro

**Nivel:** avanzado · **Tiempo:** 3 h · **Prerrequisitos:** lección 10, convección y número de Reynolds.

## Conexión con Stokes

La lección anterior construyó el espacio mixto, la restricción
incompresible, las condiciones de velocidad y el tratamiento de presión. Aquí
se conserva esa estructura y se añade el transporte de momento. Esta separación
permite atribuir los fallos al término nuevo, no a cinco conceptos simultáneos.

## Objetivos

Al terminar podrás:

- reconocer qué vuelve no lineal el problema;
- linealizar la convección mediante Picard/Oseen;
- definir un criterio de parada relativo;
- calcular caudal y arrastre como cantidades globales;
- distinguir un ejemplo docente de una simulación de alto Reynolds.

## Modelo y unidades

El canal mide 2.2×0.41, el obstáculo tiene radio 0.05, la velocidad pico de
entrada es 0.3, $\rho=1$ y $\mu=0.01$, por lo que el Reynolds del ejercicio es
bajo. Se prescribe entrada parabólica, no-slip en paredes y cilindro, y salida
natural.

## Forma fuerte

\[
\rho(u\cdot\nabla)u-\mu\Delta u+\nabla p=0,
\qquad \nabla\cdot u=0.
\]

## Linealización de Picard

Dada una velocidad $w=u^k$, se resuelve para $u^{k+1},p^{k+1}$:

\[
\mu(\nabla u^{k+1},\nabla v)
+\rho((w\cdot\nabla)u^{k+1},v)
-(p^{k+1},\nabla\cdot v)
+(\nabla\cdot u^{k+1},q)=0.
\]

Después se actualiza $w$ y se repite hasta que el cambio relativo de velocidad
sea menor que la tolerancia.

## Mapa matemático → software

| Concepto | Objeto |
| --- | --- |
| velocidad convectiva $w$ | `fem.Function` actualizada por iteración |
| término de Oseen | forma UFL no simétrica |
| iteración de Picard | ciclo Python con criterio relativo |
| fuerza sobre el cilindro | integral de tensión sobre `ds(cylinder)` |
| conservación | caudal global de entrada y salida |

## Ejemplo

```bash
python examples/11_cylinder_flow.py --quick --output results
```

Antes de resolver, inspecciona las etiquetas de entrada, salida, paredes y
cilindro. Después conserva número de iteraciones, cambio relativo, caudales y
arrastre; una línea de corriente visualmente suave no sustituye estas métricas.

## Solver

El modo docente usa una factorización directa en cada paso de Picard. El
operador es no simétrico por la convección. Una simulación grande requiere
precondicionamiento por bloques y, para regímenes más exigentes, formulación
transitoria o estabilizada que queda fuera del alcance de este ejemplo.

## Verificación cuantitativa

- Picard debe declarar convergencia.
- El arrastre debe ser finito y no nulo.
- El desbalance relativo de caudal debe ser menor de 4 % en modo `--quick`.
- El modo completo debe repetir el estudio con malla más fina y una tolerancia
  de masa más exigente.

## Errores frecuentes

- iniciar Navier–Stokes antes de validar el caso Stokes y las fronteras;
- intercambiar `grad` y `nabla_grad` sin revisar la convención;
- medir convergencia con una norma local de un solo rango;
- aceptar el máximo de iteraciones como convergencia;
- interpretar este Reynolds bajo como validación de turbulencia.

## Práctica

1. Ejecuta primero el canal de Stokes y registra su balance.
2. Cambia la velocidad de entrada y calcula el nuevo Reynolds.
3. Compara arrastre y número de iteraciones en dos mallas.
4. Explica qué prueba adicional necesitarías para un problema transitorio.

## Fuentes y versión

- [Demos oficiales de DOLFINx 0.11](https://docs.fenicsproject.org/dolfinx/v0.11.0.post0/python/demos.html).
- [Flujo alrededor de cilindro en el tutorial de Dokken](https://jsdokken.com/dolfinx-tutorial/chapter2/ns_code2.html), CC BY 4.0.

La implementación y sus comprobaciones son originales del curso y están en
`examples/11_cylinder_flow.py`.

---

**Anterior:** [Stokes y Poiseuille](../08-stokes/index.md) ·
**Siguiente:** [Cahn–Hilliard](../10-multiphysics/index.md)
