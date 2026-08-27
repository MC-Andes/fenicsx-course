# Entorno reproducible

## Ruta principal: micromamba/conda-forge

```bash
git clone https://github.com/MC-Andes/fenicsx-course.git
cd fenicsx-course
micromamba create -f environment.yml
micromamba activate mcandes-fenicsx-course
python examples/00_sanity_check.py --output results
mpirun -n 2 python examples/00_sanity_check.py --output results-mpi
pytest tests/unit
mkdocs serve
```

El entorno fija Python 3.12 y `fenics-dolfinx=0.11.*`. Para reproducir exactamente
el entorno validado, usa el lock correspondiente y después instala el paquete
local del curso:

=== "Ubuntu x86_64"

    ```bash
    conda-lock install --name mcandes-fenicsx-course conda-lock.yml
    micromamba run -n mcandes-fenicsx-course python -m pip install -e .
    ```

=== "macOS Apple Silicon"

    ```bash
    micromamba create -n mcandes-fenicsx-course -f conda-osx-arm64.lock
    micromamba run -n mcandes-fenicsx-course python -m pip install -e .
    ```

`conda-lock.yml` fija el entorno Linux usado por CI. `conda-osx-arm64.lock` es
el export explícito, con hashes, del entorno en el que se ejecutó la batería
completa local. La dependencia editable `-e .` se instala aparte por diseño.
macOS Intel se comprueba por release. Windows nativo no está garantizado: usa
WSL2 o el contenedor.

## Recuperación mediante contenedor

La imagen de la release está fijada por etiqueta y digest en
`containers/Dockerfile`.

```bash
docker build -f containers/Dockerfile -t mcandes/fenicsx-course:0.1.0 .
docker run --rm -v "$PWD/results:/course/results" mcandes/fenicsx-course:0.1.0
docker run --rm -v "$PWD:/course" -w /course mcandes/fenicsx-course:0.1.0 \
  mpirun -n 2 python3 examples/04_poisson_manufactured.py --quick --output results
```

## Comprobación esperada

El JSON `results/sanity-check.json` debe informar DOLFINx 0.11, el número de
procesos solicitado, ocho celdas globales y ambas banderas de validación en
`true`. Si MPI informa ejecución como `root` dentro del contenedor, añade las
opciones recomendadas por la implementación MPI de la imagen, no desactives
comprobaciones en el script.

## Política de versiones

`v1.x` conservará DOLFINx 0.11. Una migración a 0.12 usará rama dedicada,
entorno separado, batería numérica completa, baselines justificados y
prerelease. Los enlaces del curso apuntan a documentación 0.11, nunca a `main`
sin marcarla como desarrollo.
