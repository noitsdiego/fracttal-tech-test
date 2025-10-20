from __future__ import annotations
import re, aiohttp
from typing import List, Tuple
from .models import Item, EnrichedItem

FAKESTORE_BASE = "https://fakestoreapi.com"

def _sku_to_product_id(sku: str) -> int | None:
    m = re.search(r"(\d+)$", sku)
    if not m:
        return None
    return int(m.group(1).lstrip("0") or "0")

async def enrich_items(items: List[Item]) -> Tuple[List[EnrichedItem], list[str]]:
    warnings: list[str] = []
    out: list[EnrichedItem] = []

    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for it in items:
            pid = _sku_to_product_id(it.sku)
            data = None
            if pid:
                url = f"{FAKESTORE_BASE}/products/{pid}"
                try:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                        else:
                            warnings.append(f"SKU {it.sku}: status {resp.status} en {url}")
                except Exception as ex:
                    warnings.append(f"SKU {it.sku}: error {ex}")

            out.append(EnrichedItem(
                **it.model_dump(),
                product_id=(data.get("id") if data else None),
                title=(data.get("title") if data else None),
                api_price=(float(data.get("price")) if data and data.get("price") is not None else None),
                description=(data.get("description") if data else None),
                category=(data.get("category") if data else None),
            ))
    return out, warnings
