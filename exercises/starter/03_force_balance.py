"""Implementa una diferencia relativa robusta y ejecuta --check."""

from __future__ import annotations

import argparse


def relative_balance(reaction: float, applied: float) -> float | None:
    # TODO: reacción y carga tienen signos opuestos; evita dividir por cero.
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        print("Completa relative_balance; prueba reacción=-0.2 y carga=0.2.")
        return 0
    value = relative_balance(-0.2, 0.2)
    if value is None:
        print("TODO: relative_balance no está implementada")
        return 1
    assert value < 1.0e-14
    print(f"Balance correcto: {value:.3e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
