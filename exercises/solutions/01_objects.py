"""Una solución razonada del ejercicio de objetos."""

ANSWERS = {
    "material_parameter": "fem.Constant",
    "discrete_temperature": "fem.Function",
    "coordinate_formula": "UFL expression with SpatialCoordinate",
    "unknown_linear_field": "ufl.TrialFunction",
}

if __name__ == "__main__":
    assert set(ANSWERS) == {
        "material_parameter",
        "discrete_temperature",
        "coordinate_formula",
        "unknown_linear_field",
    }
    for key, answer in ANSWERS.items():
        print(f"{key}: {answer}")
