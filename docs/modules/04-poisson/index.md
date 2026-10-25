# Lección 2 · Primer problema completo: Poisson

**Nivel:** inicial · **Tiempo:** 3 h · **Prerrequisitos:** lecciones 0–1 y laboratorio guiado.

## Por qué Poisson aparece primero

Poisson reúne todas las piezas de una simulación sin introducir campos
vectoriales, tiempo o no linealidad. Primero ejecutarás el ciclo completo;
las lecciones 3–5 regresan a objetos, mallas y espacios para explicarlos con
detalle. No necesitas memorizar cada llamada antes de comenzar.

!!! tip "Si es tu primera simulación"
    Comienza por el [laboratorio guiado](../../guides/first-simulation.md). Allí
    cada bloque tiene una predicción, un fragmento de código y una pausa de
    comprobación. Esta página funciona como resumen matemático y técnico.

## Objetivos

Implementarás la cadena forma fuerte → forma débil → UFL → PETSc y medirás
errores L2/H1 con tasas MPI-safe.

## Modelo físico y unidades

En $\Omega=(0,1)^2$, se fabrica
$u=\sin(\pi x)\sin(\pi y)$, $f=2\pi^2u$. Puede interpretarse como potencial
o temperatura estacionaria adimensional.

## Forma fuerte y condiciones

\[
-\nabla^2u=f\quad\text{en }\Omega,\qquad u=0\quad\text{en }\partial\Omega.
\]

Dirichlet fija el espacio afín; Neumann aparecería como flujo natural y Robin
añadiría términos de contorno en ambos lados.

## Derivación débil

Multiplicar por $v\in H_0^1$, integrar y aplicar Green:

\[
\int_\Omega \nabla u\cdot\nabla v\,dx=\int_\Omega fv\,dx.
\]

## Mapa matemático → UFL/DOLFINx

| Matemática | Implementación |
| --- | --- |
| $V_h\subset H^1$ | `fem.functionspace(domain, ("Lagrange", 1))` |
| $u_h,v_h$ | `TrialFunction`, `TestFunction` |
| $a(u,v)$ | `inner(grad(u), grad(v))*dx` |
| $L(v)$ | `inner(f, v)*dx` |
| $u=0$ | `locate_dofs_topological` + `dirichletbc` |

## Ejemplo e inspección

Ejecuta:

```bash
python examples/01_poisson_manufactured.py --quick --output results
```

Después abre `results/poisson-manufactured.json` y sigue este orden:

1. `solver_reasons`: todos los valores deben ser positivos;
2. `l2_errors` y `h1_seminorm_errors`: deben disminuir al refinar;
3. `l2_rates` y `h1_rates`: deben aproximarse a 2 y 1;
4. `validation_passed`: debe ser `true`.

Usa `--write-fields` solo después de que la validación numérica pase.

## El pipeline de ocho pasos

| Paso | Pregunta | Dónde profundizar |
| ---: | --- | --- |
| 1 | ¿cuál es el dominio? | lección 4 |
| 2 | ¿qué espacio aproxima $u$? | lección 5 |
| 3 | ¿qué datos cambian? | lección 3 |
| 4 | ¿cuál es la forma débil? | lección 1 |
| 5 | ¿qué frontera fija valores? | lección 4 |
| 6 | ¿qué sistema resuelve PETSc? | herramientas transversales |
| 7 | ¿cómo se mide el error? | lección 5 |
| 8 | ¿qué se conserva como evidencia? | repertorio verificable |

![Refinamiento y convergencia esperada para elementos P1](../../assets/figures/poisson-convergence.svg){ .lesson-figure loading=lazy }

<p class="figure-caption">El refinamiento cambia el tamaño de malla; la pendiente de los errores comprueba si la discretización responde como predice la teoría.</p>

## Qué debe ocurrir en cada etapa

| Etapa | Entrada | Salida | Señal de error |
| --- | --- | --- | --- |
| geometría | `n`, tipo de celda | `domain` | número de celdas inesperado |
| discretización | malla, familia, grado | `space` | DOF o continuidad inadecuados |
| formulación | ensayo, prueba, fuente | `a`, `L` | signo o medida incorrectos |
| frontera | facetas, espacio, valor | `bc` | sistema singular o borde incorrecto |
| solve | formas, BC, opciones | `solution` | razón PETSc negativa |
| validación | exacta y refinamientos | error y tasa | `validation_passed=false` |

Esta tabla es también una ruta de diagnóstico: busca primero la etapa que
produce la primera evidencia incorrecta, no el último mensaje del programa.

## Solver

`LinearProblem` recibe el prefijo no vacío `mcandes_poisson_<n>_`, LU y
`ksp_error_if_not_converged`. Además se exige `getConvergedReason()>0`.

## Verificación cuantitativa

Para P1 suave se esperan $\|e\|_{L^2}=O(h^2)$ y
$|e|_{H^1}=O(h)$. Los umbrales 1.8/0.9 toleran mallas gruesas sin aceptar un
orden equivocado.

## Visualización

XDMF permite ParaView. Una forma sinusoidal plausible no prueba las tasas; el
JSON es la evidencia primaria.

## Errores frecuentes

- Signo incorrecto de $f$ tras integración por partes.
- Localizar geometría pero aplicar BC a DOF equivocados.
- Ensamblar error por rango sin `Allreduce`.
- Omitir la razón KSP o usar tolerancia bit a bit.

## Ejercicios graduados

1. Añade condición Neumann en la arista superior.
2. Implementa Robin y verifica con otra solución manufacturada.
3. Compara P1/P2 separando error de discretización y costo.

## Solución o guía

Neumann entra en $L(v)$ como $\int_{\Gamma_N}gv\,ds$; Robin
$\partial_n u+\alpha u=r$ añade $\alpha uv$ a $a$ y $rv$ a $L$.
Conserva una porción Dirichlet o controla el nullspace constante.

## Fuentes, licencia, versión y cambios

[Demo oficial Poisson 0.11](https://docs.fenicsproject.org/dolfinx/v0.11.0.post0/python/demos/demo_poisson.html).
La formulación manufacturada, estudio dual L2/H1 y salida JSON son del curso.

---

**Anterior:** [laboratorio guiado](../../guides/first-simulation.md) ·
**Siguiente:** [objetos de DOLFINx y UFL](../01-variables/index.md)
