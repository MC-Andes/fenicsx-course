# Ruta de mecánica de fluidos

La ruta separa deliberadamente Stokes de Navier–Stokes. Primero se aprende el
sistema mixto velocidad–presión; después se añade la no linealidad convectiva.

## Orden recomendado

| Lección | Concepto nuevo | Ejemplo | Evidencia |
| --- | --- | --- | --- |
| [10 · Stokes](../modules/08-stokes/index.md) | Taylor–Hood, presión y nullspace | canal de Poiseuille | caudal, error y divergencia |
| [11 · Navier–Stokes](../modules/navier-stokes/index.md) | convección e iteración de Picard | flujo alrededor de cilindro | masa, arrastre y convergencia |

## El puente desde Poisson

Stokes conserva una forma lineal, pero combina dos campos y produce un sistema
de punto silla. La presión actúa como multiplicador de la restricción
incompresible. Navier–Stokes reutiliza ese espacio y añade
$(u\cdot\nabla)u$, que depende de la solución.

## Dónde detenerse

- Para flujo viscoso con inercia despreciable, termina en Stokes.
- Para flujo con convección relevante, continúa con Navier–Stokes.
- Para Reynolds mayores, transitorios o turbulencia, usa la lección 11 como
  base conceptual, no como modelo de producción.

---

**Entrada:** [elementos y espacios mixtos](../modules/03-spaces/index.md) ·
**Comienza:** [Stokes y Poiseuille](../modules/08-stokes/index.md)
