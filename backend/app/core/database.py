from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings # Importa nossas configurações

# Criando engine de conexão usando url do .env
engine = create_engine(settings.DATABASE_URL)

# Criando fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que nossos modelos (tabelas) irão herdar
Base = declarative_base()

# Função "helper" para Injeção de Dependência no FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()