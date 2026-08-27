"""Añade etiquetas inferior/superior y completa EXPECTED antes de --check."""

from __future__ import annotations

import argparse

EXPECTED: dict[int, float | None] = {
    1: 1.0,
    2: 1.0,
    3: None,  # TODO: frontera inferior de un rectángulo 3x1
    4: None,  # TODO: frontera superior
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        print("Rectángulo 3x1: completa las longitudes y adapta el ejemplo 02.")
        return 0
    if any(value is None for value in EXPECTED.values()):
        print("TODO: EXPECTED todavía contiene valores None")
        return 1
    assert EXPECTED == {1: 1.0, 2: 1.0, 3: 3.0, 4: 3.0}
    print("Medidas esperadas correctas; verifica ahora mediante ds(marker).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
