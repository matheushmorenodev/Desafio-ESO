from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from .config import settings

# --- Importações das dependências do FastAPI ---
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from ..core.database import get_db
from ..models.user import User 


# --- Hashing de Senha ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- DEFINIÇÃO DOS ESQUEMAS (DEVE VIR ANTES DAS FUNÇÕES) ---
oauth2_scheme_strict = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)
# --- FIM DAS DEFINIÇÕES ---

def truncate_password(password: str) -> str:
    return password[:72] 

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano bate com o hash salvo."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha em texto plano."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Cria um novo token JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

# --- FUNÇÃO DE DEPENDÊNCIA OBRIGATÓRIA ---
async def get_current_active_user(
    token: str = Depends(oauth2_scheme_strict), # Agora 'oauth2_scheme_strict' existe
    db: Session = Depends(get_db)
) -> User:
    """
    Dependência obrigatória. 
    Exige um token válido e retorna o usuário logado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: Optional[int] = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# --- FUNÇÃO DE DEPENDÊNCIA OPCIONAL ---
async def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme_optional), # Agora 'oauth2_scheme_optional' existe
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Tenta pegar o usuário logado. Se não houver token, retorna None."""
    if token is None:
        return None
        
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: Optional[int] = payload.get("user_id")
        if user_id is None:
            return None 
    except JWTError:
        return None 

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return None
    return user