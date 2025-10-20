from typing import Any

def _to_number(x: Any) -> float:
    try: return float(x)
    except Exception: raise ValueError(f"No se puede convertir '{x}' a número")

def suma(var1: Any, var2: Any) -> float:
    return _to_number(var1) + _to_number(var2)

def resta(var1: Any, var2: Any) -> float:
    return _to_number(var1) - _to_number(var2)

def mayuscula_a_minuscula(var1: Any, var2: Any | None = None) -> str:
    s1 = str(var1).lower()
    return s1 if var2 is None else f"{s1} {str(var2).lower()}"

def concat_ws(var1: str, var2: str) -> str:
    return f"{var1}_{var2}"
  