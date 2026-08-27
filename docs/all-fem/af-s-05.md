# Ficha de independencia AF-S-05

**Referencia:** sólido neo-Hookeano/incompresible de la familia avanzada de
ALL-FEM, [DOI](https://doi.org/10.1016/j.cma.2026.118985).

**PDE:** equilibrio material (\operatorname{Div}P=0) derivado de energía.

**Parámetros/diferencias:** bloque compresible (\nu=0.3), carga incremental
y nivel moderado; la formulación mixta casi incompresible queda como reto.

**Forma débil:** primera variación de potencial neo-Hookeano propia, Jacobiano
automático UFL.

**Verificación:** convergencia SNES por incremento, (J_{min}>0), energía y
equilibrio de reacción.

**Declaración:** implementación original; no migra un script de FEniCS legado.
