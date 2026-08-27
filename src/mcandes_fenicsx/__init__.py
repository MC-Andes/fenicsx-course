"""Utilidades pequeñas y explícitas para el curso FEniCSx de MC-Andes."""

from mcandes_fenicsx.metadata import ExampleMetadata, load_metadata
from mcandes_fenicsx.results import emit_result
from mcandes_fenicsx.verification import convergence_rates

__all__ = ["ExampleMetadata", "convergence_rates", "emit_result", "load_metadata"]
__version__ = "0.1.0"
