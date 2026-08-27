# Ficha de independencia AF-F-01

**Referencia:** canal Stokes inicial de ALL-FEM,
[DOI](https://doi.org/10.1016/j.cma.2026.118985).

**PDE:** (-\Delta u+\nabla p=0), (\nabla\cdot u=0).

**Parámetros/diferencias:** cuadrado unidad con solución manufacturada exacta
(u=(4y(1-y),0)), (p=4-8x); velocidad exacta en la frontera. Esto permite una
prueba más fuerte que comparar una imagen de canal.

**Forma débil:** bloque Taylor–Hood con signos físicos de presión y nullspace
constante explícito.

**Verificación:** errores L2, divergencia y caudal analítico 2/3.

**Declaración:** código original basado en API oficial DOLFINx 0.11, no en el
repositorio ALL-FEM.
