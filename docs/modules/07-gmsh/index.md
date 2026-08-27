# Módulo 7 · Gmsh, huecos y materiales múltiples

**Nivel:** intermedio · **Tiempo:** 5 h · **Prerrequisitos:** módulos 2 y 6.

## Objetivos

Construirás geometrías OCC con grupos físicos, convertirás sus etiquetas a
DOLFINx y resolverás placas perforadas/heterogéneas con estudio de malla.

## Modelos y unidades

1. Placa 2×1 con agujero circular de radio 0.2 y tracción nominal 1.
2. Placa 2×1 adherida con (E_1=100), (E_2=400), (\nu=0.3).

## Forma fuerte y condiciones

En cada material (\Omega_i), (-\nabla\cdot\sigma_i(u)=0). En una interfaz
perfecta, el desplazamiento y la tracción son continuos. El agujero es libre de
tracción; izquierda empotrada y derecha cargada.

## Forma débil

\[
\sum_i\int_{\Omega_i}\sigma_i(u):\varepsilon(v)\,dx_i
=\int_{\Gamma_R}t\cdot v\,ds.
\]

La continuidad de desplazamiento se hereda del espacio (H^1); la de tracción
surge del equilibrio débil.

## Mapa matemático → software

| Concepto | Objeto |
| --- | --- |
| diferencia booleana | `gmsh.model.occ.cut` |
| material/frontera | grupo físico 2D/1D |
| conversión colectiva | `gmshio.model_to_mesh(..., rank=0)` |
| materiales | `dx(marker)` con `cell_tags` |
| agujero libre | ausencia de término en `ds(hole)` |

## Ejemplos e inspección

Ejecuta `python examples/07_plate_with_hole.py --quick --output results` y
`python examples/08_two_materials.py --quick --output results`. Comprueba que
`facet_tags.find` no sea vacío y que cada celda tenga material.

## Solver

Ambos problemas son lineales y usan KSP con prefijo/error explícitos. Gmsh se
inicializa solo en rango 0; la conversión/partición involucra a todo el
comunicador.

## Verificación cuantitativa

La placa perforada exige balance <2e-7 y concentración localizada entre 1.5/8;
ese intervalo es smoke, no baseline final. La bimaterial exige balance <1e-8 y
salto de desplazamiento continuo <1e-10.

## Visualización

Muestra grupos físicos con etiquetas textuales. Para concentración, compara
regiones cercanas al agujero y curvas contra tamaño de malla; no uses el máximo
global junto al empotramiento como (K_t).

## Errores frecuentes

- Crear geometría en todos los rangos.
- Añadir grupo físico antes de `occ.synchronize()`.
- Perder el agujero al no incluir superficies/facetas en grupos.
- Etiquetar por coordenadas con tolerancia dependiente de la malla.

## Ejercicios graduados

1. Exporta/relee malla y etiquetas en XDMF.
2. Refina localmente el agujero y grafica (K_t(h)).
3. Cambia (E_2/E_1) y verifica continuidad/equilibrio de interfaz.

## Solución o guía

Clasifica curvas por bounding box y valida cardinalidades. Un valor estable de
(K_t) requiere refinamientos sucesivos, no una sola malla fina.

## Fuentes, licencia, versión y cambios

[Demo Gmsh 0.11](https://docs.fenicsproject.org/dolfinx/v0.11.0.post0/python/demos/demo_gmsh.html).
Fichas independientes [AF-S-02](../../all-fem/af-s-02.md) y
[AF-S-03](../../all-fem/af-s-03.md). Geometrías/código originales MIT.
