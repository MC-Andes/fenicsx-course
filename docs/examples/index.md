# Catálogo de ejemplos canónicos

Los scripts son la única fuente ejecutable. Cada uno acepta `--quick`,
`--output DIR` y `--write-fields` cuando genera campos. Las fichas completas
viven en `examples/metadata/`.

| Script | Nivel | Evidencia principal |
| --- | --- | --- |
| `examples/00_sanity_check.py` | Inicial | versiones y celdas globales |
| `examples/01_interpolation.py` | Inicial | tasas P1/P2 |
| `examples/02_tagged_boundaries.py` | Inicial | medidas de fronteras |
| `examples/03_function_spaces.py` | Inicial | grados de libertad globales |
| `examples/04_poisson_manufactured.py` | Inicial | tasas L2/H1 |
| `examples/05_heat_diffusion.py` | Intermedio | error analítico y energía |
| `examples/06_linear_elasticity.py` | Intermedio | reacción y energía |
| `examples/07_plate_with_hole.py` | Intermedio | concentración y malla |
| `examples/08_two_materials.py` | Intermedio | continuidad y balance |
| `examples/09_stokes_channel.py` | Intermedio | Poiseuille, caudal y divergencia |
| `examples/10_cylinder_flow.py` | Avanzado | Picard, arrastre y masa |
| `examples/11_hyperelasticity.py` | Avanzado | SNES, energía y Jacobiano |
| `examples/12_cahn_hilliard.py` | Avanzado | masa y energía libre |

## Esquema de salida

Todos los JSON incluyen `example`, `dolfinx_version`, `mpi_size`,
`solver_converged` y `validation_passed`. Las pruebas comparan escalares,
normas/tendencias y nunca archivos binarios bit a bit.
