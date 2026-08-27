# Solución de problemas

## `ModuleNotFoundError: dolfinx`

Confirma `micromamba activate mcandes-fenicsx-course` y ejecuta `python -c
"import dolfinx; print(dolfinx.__version__)"`. No intentes instalar DOLFINx con
`pip` aislado: PETSc, MPI y las bibliotecas nativas deben ser compatibles.

## MPI usa una implementación distinta

Compara `which mpirun` y `python -c "from mpi4py import MPI; print(MPI.get_vendor())"`.
No mezcles Open MPI del sistema con `mpich` del entorno. Recrea el entorno si
ambos provienen de prefijos diferentes.

## PETSc devuelve razón negativa

El ejemplo falla deliberadamente. Revisa primero frontera, nullspace de presión,
escala de coeficientes y opciones prefijadas. Luego aumenta monitorización con
`-<prefijo>ksp_monitor` o `-<prefijo>snes_monitor`; no conviertas el fallo en
advertencia.

## Gmsh no carga en macOS

Verifica que `gmsh` y DOLFINx provengan del mismo entorno. Si falla una biblioteca
gráfica, usa el contenedor o instala la dependencia de sistema indicada por
conda-forge. La generación se ejecuta en el rango 0 y la conversión es colectiva.

## PyVista no abre ventana

La visualización es opcional. Ejecuta `--write-fields` y abre XDMF en ParaView;
en servidores usa renderizado off-screen. La validación JSON no depende de una
ventana gráfica.

## Diferencias serial/paralelo

Pequeñas diferencias de redondeo son normales. Diferencias grandes suelen
indicar una suma local usada como global, valores fantasma desactualizados o
una selección de entidades no colectiva. Compara normas, balances y tasas, no
vectores bit a bit.

## Reporte reproducible

Incluye comando exacto, JSON, versiones, sistema operativo, número de rangos y
el primer traceback completo. El formulario de issue pide esos datos.
