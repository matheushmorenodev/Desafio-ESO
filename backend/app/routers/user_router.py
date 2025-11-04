from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
import math

from ..core.database import get_db
from ..models.user import User
from ..repositories import user_repo, cosmetic_repo
from ..schemas.user_schema import UserPublic, PaginatedUserResponse
from ..schemas.cosmetic_schema import CosmeticPublic

router = APIRouter(
    prefix="/users",
    tags=["Usuários (Público)"]
)

#retorna lista publica dos usuarios
@router.get("/", response_model=PaginatedUserResponse)
def get_public_user_list(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    (users, total_items) = user_repo.get_all_users_paginated(db, page, limit)
    
    total_pages = math.ceil(total_items / limit)
    
    return PaginatedUserResponse(
        total_items=total_items,
        total_pages=total_pages,
        current_page=page,
        items=users 
    )

#retorna inventario de um usuario 
@router.get("/{user_id}/inventory", response_model=List[CosmeticPublic])
def get_user_public_inventory(
    user_id: int,
    db: Session = Depends(get_db)
):
    #validando se o usuário existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    items = cosmetic_repo.get_user_inventory(db, user_id=user_id)
    
    processed_items = []
    for item in items:
        public_item = CosmeticPublic.model_validate(item)
        public_item.is_acquired = True
        processed_items.append(public_item)
        
    return processed_items