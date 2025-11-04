from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import re # Precisamos importar a biblioteca de Regex do Python

# --- Schemas de Usuário ---

#campo base de um usuario
class UserBase(BaseModel):
    email: EmailStr
#criando um usuario
class UserCreate(UserBase):
    
    password: str = Field(
        ..., 
        min_length=6,  # Mínimo de 6 caracteres (ainda é válido)
        max_length=72, # Máximo de 72 (limite do bcrypt - ainda é válido)
        description=(
            "A senha deve ter entre 6 e 72 caracteres, "
            "conter pelo menos uma letra maiúscula e "
            "um caractere especial."
        )
    )

    # valida a senha
    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
       
        if not v: # Garante que não é uma string vazia (apesar do min_length)
            raise ValueError('A senha não pode ser vazia.')

        # 1. Checa se tem letra maiúscula
        if not re.search(r'[A-Z]', v):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula.')
        
        # 2. Checa se tem caractere especial
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", v):
            raise ValueError('A senha deve conter pelo menos um caractere especial.')
        
        # 3. Se passou em tudo, retorna a senha
        return v

#retorna dados publicos de usuario
class UserPublic(UserBase):
    id: int
    vbucks: int
    created_at: datetime

    class Config:
        from_attributes = True 


# resposta paginada de usuario
class PaginatedUserResponse(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    items: list[UserPublic]

# Schemas de Autenticação

#retorna o token no login
class Token(BaseModel):
    """Schema para retornar o token JWT no login."""
    access_token: str
    token_type: str

#dados guardados no token
class TokenData(BaseModel):
    user_id: int | None = None

