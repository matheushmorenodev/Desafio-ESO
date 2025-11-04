from pydantic import BaseModel
from datetime import datetime
from ..models.transaction import TransactionType
from .cosmetic_schema import CosmeticPublic 
from typing import Optional

# Mude o nome para algo mais descritivo
class TransactionHistoryResponse(BaseModel):
    """Schema para exibir um item do histórico (com dados aninhados)."""
    type: TransactionType
    value: int
    created_at: datetime
    cosmetic: Optional[CosmeticPublic] = None
    offer_id: Optional[str] = None

    class Config:
        from_attributes = True