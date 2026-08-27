# Mallas

Las geometrías fuente se conservan en `meshes/source` cuando una página necesita
un archivo `.geo`. Las mallas `.msh`, XDMF y resultados derivados no se versionan:
se regeneran desde scripts y se validan por grupos físicos, medidas y cantidades
de interés. Actualmente las geometrías OCC canónicas viven en
`src/mcandes_fenicsx/gmsh_models.py` para compartir la misma implementación con
las pruebas.
