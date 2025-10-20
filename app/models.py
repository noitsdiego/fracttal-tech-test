from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class Item(BaseModel):
    sku: str
    cantidad: int = Field(gt=0)
    precio_unitario: float = Field(ge=0)

    @field_validator("sku")
    @classmethod
    def sku_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("SKU no puede estar vacío")
        return v

class EnrichedItem(Item):
    product_id: Optional[int] = None
    title: Optional[str] = None
    api_price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None

class Order(BaseModel):
    id: int
    cliente: str
    productos: List[Item]
    fecha: datetime

    @field_validator("cliente")
    @classmethod
    def cliente_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Cliente no puede estar vacío")
        return v
