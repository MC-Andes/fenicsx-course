# Ficha de independencia AF-F-03

**Referencia:** flujo alrededor de cilindro de ALL-FEM,
[DOI](https://doi.org/10.1016/j.cma.2026.118985).

**PDE:** Navier–Stokes estacionario incompresible.

**Parámetros:** canal 2.2×0.41, cilindro (0.2,0.2), radio 0.05, (Re=3) para una
versión autoguiada estacionaria y de costo moderado.

**Diferencias:** geometría Gmsh propia, linealización Picard, modo quick y
tracción natural en salida. No pretende reproducir números de otro benchmark.

**Forma débil:** Oseen con velocidad previa como coeficiente, Taylor–Hood y BC
por grupos físicos.

**Verificación:** criterio relativo de Picard, caudal entrada/salida y arrastre
no nulo; el modo completo añade estudio de malla.

**Declaración:** no se copiaron malla, valores de referencia, código ni figuras.
