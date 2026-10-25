# Lección 5 · Elementos, espacios y convergencia

**Nivel:** inicial · **Tiempo:** 3 h · **Prerrequisitos:** lecciones 3–4, álgebra lineal.

## Conexión con las lecciones anteriores

La malla describe la geometría; el elemento decide qué información vive en cada
celda; el espacio conecta ambos y numera grados de libertad. Esta lección cierra
el núcleo común explicando por qué refinar o cambiar el grado altera el error.

## Objetivos

Elegirás familias/grados, construirás espacios escalares, vectoriales,
tensoriales y mixtos, y localizarás DOF de subespacios sin confundir colapso con
una vista.

## Modelo y unidades

Una malla triangular sostiene cinco representaciones: P1 escalar, P2 vectorial,
DG0 tensorial y Taylor–Hood P2/P1. Solo se inspecciona discretización; no hay
unidades físicas.

## Forma fuerte y débil

No se prescribe PDE. La elección del espacio anticipa conformidad: Poisson usa
$H^1$, elasticidad un espacio vectorial $(H^1)^2$ y Stokes el producto
$V\times Q$ compatible con inf-sup.

## Mapa concepto → software

| Concepto | Objeto |
| --- | --- |
| elemento escalar | `basix.ufl.element` |
| valor vectorial | `shape=(gdim,)` |
| discontinuo | `("Discontinuous Lagrange", 0)` |
| producto | `mixed_element([P2, P1])` |
| vista de componente | `W.sub(i)` |
| espacio independiente + mapa | `W.sub(i).collapse()` |

![Ubicación de grados de libertad P1, P2 y DG0 sobre la misma celda](../../assets/figures/function-spaces.svg){ .lesson-figure loading=lazy }

<p class="figure-caption">La geometría no cambia: lo que cambia es la información que cada elemento representa y cómo se comparte entre celdas.</p>

## Ejemplo e inspección

Ejecuta `python examples/04_function_spaces.py --quick --output results`. El
número global de DOF es `size_global*index_map_bs`; el tamaño de `x.array`
incluye información local/fantasma y no es esa dimensión global.

### Decide el espacio con tres preguntas

1. **¿Qué tipo de valor tiene la incógnita?** Escalar, vector o tensor.
2. **¿Debe ser continua entre celdas?** Poisson P1 sí; un material DG0 no.
3. **¿Qué grado necesitas?** Relaciónalo con regularidad, costo y tasa esperada.

Después construye el espacio y comprueba su dimensión global. En un problema
mixto añade una cuarta pregunta: ¿qué subespacio recibe cada condición?

!!! question "Punto de control"
    `W.sub(i)` es una vista dentro del espacio mixto. `collapse()` crea un
    espacio independiente y un mapa; no son intercambiables al localizar DOF.

## Solver

No hay solver. En lecciones posteriores, el orden de bloques y los mapas de
subespacio determinarán las condiciones esenciales y el precondicionador.

## Verificación cuantitativa

El espacio P2 vectorial debe superar P1 escalar; el mixto debe superar el bloque
de velocidad y el mapa de presión colapsada no puede ser vacío.

## Visualización

Visualiza coordenadas de DOF para P1/P2 y centroides para DG0. No conectes puntos
DG0 como si fueran nodos continuos.

## Errores frecuentes

- Aplicar una BC del espacio colapsado sin el mapa al subespacio mixto.
- Confundir grado geométrico, grado del elemento y tasa observada.
- Proyectar siempre cuando una interpolación compatible es suficiente.
- Usar igual orden P1/P1 para Stokes sin estabilización.

## Ejercicios graduados

1. Cuenta DOF P1/P2 en tres mallas y explica su escalamiento.
2. Crea un tensor simétrico DG0 y compara almacenamiento con tensor completo.
3. Construye Taylor–Hood y localiza únicamente la componente x en una frontera.

## Solución o guía

Usa pares `(W.sub(0), V_colapsado)` en `locate_dofs_topological` para BC mixtas.
No reconstruyas índices manualmente.

## Fuentes, licencia y versión

[Basix 0.11](https://docs.fenicsproject.org/basix/v0.11.0/python/) y DOLFINx
0.11.0.post0. Código MIT, texto CC BY 4.0.

---

**Anterior:** [mallas, etiquetas y fronteras](../02-meshes/index.md) ·
**Siguiente:** [elige una ruta de especialización](../../learning-path.md#rutas-segun-tu-objetivo)
