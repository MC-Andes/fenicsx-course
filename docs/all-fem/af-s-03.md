# Ficha de independencia AF-S-03

**Referencia:** placa de materiales múltiples de ALL-FEM,
[DOI](https://doi.org/10.1016/j.cma.2026.118985).

**PDE:** equilibrio elástico por subdominio, continuidad de desplazamiento y
tracción en interfaz perfectamente adherida.

**Parámetros:** placa 2×1 dividida en (x=1), (E_1=100), (E_2=400),
(\nu=0.3), tracción 1.

**Diferencias:** malla incorporada alineada, tags de celda calculados por
centroide y dos integrales `dx(marker)`.

**Forma débil:** suma de trabajos internos por material igual al trabajo externo.

**Verificación:** salto L2 de desplazamiento continuo y balance global.

**Declaración:** no se tradujo código `dolfin`; formulación/código son originales.
