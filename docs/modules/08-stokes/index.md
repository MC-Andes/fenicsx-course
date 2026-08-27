# Módulo 8 · Stokes y Navier–Stokes

**Nivel:** intermedio/avanzado · **Tiempo:** 6 h · **Prerrequisitos:** módulos 3–4 y mecánica de fluidos.

## Objetivos

Construirás Taylor–Hood, controlarás el nullspace de presión, validarás
Poiseuille y resolverás un Oseen iterativo con arrastre/balance de masa.

## Modelos y unidades

Stokes manufacturado en canal unidad: (u=(4y(1-y),0)), (p=4-8x), viscosidad
1. Cilindro: canal 2.2×0.41, radio 0.05, velocidad pico 0.3, (\rho=1),
(\mu=0.01), (Re=3).

## Forma fuerte y condiciones

\[
-\mu\Delta u+\rho(u\cdot\nabla)u+\nabla p=0,\qquad\nabla\cdot u=0.
\]

Poiseuille prescribe velocidad exacta; el cilindro usa entrada parabólica,
no-slip en paredes/obstáculo y tracción natural en salida.

## Forma débil

\[
\mu(\nabla u,\nabla v)+\rho((w\cdot\nabla)u,v)
-(p,\nabla\cdot v)+(\nabla\cdot u,q)=0.
\]

Para Stokes, (w=0). Para Picard, (w=u^k) y se itera hasta convergencia.

## Mapa matemático → software

| Concepto | Objeto |
| --- | --- |
| velocidad/presión | P2 vectorial / P1 escalar |
| saddle point | matriz bloque/nest |
| presión hasta constante | `PETSc.NullSpace` |
| Picard | `Function` coeficiente actualizado |
| caudal/arrastre | integrales `ds` globales |

## Ejemplos e inspección

Ejecuta `python examples/09_stokes_channel.py --quick --output results` y después
`python examples/10_cylinder_flow.py --quick --output results`. Inspecciona
fronteras, mapas mixtos, media de presión e iteración relativa.

## Solver

Stokes usa MINRES + fieldsplit GAMG/Jacobi y nullspace constante. El cilindro
usa LU por iteración de Picard para el modo de práctica; una simulación grande debe
usar precondicionamiento por bloques.

## Verificación cuantitativa

Poiseuille comprueba errores de velocidad/presión, divergencia y caudal 2/3. El
cilindro exige Picard convergente, arrastre no nulo y desbalance de caudal <4 %
en modo quick; el estudio completo reduce esa tolerancia y refina el obstáculo.

## Visualización

Exporta velocidad interpolada a P1 y presión por separado. Usa flechas y líneas
de corriente con escala declarada; reporta arrastre/caída de presión junto a la
figura.

## Errores frecuentes

- Par P1/P1 no estabilizado.
- Omitir nullspace con velocidad prescrita en todo el contorno.
- Comparar presión sin eliminar su constante.
- Integrar caudal con signo de normal inconsistente.
- Aceptar una iteración no lineal sin criterio relativo.

## Ejercicios graduados

1. Cambia longitud/altura y deriva caudal analítico.
2. Impone presión de referencia en vez de nullspace y compara.
3. Estudia arrastre del cilindro con tres mallas y dos (Re).

## Solución o guía

Una presión puntual y un nullspace son alternativas, no deben aplicarse a la
vez sin justificar. El balance usa flujo entrante con signo opuesto a la normal.

## Fuentes, licencia, versión y cambios

[Demo Stokes 0.11](https://docs.fenicsproject.org/dolfinx/v0.11.0.post0/python/demos/demo_stokes.html).
Los casos del canal y el cilindro incluyen aquí su formulación, código y
comprobaciones de caudal, divergencia, masa y arrastre.
