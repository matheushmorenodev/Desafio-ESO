from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import math
from datetime import datetime
from typing import Optional, List

from ..core.database import get_db
from ..schemas.cosmetic_schema import CosmeticPublic, PaginatedCosmeticResponse
from ..schemas.user_schema import UserPublic
from ..repositories import cosmetic_repo
from ..models.inventory import Inventory
from ..models.transaction import TransactionType
from ..models.user import User

# --- IMPORTAÇÕES CORRIGIDAS ---
# Agora importamos apenas as FUNÇÕES de dependência do security.py
from ..core.security import get_current_active_user, get_optional_current_user
# --- FIM DA CORREÇÃO ---

router = APIRouter(
    prefix="/cosmetics",
    tags=["Cosméticos"]
)

@router.get("/", response_model=PaginatedCosmeticResponse)
def get_all_cosmetics(
    # A dependência 'get_optional_current_user' já usa o 'oauth2_scheme_optional'
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
    
    # Filtros
    name: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    rarity: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    is_new: Optional[bool] = Query(None),
    is_on_sale: Optional[bool] = Query(None),
    is_on_promotion: Optional[bool] = Query(None),
    
    # Paginação
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Lista todos os cosméticos com filtros e paginação.
    """
    
    filters = cosmetic_repo.CosmeticFilterParams(
        name=name, type=type, rarity=rarity,
        date_from=date_from, date_to=date_to,
        is_new=is_new, is_on_sale=is_on_sale,
        is_on_promotion=is_on_promotion
    )
    
    (items, total_items) = cosmetic_repo.get_cosmetics_with_filters(
        db, filters=filters, page=page, limit=limit
    )
    
    processed_items = []
    acquired_ids = set()
    
    if current_user:
        user_inventory = db.query(Inventory.cosmetic_id).filter(
            Inventory.user_id == current_user.id
        ).all()
        acquired_ids = {item_id for (item_id,) in user_inventory}

    for item in items:
        public_item = CosmeticPublic.model_validate(item)
        if public_item.id in acquired_ids:
            public_item.is_acquired = True
        processed_items.append(public_item)

    total_pages = math.ceil(total_items / limit)
    
    return PaginatedCosmeticResponse(
        total_items=total_items,
        total_pages=total_pages,
        current_page=page,
        items=processed_items
    )

@router.get("/{cosmetic_id}", response_model=CosmeticPublic)
def get_cosmetic_details(
    cosmetic_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user) 
):
    """
    [Requisito PDF] Retorna os detalhes completos de um único cosmético.
    """
    cosmetic = cosmetic_repo.get_cosmetic_by_id(db, cosmetic_id)
    if not cosmetic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cosmético não encontrado."
        )

    public_item = CosmeticPublic.model_validate(cosmetic)
    
    if current_user:
        inventory_item = cosmetic_repo.get_inventory_item(
            db, user_id=current_user.id, cosmetic_id=cosmetic_id
        )
        if inventory_item:
            public_item.is_acquired = True
            
    return public_item

@router.post(
    "/{cosmetic_id}/buy", 
    status_code=status.HTTP_200_OK,
    response_model=UserPublic
)
def buy_cosmetic(
    cosmetic_id: str,
    db: Session = Depends(get_db),
    # A dependência 'get_current_active_user' já usa o 'oauth2_scheme_strict'
    current_user: User = Depends(get_current_active_user)
):
    """
    Compra um cosmético. Retorna os dados do usuário atualizado (com novo saldo).
    """
    cosmetic = cosmetic_repo.get_cosmetic_by_id(db, cosmetic_id)
    if not cosmetic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cosmético não encontrado.")

    if not cosmetic.is_on_sale or cosmetic.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este item não está disponível para compra."
        )

    if current_user.vbucks < cosmetic.price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="V-Bucks insuficientes."
        )
        
    existing_item = cosmetic_repo.get_inventory_item(db, current_user.id, cosmetic_id)
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Você já possui este item."
        )
        
    try:
        current_user.vbucks -= cosmetic.price
        db.add(current_user)
        
        cosmetic_repo.add_item_to_inventory(db, current_user, cosmetic)
        
        cosmetic_repo.create_transaction(
            db, 
            user=current_user, 
            cosmetic=cosmetic,
            type=TransactionType.PURCHASE, 
            value= -cosmetic.price
        )
        
        db.commit()
        db.refresh(current_user)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Ocorreu um erro ao processar a compra: {e}"
        )

    return current_user

@router.post(
    "/{cosmetic_id}/return", 
    status_code=status.HTTP_200_OK,
    response_model=UserPublic
)
def return_cosmetic(
    cosmetic_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Devolve um cosmético. Retorna os dados do usuário atualizado (com novo saldo).
    """
    cosmetic = cosmetic_repo.get_cosmetic_by_id(db, cosmetic_id)
    if not cosmetic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cosmético não encontrado.")
        
    inventory_item = cosmetic_repo.get_inventory_item(db, current_user.id, cosmetic_id)
    if not inventory_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Você não possui este item para devolver."
        )
        
    last_purchase = cosmetic_repo.get_last_purchase_transaction(db, current_user.id, cosmetic_id)
    
    if not last_purchase or last_purchase.value >= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Não foi possível encontrar o valor da transação original."
        )
        
    refund_amount = abs(last_purchase.value)

    try:
        current_user.vbucks += refund_amount
        db.add(current_user)
        
        cosmetic_repo.remove_item_from_inventory(db, inventory_item)
        
        cosmetic_repo.create_transaction(
            db, 
            user=current_user, 
            cosmetic=cosmetic,
            type=TransactionType.RETURN, 
            value= refund_amount
        )
        
        db.commit()
        db.refresh(current_user)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Ocorreu um erro ao processar a devolução: {e}"
        )
        
    return current_user