from __future__ import annotations
import asyncio, json, logging
from datetime import datetime
from typing import Any, Dict, List
from .db import DB
from .models import Order
from .enrichment import enrich_items
from .pricing import compute_totals
from .hash_utils import make_order_hash
from .logging_conf import configure_logging

class OrderProcessor:
    def __init__(self, db_path: str = "orders.db", workers: int = 3, max_retries: int = 3) -> None:
        self.db = DB(db_path)
        self.queue: "asyncio.Queue[tuple[Dict[str, Any], int]]" = asyncio.Queue()
        self.dlq: List[Dict[str, Any]] = []
        self.workers = workers
        self.max_retries = max_retries
        self.log = logging.getLogger("pipeline")

    async def _process_once(self, raw: Dict[str, Any]) -> None:
        order = Order.model_validate(raw)
        enriched_items, warnings = await enrich_items(order.productos)
        total_bruto, descuento, total_neto = compute_totals(enriched_items)

        payload_for_hash = {
            "order_id": order.id,
            "cliente": order.cliente,
            "fecha": order.fecha.isoformat(),
            "items": [i.model_dump() for i in enriched_items],
            "totales": {"bruto": total_bruto, "descuento": descuento, "neto": total_neto},
        }
        order_hash = make_order_hash(payload_for_hash)

        row = {
            "order_id": order.id,
            "cliente": order.cliente,
            "fecha": order.fecha.isoformat(),
            "total_bruto": total_bruto,
            "descuento": descuento,
            "total_neto": total_neto,
            "hash": order_hash,
            "details_json": json.dumps(payload_for_hash, ensure_ascii=False),
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        inserted = await self.db.insert_processed(row)
        if inserted:
            self.log.info("Pedido procesado", extra={"extra": {"order_id": order.id, "warnings": warnings}})
        else:
            self.log.info("Pedido ya existía (idempotente)", extra={"extra": {"order_id": order.id}})

    async def worker(self, name: str) -> None:
        while True:
            raw, attempt = await self.queue.get()
            try:
                await self._process_once(raw)
            except Exception as ex:
                if attempt < self.max_retries:
                    backoff = 2 ** attempt
                    self.log.warning("Fallo; reintentando",
                        extra={"extra":{"order_id": raw.get("id"), "attempt": attempt, "sleep": backoff, "error": str(ex)}}
                    )
                    await asyncio.sleep(backoff)
                    await self.queue.put((raw, attempt + 1))
                else:
                    self.log.error("Fallo definitivo; DLQ", extra={"extra":{"order_id": raw.get("id"), "error": str(ex)}})
                    self.dlq.append(raw)
            finally:
                self.queue.task_done()

    async def run(self, orders: List[Dict[str, Any]]) -> None:
        configure_logging()
        await self.db.init()
        for o in orders:
            await self.queue.put((o, 0))
        tasks = [asyncio.create_task(self.worker(f"w{i}")) for i in range(self.workers)]
        await self.queue.join()
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        if self.dlq:
            self.log.error("DLQ contiene pedidos no procesados", extra={"extra": {"size": len(self.dlq)}})
        await self.db.close()
