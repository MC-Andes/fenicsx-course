"""Solución de medidas del rectángulo 3x1."""

EXPECTED = {1: 1.0, 2: 1.0, 3: 3.0, 4: 3.0}

if __name__ == "__main__":
    perimeter = sum(EXPECTED.values())
    assert perimeter == 8.0
    print(f"Medidas: {EXPECTED}; perímetro={perimeter}")
