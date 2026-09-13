# Lección 1 · Matemática mínima y forma débil

**Nivel:** inicial · **Tiempo:** 90 min · **Prerrequisitos:** lección 0, cálculo diferencial e integral.

## Por qué esta lección va antes del código

FEniCSx no ofrece un menú para elegir “calor” o “elasticidad”. Tú declaras los
campos y escribes la formulación variacional. Esta lección reúne únicamente la
matemática que reaparece en las demás páginas; la lección 2 la convierte en un
programa completo.

## Objetivos

Al terminar podrás:

- distinguir campos escalares, vectoriales y tensoriales;
- interpretar `grad`, `div`, `sym`, `inner`, `dx` y `ds`;
- derivar la forma débil de Poisson mediante integración por partes;
- diferenciar condiciones esenciales y naturales;
- identificar incógnita, función de ensayo y función de prueba.

## Campos y operadores

| Objeto físico | Tipo | Ejemplo | UFL frecuente |
| --- | --- | --- | --- |
| temperatura o presión | escalar | $T(x)$ | `T` |
| desplazamiento o velocidad | vector | $u(x)$ | `u` |
| deformación o tensión | tensor | $\varepsilon(u)$ | `sym(grad(u))` |
| cambio espacial de un escalar | vector | $\nabla T$ | `grad(T)` |
| expansión de un vector | escalar | $\nabla\cdot u$ | `div(u)` |
| producto o contracción | escalar | $A:B$ | `inner(A, B)` |

`grad` aumenta el orden del objeto: un escalar produce un vector y un vector
produce un tensor. `div` contrae una dirección. En elasticidad se usa la parte
simétrica del gradiente porque una rotación rígida no es deformación.

## Dominio, frontera y medidas

Sea $\Omega$ el dominio y $\partial\Omega$ su frontera.

| Medida | Región de integración | Uso típico |
| --- | --- | --- |
| `dx` | celdas de $\Omega$ | fuente, energía, masa |
| `ds` | frontera exterior | flujo, tracción, convección |
| `ds(tag)` | parte etiquetada de la frontera | condición natural localizada |
| `dS` | facetas interiores | métodos DG; no se usa en el primer solve |

La malla aproxima la geometría y las medidas indican dónde se integra. Una
etiqueta no impone por sí sola una condición: solamente identifica entidades.

## De la forma fuerte a la débil

Considera Poisson:

\[
-\nabla^2 u=f\quad\text{en }\Omega,
\qquad u=0\quad\text{en }\partial\Omega.
\]

### 1. Elegir una función de prueba

Multiplicamos por una variación admisible $v$. Como $u$ está fijada en la
frontera, $v$ debe anularse allí.

### 2. Integrar en el dominio

\[
-\int_\Omega (\nabla^2 u)v\,dx=\int_\Omega fv\,dx.
\]

### 3. Integrar por partes

La identidad de Green mueve una derivada de $u$ hacia $v$:

\[
\int_\Omega \nabla u\cdot\nabla v\,dx
-\int_{\partial\Omega}(\nabla u\cdot n)v\,ds
=\int_\Omega fv\,dx.
\]

El término de frontera desaparece en la parte Dirichlet porque $v=0$. Si se
prescribe un flujo $g=\nabla u\cdot n$ en otra parte, permanece en el lado
derecho como una integral sobre `ds`.

### 4. Enunciar el problema variacional

Encontrar $u\in V$ tal que, para todo $v\in V_0$,

\[
a(u,v)=L(v),\qquad
a(u,v)=\int_\Omega\nabla u\cdot\nabla v\,dx,
\qquad L(v)=\int_\Omega fv\,dx.
\]

Al restringir $V$ a un espacio finito $V_h$, la igualdad se convierte en el
sistema algebraico $A\mathbf{u}=\mathbf{b}$.

## Ensayo, prueba y solución

| Papel | Símbolo | Objeto |
| --- | --- | --- |
| incógnita simbólica lineal | $u_h$ | `ufl.TrialFunction(V)` |
| variación | $v_h$ | `ufl.TestFunction(V)` |
| solución con coeficientes | $u_h$ después del solve | `fem.Function(V)` |
| dato mutable | $f$, material o tiempo | `fem.Constant` o `fem.Function` |

La `TrialFunction` no contiene valores. Sirve para construir una forma lineal
en la incógnita. La `Function` sí almacena los coeficientes de la solución.

## Condiciones de frontera

### Dirichlet o esencial

Prescribe el valor de la incógnita, por ejemplo $u=g$. Se aplica a grados de
libertad con `dirichletbc`; no se añade como una carga a `L`.

### Neumann o natural

Prescribe un flujo o una tracción. Aparece en la integral de frontera obtenida
por integración por partes. Neumann homogénea suele no requerir código extra.

### Robin o mixta

Relaciona valor y flujo. Una condición $\partial_n u+\alpha u=r$ añade un
término con $u$ a la forma bilineal y otro con $r$ al lado derecho.

## El mapa que usarás en la lección 2

```python
# Esquema conceptual; la implementación completa está en la lección 2.
u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)
a = ufl.inner(ufl.grad(u), ufl.grad(v)) * ufl.dx
L = f * v * ufl.dx
```

Lee cada línea de derecha a izquierda: región de integración, operación sobre
campos y papel de cada función. Todavía faltan malla, espacio, frontera, solve y
verificación; la siguiente página conecta las ocho piezas.

## Comprobación antes de avanzar

1. ¿Por qué el método no usa directamente $\nabla^2u$ con elementos P1?
2. ¿Dónde aparecería un flujo conocido?
3. ¿Qué diferencia hay entre `TrialFunction` y `Function`?
4. ¿Qué evidencia usarías para comprobar Poisson si conoces una solución exacta?

**Respuestas breves:** integración por partes reduce la regularidad; el flujo
aparece en `ds`; ensayo es simbólico y solución almacena coeficientes; se puede
medir el error y su tasa al refinar.

## Fuentes y versión

- [Manual UFL](https://docs.fenicsproject.org/ufl/2026.1.0/manual.html).
- [Demo oficial de Poisson en DOLFINx 0.11](https://docs.fenicsproject.org/dolfinx/v0.11.0.post0/python/demos/demo_poisson.html).
- [Tutorial de FEniCSx de Dokken](https://jsdokken.com/dolfinx-tutorial/chapter1/fundamentals.html), CC BY 4.0.

El texto y los ejemplos conceptuales de esta página son originales de MC-Andes.

---

**Anterior:** [orientación](../modules/00-orientation/index.md) ·
**Siguiente:** [primer problema completo — Poisson](../modules/04-poisson/index.md)
