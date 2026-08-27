# Módulo 1 · Variables, funciones y expresiones

**Nivel:** inicial · **Tiempo:** 2 h · **Prerrequisitos:** módulo 0, NumPy.

## Objetivos

Distinguirás escalares/arreglos Python, `fem.Constant`, `fem.Function`,
`SpatialCoordinate`, expresiones UFL y funciones de prueba/ensayo; actualizarás
un campo sin tratar su vector local como arreglo global.

## Modelo y unidades

Se interpola (g(x,y)=\sin(\pi x)\sin(\pi y)) en el cuadrado unidad. Todo es
adimensional; no hay ecuación gobernante ni condiciones de frontera.

## Forma fuerte y débil

No hay PDE. La operación discreta es encontrar (g_h\in V_h) cuyos grados de
libertad reproduzcan los funcionales de interpolación de (g). La forma de
masa `inner(trial, test)*dx` se construye solo para mostrar simbolismo; no se
resuelve.

## Mapa concepto → software

| Cantidad | Representación correcta |
| --- | --- |
| parámetro mutable | `fem.Constant(domain, value)` |
| campo discreto | `fem.Function(V)` |
| coordenada simbólica | `ufl.SpatialCoordinate(domain)` |
| incógnita lineal | `ufl.TrialFunction(V)` |
| variación | `ufl.TestFunction(V)` |
| valores locales + fantasmas | `function.x.array` |

## Ejemplo mínimo e inspección

Ejecuta `python examples/01_interpolation.py --quick --output results`. Inspecciona
el tamaño propio con `V.dofmap.index_map.size_local`, el bloque con
`index_map_bs` y los fantasmas con `num_ghosts`. Tras asignar, llama
`field.x.scatter_forward()`.

## Solver

La interpolación no usa KSP. Cambiar una `Constant` evita recompilar una forma;
cambiar una expresión Python interpolada modifica los coeficientes de una
`Function`.

## Verificación cuantitativa

El error L2 de interpolación debe decrecer aproximadamente como (h^2) para P1
y (h^3) para P2. El ejemplo exige tasas >1.7 y >2.5 en la última pareja.

## Visualización

Una superficie suave puede ocultar un orden incorrecto. Grafica solo después
de conservar la tabla de (h), error y tasa.

## Errores frecuentes

- Comparar `field.x.array` entre MPI 1/2 como si el orden fuera global.
- Usar una `Function` donde se necesita `TrialFunction`.
- Esperar valores numéricos de una expresión UFL sin interpolar/ensamblar.
- Olvidar actualizar fantasmas tras escribir coeficientes.

## Ejercicios graduados

1. Clasifica diez objetos en Python, NumPy, DOLFINx discreto o UFL simbólico.
2. Sustituye (g) por un polinomio cuadrático y predice qué espacio lo reproduce.
3. Añade P3 y verifica su tasa sin copiar el vector a rango 0.

## Solución o guía

P2 reproduce exactamente un polinomio cuadrático (salvo redondeo). La tasa P3
esperada para una función suave es 4 en L2. Usa la reducción de
`global_l2_error`, no `np.linalg.norm` sobre un rango.

## Fuentes, licencia, versión y cambios

DOLFINx 0.11.0.post0. Implementación original MIT, página CC BY 4.0. Se inspira
en el demo oficial de interpolación, pero añade comparación P1/P2, reducción
global, metadata y criterio obligatorio.
