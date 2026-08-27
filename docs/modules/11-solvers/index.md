# Módulo 11 · Solvers, paralelismo, rendimiento e I/O

**Nivel:** cierre · **Tiempo:** 4 h · **Prerrequisitos:** módulos 4–10.

## Objetivos

Escogerás KSP/PC/SNES iniciales, descubrirás prefijos, interpretarás vectores
distribuidos, compararás serial/MPI y producirás salidas/reporte reproducibles.

## Modelo y unidades

El laboratorio reproduce Poisson y Stokes con uno/dos rangos. Las unidades son
las de cada problema; la comparación usa métricas físicas, no orden de DOF.

## Forma fuerte y débil

No se introduce una PDE nueva. Se conserva exactamente la formulación de los
módulos anteriores y se cambia únicamente representación algebraica,
precondicionador, partición y salida.

## Mapa concepto → software

| Concepto | Objeto |
| --- | --- |
| lineal SPD | KSP CG + PC GAMG |
| saddle point simétrico | MINRES + fieldsplit |
| no simétrico | GMRES + precondicionador adecuado |
| no lineal | SNES + Jacobiano/line search |
| datos locales/fantasma | `Function.x`, `index_map` |
| salida paralela | XDMF/VTX |

## Laboratorio e inspección

```bash
python examples/04_poisson_manufactured.py --quick --output results/serial
mpirun -n 2 python examples/04_poisson_manufactured.py --quick --output results/mpi2
python examples/09_stokes_channel.py --quick --output results/serial
mpirun -n 2 python examples/09_stokes_channel.py --quick --output results/mpi2
```

Compara error, tasa, caudal y divergencia dentro de tolerancia; no compares el
contenido de `x.array` ni XDMF bit a bit.

## Solver

`petsc_options_prefix` es obligatorio en DOLFINx 0.11. Descubre el prefijo real
con `problem.solver.getOptionsPrefix()` y añade opciones de línea de comandos
sin contaminar otros problemas. Toda razón <=0 es fallo.

## Verificación cuantitativa

Las diferencias serial/MPI deben quedar por debajo de las tolerancias de cada
ficha. Registra celdas globales, rangos, tiempo y razón/iteraciones; una aceleración
con física distinta no cuenta.

## I/O y visualización

XDMF sirve para mallas/campos compatibles y VTX para series de alta orden.
PyVista es exploración; ParaView, posproceso externo. Artefactos grandes no se
versionan y los workflows conservan JSON/logs temporalmente.

## Errores frecuentes

- Usar suma local como energía global.
- Cronometrar compilación JIT como si fuera solo solve sin declararlo.
- No sincronizar campos antes de I/O.
- Ejecutar varios casos con el mismo prefijo PETSc.
- Optimizar antes de establecer un baseline verificable.

## Ejercicios graduados

1. Descubre prefijos y activa monitor solo para un bloque.
2. Compara 1/2 rangos con tabla de tiempo y métricas.
3. Cambia LU por iterativo y justifica tolerancia/precondicionador.

## Solución o guía

Una tabla mínima contiene plataforma, versión, MPI, celdas, DOF, tiempo JIT,
tiempo solve, iteraciones y métrica física. Repite para amortiguar ruido.

## Fuentes, licencia y versión

[API FEM/PETSc 0.11](https://docs.fenicsproject.org/dolfinx/v0.11.0.post0/python/generated/dolfinx.fem.petsc.html)
y demos de comunicación/I/O. Código MIT, contenido CC BY 4.0.
