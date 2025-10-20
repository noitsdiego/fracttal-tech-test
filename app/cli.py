from __future__ import annotations
import argparse, asyncio, json
from pathlib import Path
from typing import Any, Dict, List
from .pipeline import OrderProcessor

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="orders", description="Procesa pedidos con cola asíncrona")
    p.add_argument("--orders", required=True, help="Ruta a archivo JSON (objeto o lista de pedidos)")
    p.add_argument("--workers", type=int, default=3, help="Número de workers (default 3)")
    p.add_argument("--db", default="orders.db", help="Ruta SQLite (default orders.db)")
    return p.parse_args()

def _load_orders(path: str) -> List[Dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return [data]
    if not isinstance(data, list):
        raise ValueError("El archivo debe contener un objeto de pedido o una lista")
    return data

def main() -> None:
    ns = parse_args()
    op = OrderProcessor(db_path=ns.db, workers=ns.workers)
    asyncio.run(op.run(_load_orders(ns.orders)))

if __name__ == "__main__":
    main()
