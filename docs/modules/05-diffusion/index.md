# Lección 6 · Difusión transitoria

**Nivel:** intermedio · **Tiempo:** 4 h · **Prerrequisitos:** lecciones 2–5, derivadas temporales.

## Qué cambia frente a Poisson

La rigidez espacial es conocida. La novedad es conservar un estado anterior,
discretizar $\partial_tu$ y verificar la evolución, no solamente el campo final.
Este patrón reaparece en Navier–Stokes transitorio y multifísica.

## Objetivos

Discretizarás el tiempo con Euler implícito, actualizarás `Function`/`Constant`,
reutilizarás la estructura del problema y comprobarás solución y energía.

## Modelo y unidades

Temperatura adimensional en el cuadrado unidad, difusividad 1, tiempo final
0.05. La condición inicial es (u_0=\sin(\pi x)\sin(\pi y)).

## Forma fuerte y condiciones

\[
\partial_tu-\nabla^2u=0,\quad u|_{\partial\Omega}=0,\quad u(x,0)=u_0(x).
\]

La solución exacta es (u=e^{-2\pi^2t}u_0).

## Derivación débil temporal

Con Euler hacia atrás:

\[
\int_\Omega u^{n+1}v\,dx+\Delta t\int_\Omega\nabla u^{n+1}\cdot\nabla v\,dx
=\int_\Omega u^nv\,dx.
\]

## Mapa matemático → software

| Matemática | Objeto |
| --- | --- |
| estado (u^n) | `fem.Function` |
| paso (\Delta t) | `fem.Constant` |
| matriz masa+rigidez | forma bilineal |
| actualización | copia de coeficientes + `scatter_forward` |

## Ejemplo e inspección

Ejecuta `python examples/05_heat_diffusion.py --quick --output results`.
Inspecciona `time_steps`, `final_time`, error y energías. El script canónico es
`examples/05_heat_diffusion.py`.

## Solver

Cada paso exige razón KSP positiva. La forma mantiene el mismo `dt`; un flujo de
producción podría ensamblar la matriz una vez y solo actualizar el lado derecho.

## Verificación cuantitativa

Se exige error L2 final <0.03 y (E_{n+1}<E_n), con
(E=\frac12\int u^2dx). El umbral incluye error espacial y temporal del modo
quick; un estudio serio varía ambos por separado.

## Visualización

XDMF recibe tiempo explícito. Para una serie completa usa VTX/XDMF y comprueba
que nombres/tiempos sean monótonos; la animación no reemplaza el balance.

## Errores frecuentes

- Sobrescribir `u_n` antes de medir el paso.
- Actualizar solo DOF propios y olvidar fantasmas.
- Cambiar `dt` sin actualizar `Constant` o matriz.
- Atribuir todo error a la malla sin refinar tiempo.

## Ejercicios graduados

1. Duplica pasos con malla fija y estima orden temporal.
2. Cambia difusividad y corrige solución exacta.
3. Implementa Crank–Nicolson y compara energía/error.

## Solución o guía

Euler implícito es de orden 1 temporal; Crank–Nicolson, de orden 2 para solución
suave. Construye tablas separadas de (h) y (\Delta t).

## Fuentes, licencia y versión

DOLFINx 0.11.0.post0; explicación original con referencia al tutorial FEniCSx
de Dokken (CC BY 4.0). Código del curso MIT, contenido CC BY 4.0.

---

**Anterior:** [núcleo común](../03-spaces/index.md) ·
**Siguiente:** [ruta de sólidos](../../tracks/solids.md) o
[multifísica](../10-multiphysics/index.md)
