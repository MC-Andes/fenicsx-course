# Ruta de mecánica de sólidos

Esta ruta transforma el problema escalar del núcleo común en modelos
vectoriales de deformación y tensión.

## Orden recomendado

| Lección | Concepto nuevo | Ejemplo | Evidencia |
| --- | --- | --- | --- |
| [7 · Elasticidad lineal](../modules/06-elasticity/index.md) | espacio vectorial, deformación y tracción | placa rectangular | equilibrio y energía |
| [8 · Gmsh y materiales](../modules/07-gmsh/index.md) | geometría CAD, etiquetas e interfaz | placa con agujero/dos materiales | malla y balance |
| [9 · Hiperelasticidad](../modules/09-nonlinear/index.md) | energía, Jacobiano y SNES | bloque neo-Hookeano | convergencia y $J>0$ |

## El puente desde Poisson

El pipeline no cambia. En elasticidad, la incógnita pasa de escalar a vector,
`grad(u)` pasa a ser tensor y la ley constitutiva conecta deformación y tensión.
La integral de rigidez sigue representando trabajo interno; el lado derecho
representa trabajo externo.

## Dónde detenerse

- Si solo necesitas deformaciones pequeñas y geometría simple, termina en 7.
- Si hay huecos, regiones o varios materiales, continúa con 8.
- Si hay grandes deformaciones o la respuesta depende del estado actual,
  continúa con 9.

Antes de usar máximos de tensión, realiza un estudio de malla. En esquinas,
huecos o cargas puntuales puede existir una singularidad y el máximo no tiene
por qué converger.

---

**Entrada:** [elementos, espacios y convergencia](../modules/03-spaces/index.md) ·
**Comienza:** [elasticidad lineal](../modules/06-elasticity/index.md)
