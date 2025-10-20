from __future__ import annotations
from typing import Iterable, Tuple
from .models import EnrichedItem

def compute_totals(items: Iterable[EnrichedItem]) -> Tuple[float, float, float]:
    total_bruto = sum(i.cantidad * i.precio_unitario for i in items)
    descuento = 0.0
    if total_bruto > 500:
        descuento += total_bruto * 0.10 
    total_neto = total_bruto - descuento
    return round(total_bruto, 2), round(descuento, 2), round(total_neto, 2)
