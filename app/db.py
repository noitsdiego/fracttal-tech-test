import aiosqlite
from typing import Any, Dict

DDL = """
CREATE TABLE IF NOT EXISTS processed_orders (
    order_id INTEGER PRIMARY KEY,
    cliente TEXT NOT NULL,
    fecha TEXT NOT NULL,
    total_bruto REAL NOT NULL,
    descuento REAL NOT NULL,
    total_neto REAL NOT NULL,
    hash TEXT NOT NULL,
    details_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""

class DB:
    def __init__(self, path: str = "orders.db") -> None:
        self.path = path
        self._conn: aiosqlite.Connection | None = None

    async def init(self) -> None:
        self._conn = await aiosqlite.connect(self.path)
        await self._conn.execute("PRAGMA journal_mode=WAL;")
        await self._conn.execute(DDL)
        await self._conn.commit()

    @property
    def conn(self) -> aiosqlite.Connection:
        assert self._conn is not None, "DB no inicializada"
        return self._conn

    async def insert_processed(self, row: Dict[str, Any]) -> bool:
        sql = (
            "INSERT OR IGNORE INTO processed_orders "
            "(order_id, cliente, fecha, total_bruto, descuento, total_neto, hash, details_json, created_at) "
            "VALUES (:order_id, :cliente, :fecha, :total_bruto, :descuento, :total_neto, :hash, :details_json, :created_at)"
        )
        cur = await self.conn.execute(sql, row)
        await self.conn.commit()
        return cur.rowcount == 1

    async def close(self) -> None:
        if self._conn:
            await self._conn.close()
            self._conn = None
