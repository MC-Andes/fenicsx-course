FROM ghcr.io/fenics/dolfinx/dolfinx:v0.11.0@sha256:2ae4bfbc0d9077268880faf04c72750528bee986c94ab223a2c159969bd56fa8

WORKDIR /course
COPY . /course
RUN python3 -m pip install --no-cache-dir -e ".[dev,docs]" pyyaml gmsh pyvista
CMD ["python3", "examples/00_sanity_check.py", "--output", "results"]
