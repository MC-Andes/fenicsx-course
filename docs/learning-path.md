# Mapa del curso y rutas de aprendizaje

El curso tiene un **núcleo común** y varias rutas por física. No necesitas leer
las trece lecciones como si fueran un manual lineal. Primero aprende el ciclo
completo de una simulación con Poisson; después vuelve sobre cada pieza con más
detalle y elige la física que necesitas.

## La idea que conecta todo

Toda simulación del curso recorre el mismo ciclo:

1. declarar el dominio y la malla;
2. escoger el elemento y el espacio de funciones;
3. definir datos, incógnitas y funciones de prueba;
4. escribir la forma débil con UFL;
5. imponer condiciones de frontera;
6. ensamblar y resolver con PETSc;
7. verificar una cantidad independiente;
8. guardar o visualizar solo después de validar.

Las lecciones cambian la física, pero conservan este vocabulario. Cada página
indica qué pasos son nuevos y cuáles se reutilizan.

## Recorrido recomendado

| Etapa | Lecciones | Pregunta que resuelve | Evidencia |
| --- | --- | --- | --- |
| Preparación | instalación, diagnóstico y 0 | ¿puedo ejecutar el entorno correcto? | sanity check serial/MPI |
| Primer modelo | 1–2 | ¿cómo se convierte una PDE en un solve? | Poisson manufacturado |
| Herramientas FEM | 3–5 | ¿qué representan objetos, mallas, fronteras y espacios? | interpolación, medidas y tasas |
| Primera física | 6 o 7 | ¿cómo cambia el patrón en tiempo o en un campo vectorial? | energía o equilibrio |
| Especialización | 8–12 | ¿cómo trato geometría, mezcla, no linealidad o acoplamiento? | benchmark verificado |
| Cierre | PETSc, MPI e I/O | ¿cómo reproduzco y escalo el resultado? | comparación serial/MPI |

!!! tip "Primer hito"
    No intentes memorizar la API antes de la lección 2. Ejecuta Poisson,
    identifica sus ocho pasos y después usa las lecciones 3–5 para entenderlos.

## Rutas según tu objetivo

### Ruta esencial — una primera PDE

Completa 0 → 1 → 2. Al final podrás leer un problema escalar lineal, reconocer
su forma débil y ejecutar una solución con comprobación de error.

### Ruta térmica

Completa 0–6. Poisson funciona como conducción estacionaria; la lección 6 añade
estado previo, paso temporal y balance de energía.

### Ruta de mecánica de sólidos

Completa 0–5 y continúa con 7 → 8 → 9. Consulta la
[guía de sólidos](tracks/solids.md) para decidir si necesitas materiales
múltiples, Gmsh o grandes deformaciones.

### Ruta de mecánica de fluidos

Completa 0–5 y continúa con 10 → 11. Consulta la
[guía de fluidos](tracks/fluids.md). Stokes introduce el sistema mixto;
Navier–Stokes añade convección e iteración de Picard.

### Ruta de multifísica

Completa 0–6, 9 y luego 12. Cahn–Hilliard combina tiempo, espacio mixto y solve
no lineal; por eso no es una buena primera simulación.

### Ruta rápida para usuarios con experiencia

Si ya conoces FEM o FEniCS legado:

1. ejecuta la lección 0 y revisa las versiones;
2. estudia el pipeline de la lección 2;
3. compara los objetos de la lección 3 con `dolfin` legado;
4. revisa las etiquetas de la lección 4 y los prefijos PETSc;
5. salta a la ruta física de interés.

## Señales para avanzar

Avanza cuando puedas responder sin mirar el código:

- ¿cuál es la incógnita y en qué espacio vive?;
- ¿qué condición es esencial y cuál aparece como término natural?;
- ¿qué integral o norma demuestra que el resultado es razonable?;
- ¿cómo sabrías que PETSc no convergió?;
- ¿qué cambia y qué permanece si refinas la malla?

Si alguna respuesta no es clara, vuelve a la lección enlazada desde el mensaje
de “prerrequisitos” de la página actual.

## Qué no forma parte de la ruta

- Los [ejemplos](examples/index.md) son implementaciones de apoyo, no capítulos
  que debas leer completos de arriba abajo.
- Los JSON en `results/` son evidencia regenerable, no material de estudio.
- Los cuadernos Jupyter no son necesarios: toda la ruta utiliza scripts `.py`.
- Visualizar es opcional; verificar es obligatorio.

## Criterio de diseño

La secuencia matemática → Poisson → rutas por física toma como referencia la
organización general de
[Robiolab/FEniCSx-tutorials](https://github.com/Robiolab/FEniCSx-tutorials),
adaptada a DOLFINx 0.11, español, scripts verificables, MPI y navegación web.
No se ha copiado su código.

---

**Siguiente:** [instala y comprueba el entorno](setup.md) o, si ya funciona,
empieza por [la orientación](modules/00-orientation/index.md).
