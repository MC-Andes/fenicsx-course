"""Clasifica objetos del ecosistema; completa ANSWERS y ejecuta --check."""

from __future__ import annotations

import argparse

QUESTIONS = {
    "material_parameter": "¿Python float, Constant, Function o UFL expression?",
    "discrete_temperature": "¿Python float, Constant, Function o UFL expression?",
    "coordinate_formula": "¿Python float, Constant, Function o UFL expression?",
    "unknown_linear_field": "¿Function, TrialFunction o TestFunction?",
}

# TODO: reemplaza None por la categoría correcta.
ANSWERS: dict[str, str | None] = {key: None for key in QUESTIONS}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        for key, question in QUESTIONS.items():
            print(f"{key}: {question}")
        return 0
    missing = [key for key, answer in ANSWERS.items() if answer is None]
    if missing:
        print(f"TODO pendientes: {', '.join(missing)}")
        return 1
    print("Todas las respuestas están completas; compáralas con la guía.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
