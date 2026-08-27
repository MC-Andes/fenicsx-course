# ALL-FEM: política y catálogo de adaptaciones

ALL-FEM aporta enunciados de referencia, no plantillas de código. El repositorio
de resultados inspeccionado el 2026-08-26 no declaraba licencia y sus soluciones
usaban FEniCS legado (`dolfin`). Por tanto, este curso:

1. reconstruye PDE/condiciones desde el artículo y apéndice;
2. define parámetros y geometrías propias;
3. deriva formas débiles independientemente;
4. implementa DOLFINx 0.11 desde cero;
5. valida con balances, soluciones o invariantes propios;
6. no copia texto extenso, código, figuras ni mallas del repositorio.

| ID | Tema | Script canónico | Evidencia |
| --- | --- | --- | --- |
| AF-S-01 | placa lineal | `examples/06_linear_elasticity.py` | reacción/energía |
| AF-S-02 | placa perforada | `examples/07_plate_with_hole.py` | concentración/malla |
| AF-S-03 | dos materiales | `examples/08_two_materials.py` | continuidad/balance |
| AF-F-01 | Stokes en canal | `examples/09_stokes_channel.py` | Poiseuille/caudal |
| AF-F-03 | cilindro | `examples/10_cylinder_flow.py` | Picard/arrastre/masa |
| AF-S-05 | neo-Hookeano | `examples/11_hyperelasticity.py` | SNES/J/energía |
| AF-M-01 | Cahn–Hilliard | `examples/12_cahn_hilliard.py` | masa/energía libre |

La numeración editorial exacta debe cotejarse con el apéndice final antes de
`v1.0.0`. Los ID del curso permanecen estables.
