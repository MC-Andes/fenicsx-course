# Lección 10 · Stokes y el primer problema mixto

**Nivel:** intermedio · **Tiempo:** 3 h · **Prerrequisitos:** lecciones 2–5 y mecánica de fluidos básica.

## Por qué Stokes va antes de Navier–Stokes

Stokes introduce dos dificultades nuevas —velocidad/presión y restricción de
incompresibilidad— sin añadir todavía convección no lineal. Cuando el canal
analítico esté validado, la lección 11 conservará este sistema y añadirá un solo
concepto: transporte de momento.

## Objetivos

Al terminar podrás:

- construir un espacio Taylor–Hood velocidad–presión;
- explicar por qué la presión puede estar definida hasta una constante;
- imponer no-slip y un perfil de entrada;
- medir caudal, divergencia y error global;
- interpretar un sistema de punto silla.

## Modelo y unidades

En un canal rectangular adimensional se usa
$u=(4y(1-y),0)$, $p=4-8x$ y viscosidad $\mu=1$. El perfil de Poiseuille y la
presión lineal ofrecen una referencia analítica.

## Forma fuerte

\[
-\mu\Delta u+\nabla p=0,
\qquad \nabla\cdot u=0.
\]

La velocidad se prescribe en entrada y paredes. La salida y el tratamiento de
presión se documentan en el script; no se debe imponer simultáneamente una
presión puntual y un nullspace sin justificación.

## Forma débil

Encontrar $(u,p)\in V\times Q$ tal que, para todo $(v,q)$,

\[
\mu(\nabla u,\nabla v)
-(p,\nabla\cdot v)
+(\nabla\cdot u,q)=0.
\]

La elección P2/P1 evita el par igual orden no estabilizado y satisface la
compatibilidad inf-sup a nivel de este curso.

## Mapa matemático → software

| Concepto | Objeto |
| --- | --- |
| velocidad | elemento P2 vectorial |
| presión | elemento P1 escalar |
| espacio mixto | `mixed_element([P2, P1])` |
| sistema de punto silla | matriz y vectores por bloques |
| presión hasta constante | `PETSc.NullSpace` |
| caudal | integral global de $u\cdot n$ |

## Ejemplo

```bash
python examples/10_stokes_channel.py --quick --output results
```

Antes del solve, comprueba fronteras, grados de libertad restringidos y espacio
de presión. Después revisa el error de velocidad/presión, la divergencia y el
caudal; no empieces por la visualización.

## Solver

El ejemplo usa MINRES con `fieldsplit`, GAMG para velocidad, Jacobi para presión
y nullspace constante. El prefijo PETSc debe ser único y toda razón de
convergencia menor o igual a cero es un fallo.

## Verificación cuantitativa

- el caudal analítico es $2/3$;
- los errores de velocidad y presión deben quedar bajo las tolerancias de la
  metadata;
- la norma de divergencia debe ser pequeña;
- las métricas deben coincidir entre uno y dos rangos dentro de tolerancia.

## Errores frecuentes

- usar P1/P1 sin estabilización;
- comparar presión sin eliminar su constante;
- olvidar la condición de compatibilidad del sistema;
- integrar caudal con el signo de normal equivocado;
- usar un valor local como si fuera la integral global.

## Práctica

1. Cambia longitud y altura, y deriva el nuevo caudal.
2. Sustituye el nullspace por una presión de referencia y compara.
3. Ejecuta con uno y dos procesos y explica las diferencias de redondeo.
4. Identifica qué término faltaría para obtener Navier–Stokes.

## Fuentes y versión

- [Demo oficial de Stokes en DOLFINx 0.11](https://docs.fenicsproject.org/dolfinx/v0.11.0.post0/python/demos/demo_stokes.html).
- [Demos oficiales de DOLFINx](https://docs.fenicsproject.org/dolfinx/v0.11.0.post0/python/demos.html).

El caso incluye formulación, código y comprobaciones en
`examples/10_stokes_channel.py`.

---

**Anterior:** [ruta de fluidos](../../tracks/fluids.md) ·
**Siguiente:** [Navier–Stokes y cilindro](../navier-stokes/index.md)
