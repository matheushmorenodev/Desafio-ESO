from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..core.database import get_db
from ..schemas.user_schema import UserCreate, UserPublic, Token
from ..repositories import user_repo # Nosso repositório
from ..core import security # Nossas funções de segurança

#criando um roteador
router = APIRouter(
    prefix="/auth", # O prefixo da URL (ex: /api/auth/...)
    tags=["Autenticação"] # Agrupa endpoints na documentação
)

# rota de registro de usuário
@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    db_user = user_repo.get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado."
        )
    new_user = user_repo.create_user(db=db, user_data=user_data)

    return new_user

# rota de login
@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # 1. Busca o usuário pelo e-mail (no form OAuth, o "username" é o nosso e-mail)
    user = user_repo.get_user_by_email(db, email=form_data.username)
    
    # 2. Verifica se o usuário existe E se a senha está correta
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Se tudo estiver certo, cria o token JWT
    access_token = security.create_access_token(
        data={"user_id": user.id} # Os dados que queremos guardar no token
    )
    
    return {"access_token": access_token, "token_type": "bearer"}