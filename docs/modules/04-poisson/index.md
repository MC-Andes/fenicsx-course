# Módulo 4 · De la PDE a la forma débil: Poisson

**Nivel:** inicial · **Tiempo:** 4 h · **Prerrequisitos:** módulos 1–3, integración por partes.

## Objetivos

Implementarás la cadena forma fuerte → forma débil → UFL → PETSc y medirás
errores L2/H1 con tasas MPI-safe.

## Modelo físico y unidades

En (Ω=(0,1)^2), se fabrica
(u=\sin(\pi x)\sin(\pi y)), (f=2\pi^2u). Puede interpretarse como potencial
o temperatura estacionaria adimensional.

## Forma fuerte y condiciones

\[
-\nabla^2u=f\quad\text{en }\Omega,\qquad u=0\quad\text{en }\partial\Omega.
\]

Dirichlet fija el espacio afín; Neumann aparecería como flujo natural y Robin
añadiría términos de contorno en ambos lados.

## Derivación débil

Multiplicar por (v\in H_0^1), integrar y aplicar Green:

\[
\int_\Omega \nabla u\cdot\nabla v\,dx=\int_\Omega fv\,dx.
\]

## Mapa matemático → UFL/DOLFINx

| Matemática | Implementación |
| --- | --- |
| (V_h\subset H^1) | `fem.functionspace(domain, ("Lagrange", 1))` |
| (u_h,v_h) | `TrialFunction`, `TestFunction` |
| (a(u,v)) | `inner(grad(u), grad(v))*dx` |
| (L(v)) | `inner(f, v)*dx` |
| (u=0) | `locate_dofs_topological` + `dirichletbc` |

## Ejemplo e inspección

Ejecuta `python examples/04_poisson_manufactured.py --quick --output results`.
Inspecciona celdas globales, DOF, facetas de frontera y el JSON de cada
refinamiento. Usa `--write-fields` solo después de que la validación numérica pase.

## Solver

`LinearProblem` recibe el prefijo no vacío `mcandes_poisson_<n>_`, LU y
`ksp_error_if_not_converged`. Además se exige `getConvergedReason()>0`.

## Verificación cuantitativa

Para P1 suave se esperan (\|e\|_{L^2}=O(h^2)) y
(|e|_{H^1}=O(h)). Los umbrales 1.8/0.9 toleran mallas gruesas sin aceptar un
orden equivocado.

## Visualización

XDMF permite ParaView. Una forma sinusoidal plausible no prueba las tasas; el
JSON es la evidencia primaria.

## Errores frecuentes

- Signo incorrecto de (f) tras integración por partes.
- Localizar geometría pero aplicar BC a DOF equivocados.
- Ensamblar error por rango sin `Allreduce`.
- Omitir la razón KSP o usar tolerancia bit a bit.

## Ejercicios graduados

1. Añade condición Neumann en la arista superior.
2. Implementa Robin y verifica con otra solución manufacturada.
3. Compara P1/P2 separando error de discretización y costo.

## Solución o guía

Neumann entra en (L(v)) como (\int_{\Gamma_N}gv\,ds); Robin
(\partial_nu+\alpha u=r) añade (\alpha uv) a (a) y (rv) a (L).
Conserva una porción Dirichlet o controla el nullspace constante.

## Fuentes, licencia, versión y cambios

[Demo oficial Poisson 0.11](https://docs.fenicsproject.org/dolfinx/v0.11.0.post0/python/demos/demo_poisson.html).
La formulación manufacturada, estudio dual L2/H1 y salida JSON son del curso.
