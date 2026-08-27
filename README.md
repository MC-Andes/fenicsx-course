# Curso FEniCSx/DOLFINx de MC-Andes

Curso abierto, reproducible y verificable de elementos finitos con FEniCSx
0.11, DOLFINx 0.11.0.post0 y Python 3.12. El material está escrito en español y
conserva los términos técnicos en inglés cuando ayudan a consultar la API.

## Estado

La versión `0.1.0` contiene los doce módulos, ejemplos canónicos ejecutables,
ejercicios, pruebas numéricas, documentación y flujos de CI/publicación. Los
casos inspirados en ALL-FEM son implementaciones independientes construidas
desde sus ecuaciones; no contienen código del repositorio de resultados.

## Instalación nativa

```bash
micromamba create -f environment.yml
micromamba activate mcandes-fenicsx-course
python examples/00_sanity_check.py --output results
mpirun -n 2 python examples/00_sanity_check.py --output results
pytest
mkdocs build --strict
```

Los locks exactos para Linux x86_64 y macOS Apple Silicon, y la ruta alternativa
mediante contenedor, están explicados en
[`docs/setup.md`](docs/setup.md). Los ejemplos aceptan `--quick` para CI y
escriben un resumen JSON en el directorio indicado por `--output`.

## Estructura

- `examples/`: fuente única de las demostraciones completas.
- `docs/modules/`: recorrido pedagógico de módulos 0 a 11.
- `exercises/`: enunciados y soluciones separados.
- `src/mcandes_fenicsx/`: utilidades pequeñas de metadatos, mallas y
  verificación MPI-safe.
- `tests/`: pruebas unitarias, regresiones numéricas y ejecución paralela.

## Licencias

El código original se distribuye bajo MIT; véase [`LICENSE-CODE`](LICENSE-CODE).
El texto, las figuras y el material didáctico original se distribuyen bajo CC BY
4.0; véase [`LICENSE-CONTENT`](LICENSE-CONTENT). Cada activo de terceros conserva
su atribución específica.

## Cita

Use la metadata de [`CITATION.cff`](CITATION.cff). La release `v1.0.0` será la
primera versión estable y podrá enlazarse a un DOI de Zenodo cuando la
organización active esa integración.
