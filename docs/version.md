# Versiones, soporte y mantenimiento

| Curso | DOLFINx | Python | Estado |
| --- | --- | --- | --- |
| 0.1.x | 0.11.* | 3.12 | desarrollo público |
| 1.x | 0.11.* | 3.12 | objetivo estable |

Los arreglos didácticos/técnicos son releases patch; nuevas lecciones compatibles,
minor; una migración general de DOLFINx puede requerir major. Se revisan issues
y enlaces cada mes, el entorno cada semestre y la siguiente versión estable una
vez al año.

## Lista de reproducción de release

1. Resolver un entorno limpio y registrar versiones.
2. Ejecutar unitarias, smoke serial, subconjunto MPI y nightly completo.
3. Construir documentación estricta y auditar enlaces/atribuciones.
4. Actualizar changelog y `CITATION.cff`.
5. Publicar prerelease, probar Ubuntu/Apple Silicon y solicitar validación externa.
6. Etiquetar SemVer, publicar Pages y verificar rollback.
