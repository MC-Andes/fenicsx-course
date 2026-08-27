# Ficha de independencia AF-S-01

**Referencia:** caso inicial de placa rectangular elástica descrito en ALL-FEM,
[DOI 10.1016/j.cma.2026.118985](https://doi.org/10.1016/j.cma.2026.118985).

**PDE reconstruida:** equilibrio lineal (-\nabla\cdot\sigma=0), Hooke isotrópico,
empotramiento izquierdo y tracción derecha.

**Parámetros MC-Andes:** 1×0.2, (E=100), (\nu=0.3), tensión plana, tracción 1.

**Diferencias deliberadas:** geometría adimensional, solución P2, prefijo PETSc,
salida JSON y modo MPI/quick propios.

**Forma débil propia:** ((\sigma(u),\varepsilon(v))=(t,v)_{\Gamma_R}).

**Verificación independiente:** reacción opuesta a carga, energía positiva y
desplazamiento de punta; no se usa una figura de referencia.

**Declaración:** no se copió código, malla, figura ni texto del repositorio de
resultados ALL-FEM.
