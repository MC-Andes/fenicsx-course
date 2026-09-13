# Curso FEniCSx/DOLFINx de MC-Andes

Curso abierto, reproducible y verificable de elementos finitos con FEniCSx
0.11, DOLFINx 0.11.0.post0 y Python 3.12. El material está escrito en español y
conserva los términos técnicos en inglés cuando ayudan a consultar la API.

## Estado

La rama actual contiene trece ejemplos canónicos, ejercicios, pruebas
numéricas, documentación y flujos de CI/publicación. La ruta renovada comienza
con matemática mínima y un solve completo de Poisson; después explica objetos,
mallas y espacios, y abre recorridos de calor, sólidos, fluidos y multifísica.
El repertorio solo presenta problemas con código incluido, criterio cuantitativo
de éxito y ejecución comprobable.

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
- `docs/learning-path.md`: mapa, dependencias y rutas abreviadas.
- `docs/foundations/`: matemática mínima antes del primer solve.
- `docs/modules/`: lecciones del núcleo y de cada fenómeno.
- `docs/tracks/`: puentes conceptuales para sólidos y fluidos.
- `exercises/`: enunciados y soluciones separados.
- `src/mcandes_fenicsx/`: utilidades pequeñas de metadatos, mallas y
  verificación MPI-safe.
- `tests/`: pruebas unitarias, regresiones numéricas y ejecución paralela.

## Licencias

El código original se distribuye bajo MIT; véase [`LICENSE-CODE`](LICENSE-CODE).
El texto, las figuras y el material didáctico original se distribuyen bajo CC BY
4.0; véase [`LICENSE-CONTENT`](LICENSE-CONTENT). Cada activo de terceros conserva
su atribución específica.

## Ruta recomendada

1. instalación y sanity check;
2. fundamentos matemáticos;
3. primer Poisson completo;
4. objetos, mallas, fronteras, espacios y convergencia;
5. una ruta por física;
6. PETSc, MPI, I/O y proyecto libre.

El sitio publicado contiene el
[mapa navegable](https://mc-andes.github.io/fenicsx-course/learning-path/).

## Cita

Use la metadata de [`CITATION.cff`](CITATION.cff). La release `v1.0.0` será la
primera versión estable y podrá enlazarse a un DOI de Zenodo cuando la
organización active esa integración.
