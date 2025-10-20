import argparse, importlib, inspect, pkgutil
from typing import Any, Callable, Dict

def _discover_functions(package_name: str = "operations") -> Dict[str, Callable[..., Any]]:
    pkg = importlib.import_module(package_name)
    funcs: Dict[str, Callable[..., Any]] = {}
    for m in pkgutil.iter_modules(pkg.__path__):  # type: ignore
        mod = importlib.import_module(f"{package_name}.{m.name}")
        for name, obj in inspect.getmembers(mod, inspect.isfunction):
            if not name.startswith("_"):
                funcs[name] = obj
    return funcs

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="ops", description="Ejecutor dinámico de operaciones")
    p.add_argument("func", help="Nombre de la función (suma/resta/mayuscula_a_minuscula/...)")
    p.add_argument("var1", help="Primer parámetro")
    p.add_argument("var2", nargs="?", default=None, help="Segundo parámetro (opcional)")
    return p.parse_args()

def main() -> None:
    ns = parse_args()
    funcs = _discover_functions("operations")
    if ns.func not in funcs:
        raise SystemExit(f"Función '{ns.func}' no encontrada. Disponibles: {', '.join(sorted(funcs.keys()))}")
    fn = funcs[ns.func]
    print(fn(ns.var1) if ns.var2 is None else fn(ns.var1, ns.var2))

if __name__ == "__main__":
    main()
