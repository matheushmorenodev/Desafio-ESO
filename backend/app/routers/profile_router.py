from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..core.security import get_current_active_user 
from ..models.user import User
from ..repositories import cosmetic_repo
from ..schemas.cosmetic_schema import CosmeticPublic
from ..schemas.transaction_schema import TransactionHistoryResponse
from ..schemas.user_schema import UserPublic

router = APIRouter(
    prefix="/profile/me", # Prefixo para todos os endpoints "meu perfil"
    tags=["Meu Perfil (Privado)"],
    dependencies=[Depends(get_current_active_user)] 
)

@router.get("/inventory", response_model=List[CosmeticPublic])
def get_my_inventory(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Retorna todos os cosméticos adquiridos pelo usuário logado
    items = cosmetic_repo.get_user_inventory(db, user_id=current_user.id)
    
    processed_items = []
    for item in items:
        public_item = CosmeticPublic.model_validate(item)
        public_item.is_acquired = True
        processed_items.append(public_item)
        
    return processed_items

#Retorna o histórico de compras e devoluções do usuário logado.
@router.get("/history", response_model=List[TransactionHistoryResponse])
def get_my_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):

    history = cosmetic_repo.get_user_transaction_history(db, user_id=current_user.id)
    return history

#endpoint meu perfil
@router.get("/", response_model=UserPublic)
def get_my_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Retorna os dados do perfil do usuário logado (incluindo saldo de V-Bucks).
    """
    # A dependência 'get_current_active_user' já busca o usuário
    # no banco para nós. Só precisamos retorná-lo.
    return current_user
