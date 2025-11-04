from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional # Use "Optional" em versões mais antigas do Python

class CosmeticBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    type: Optional[str] = None
    rarity: Optional[str] = None
    price: int
    image_url: Optional[str] = None
    added_at: Optional[datetime] = None

class CosmeticPublic(CosmeticBase):
    """O que mostramos na listagem e detalhes."""
    is_new: bool
    is_on_sale: bool
    is_on_promotion: bool
    
    # Adicionamos o "status" de comprado, que virá da sua lógica
    is_acquired: bool = False # O padrão é 'não adquirido'

    class Config:
        from_attributes = True

class PaginatedCosmeticResponse(BaseModel):
    """Define o formato da resposta paginada."""
    total_items: int
    total_pages: int
    current_page: int
    items: list[CosmeticPublic]