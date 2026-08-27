# Comprobación previa de conocimientos

Esta página es privada para ti: no envía respuestas, no asigna una nota y no
bloquea ningún módulo. Úsala para decidir qué repasar antes de empezar.

Intenta resolver sin consultar fuentes:

1. En NumPy, crea 100 puntos y evalúa (\sin(\pi x)).
2. Explica la diferencia entre gradiente y divergencia.
3. Integra por partes (-u''=f) con Dirichlet homogéneo.
4. Describe una condición inicial y una de frontera.
5. Crea/activa un entorno y ejecuta un script con argumento.
6. Explica por qué sumar valores locales de dos procesos requiere comunicación.

## Pistas para decidir el siguiente paso

- Si 1 o 5 no son familiares, repasa Python, NumPy y terminal.
- Si 2–4 no son familiares, repasa cálculo vectorial y PDE antes del módulo 4.
- Si 6 no es familiar, puedes empezar; el módulo 0 presenta el modelo MPI.

Una forma esperada para 3 es
(\int u'v'\,dx=\int fv\,dx) cuando el término de frontera desaparece. En 6,
la suma global se obtiene con una colectiva como `MPI.Allreduce`.
