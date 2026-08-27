# Ficha de independencia AF-S-02

**Referencia:** problema de concentración de tensión alrededor de un agujero en
ALL-FEM, [DOI](https://doi.org/10.1016/j.cma.2026.118985).

**PDE:** elasticidad lineal en dominio perforado; agujero libre, izquierda fija,
tracción derecha.

**Parámetros:** placa 2×1, centro (1,0), radio 0.2, (E=100), (\nu=0.3).

**Diferencias:** geometría OCC y clasificación por bounding box creadas por
MC-Andes; (K_t) se mide en una vecindad del agujero y se acompaña de balance.

**Forma débil:** integral de Hooke en la placa; el agujero no aporta tracción.

**Verificación:** equilibrio global y estabilización de concentración bajo
refinamiento. El intervalo de smoke 1.5–8 detecta errores gruesos; no sustituye
la curva de independencia de malla.

**Declaración:** implementación DOLFINx/Gmsh original sin activos ALL-FEM.
