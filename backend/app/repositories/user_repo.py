from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user_schema import UserCreate
from ..core.security import get_password_hash 
from sqlalchemy import func
import math

#buscando usario pelo email
def get_user_by_email(db: Session, email: str) -> User | None:
    
    return db.query(User).filter(User.email == email).first()

#criando usuario no banco
def create_user(db: Session, user_data: UserCreate) -> User:   
    # gera o hash da senha ante de salvar
    hashed_password = get_password_hash(user_data.password)
    
    db_user = User(
        email=user_data.email,
        password_hash=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#buscando usuarios publicos
def get_all_users_paginated(
    db: Session, page: int = 1, limit: int = 20
) -> tuple[list[User], int]:
    """Busca todos os usuários públicos, com paginação."""
    query = db.query(User)
    
    total_items = query.count()
    
    offset = (page - 1) * limit
    users = query.offset(offset).limit(limit).all()
    
    return (users, total_items)