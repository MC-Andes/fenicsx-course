"""Solución robusta del balance de fuerzas."""


def relative_balance(reaction: float, applied: float) -> float:
    return abs(reaction + applied) / max(abs(applied), 1.0e-15)


if __name__ == "__main__":
    assert relative_balance(-0.2, 0.2) == 0.0
    assert relative_balance(-0.199, 0.2) > 0.0
    print("Balance verificado")
