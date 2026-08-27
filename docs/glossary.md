# Glosario bilingüe

**Basix**
: Define y tabula elementos finitos; aporta las familias, grados, formas de
  valor y puntos de interpolación.

**DOLFINx**
: Biblioteca de alto nivel que coordina mallas, espacios, ensamblaje,
  condiciones, solvers e I/O. La grafía correcta es DOLFINx.

**FFCx**
: Compilador que transforma formas UFL en kernels de ensamblaje.

**FEniCSx**
: Ecosistema moderno compuesto por UFL, Basix, FFCx y DOLFINx.

**Grado de libertad (degree of freedom, DOF)**
: Coeficiente que determina una función discreta. En MPI, cada rango posee DOF
  propios y copias fantasma de algunos DOF vecinos.

**KSP / PC**
: Solver de Krylov y precondicionador de PETSc para sistemas lineales.

**MeshTags**
: Pares entidad–marcador para distinguir materiales, celdas o fronteras.

**MPI**
: Modelo de memoria distribuida. Una integral ensamblada localmente requiere
  reducción global para convertirse en una métrica física del dominio completo.

**PETSc / petsc4py**
: Infraestructura de álgebra lineal distribuida y su interfaz Python.

**SNES**
: Solver de sistemas no lineales de PETSc; su razón de convergencia debe
  comprobarse explícitamente.

**UFL**
: Lenguaje simbólico de formas. Una expresión UFL describe una operación; no es
  un arreglo de valores ya evaluados.

**Valores fantasma (ghost values)**
: Copias locales de información poseída por otro rango. `scatter_forward`
  actualiza estas copias después de modificar un campo distribuido.
