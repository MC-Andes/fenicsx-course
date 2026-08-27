# Ficha de independencia AF-M-01

**Referencia:** benchmark Cahn–Hilliard mixto de ALL-FEM,
[DOI](https://doi.org/10.1016/j.cma.2026.118985).

**PDE:** conservación de concentración y definición de potencial químico en dos
ecuaciones de segundo orden.

**Parámetros/diferencias:** cuadrado unidad, (\lambda=10^{-2}), movilidad 1,
perturbación trigonométrica determinista. Se evita un RNG dependiente de la
partición.

**Forma débil:** P1×P1, Euler hacia atrás, residuo monolítico y derivada UFL.

**Verificación:** deriva de masa y energía libre no creciente en cada paso.

**Declaración:** se usó la PDE publicada y el demo oficial DOLFINx como fuentes;
no se copió código/figuras del repositorio ALL-FEM sin licencia.
