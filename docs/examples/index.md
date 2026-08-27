# Repertorio verificable de problemas

Aquí solo se catalogan problemas cuyo código ejecutable está incluido y cuya
comprobación se ejecuta localmente y en CI. Los scripts son la única fuente
ejecutable. Cada uno acepta `--quick`, `--output DIR` y `--write-fields` cuando
genera campos. Las fichas completas viven en `examples/metadata/`.

| Ejemplo | Nivel | Evidencia principal |
| --- | --- | --- |
| [00 · Sanity check](#sanity-check) | Inicial | versiones y celdas globales |
| [01 · Interpolación](#interpolacion) | Inicial | tasas P1/P2 |
| [02 · Fronteras etiquetadas](#fronteras-etiquetadas) | Inicial | medidas de fronteras |
| [03 · Espacios de funciones](#espacios-de-funciones) | Inicial | grados de libertad globales |
| [04 · Poisson manufacturado](#poisson-manufacturado) | Inicial | tasas L2/H1 |
| [05 · Difusión de calor](#difusion-de-calor) | Intermedio | error analítico y energía |
| [06 · Elasticidad lineal](#elasticidad-lineal) | Intermedio | reacción y energía |
| [07 · Placa con agujero](#placa-con-agujero) | Intermedio | concentración y malla |
| [08 · Dos materiales](#dos-materiales) | Intermedio | continuidad y balance |
| [09 · Canal de Stokes](#canal-de-stokes) | Intermedio | Poiseuille, caudal y divergencia |
| [10 · Flujo alrededor de cilindro](#flujo-alrededor-de-cilindro) | Avanzado | Picard, arrastre y masa |
| [11 · Hiperelasticidad](#hiperelasticidad) | Avanzado | SNES, energía y Jacobiano |
| [12 · Cahn–Hilliard](#cahn-hilliard) | Avanzado | masa y energía libre |

## Ejemplos completos

Cada enlace del catálogo llega a una sección autocontenida. El código se
incluye automáticamente desde el script canónico, por lo que la página y las
pruebas siempre muestran la misma implementación.

### 00 · Sanity check { #sanity-check }

```bash
python examples/00_sanity_check.py --output results
```

```python title="examples/00_sanity_check.py"
--8<-- "examples/00_sanity_check.py"
```

### 01 · Interpolación { #interpolacion }

```bash
python examples/01_interpolation.py --quick --output results
```

```python title="examples/01_interpolation.py"
--8<-- "examples/01_interpolation.py"
```

### 02 · Fronteras etiquetadas { #fronteras-etiquetadas }

```bash
python examples/02_tagged_boundaries.py --quick --output results
```

```python title="examples/02_tagged_boundaries.py"
--8<-- "examples/02_tagged_boundaries.py"
```

### 03 · Espacios de funciones { #espacios-de-funciones }

```bash
python examples/03_function_spaces.py --quick --output results
```

```python title="examples/03_function_spaces.py"
--8<-- "examples/03_function_spaces.py"
```

### 04 · Poisson manufacturado { #poisson-manufacturado }

```bash
python examples/04_poisson_manufactured.py --quick --output results
```

```python title="examples/04_poisson_manufactured.py"
--8<-- "examples/04_poisson_manufactured.py"
```

### 05 · Difusión de calor { #difusion-de-calor }

```bash
python examples/05_heat_diffusion.py --quick --output results
```

```python title="examples/05_heat_diffusion.py"
--8<-- "examples/05_heat_diffusion.py"
```

### 06 · Elasticidad lineal { #elasticidad-lineal }

```bash
python examples/06_linear_elasticity.py --quick --output results
```

```python title="examples/06_linear_elasticity.py"
--8<-- "examples/06_linear_elasticity.py"
```

### 07 · Placa con agujero { #placa-con-agujero }

```bash
python examples/07_plate_with_hole.py --quick --output results
```

```python title="examples/07_plate_with_hole.py"
--8<-- "examples/07_plate_with_hole.py"
```

### 08 · Dos materiales { #dos-materiales }

```bash
python examples/08_two_materials.py --quick --output results
```

```python title="examples/08_two_materials.py"
--8<-- "examples/08_two_materials.py"
```

### 09 · Canal de Stokes { #canal-de-stokes }

```bash
python examples/09_stokes_channel.py --quick --output results
```

```python title="examples/09_stokes_channel.py"
--8<-- "examples/09_stokes_channel.py"
```

### 10 · Flujo alrededor de cilindro { #flujo-alrededor-de-cilindro }

```bash
python examples/10_cylinder_flow.py --quick --output results
```

```python title="examples/10_cylinder_flow.py"
--8<-- "examples/10_cylinder_flow.py"
```

### 11 · Hiperelasticidad { #hiperelasticidad }

```bash
python examples/11_hyperelasticity.py --quick --output results
```

```python title="examples/11_hyperelasticity.py"
--8<-- "examples/11_hyperelasticity.py"
```

### 12 · Cahn–Hilliard { #cahn-hilliard }

```bash
python examples/12_cahn_hilliard.py --quick --output results
```

```python title="examples/12_cahn_hilliard.py"
--8<-- "examples/12_cahn_hilliard.py"
```

## Esquema de salida

Todos los JSON incluyen `example`, `dolfinx_version`, `mpi_size`,
`solver_converged` y `validation_passed`. Las pruebas comparan escalares,
normas/tendencias y nunca archivos binarios bit a bit.

## Regla para ampliar el repertorio

Un problema nuevo aparece aquí únicamente cuando entrega, en el mismo cambio:

1. ecuación, dominio, condiciones de frontera, parámetros y unidades;
2. script completo en `examples/` y ficha en `examples/metadata/`;
3. criterio cuantitativo con tolerancia explícita;
4. resultado JSON reproducible y al menos una prueba automatizada;
5. fuente técnica accesible y ejecución serial o MPI declarada.

Una lista externa de enunciados puede orientar ideas futuras, pero no se
presenta como parte del curso hasta que exista código comprobable aquí.
