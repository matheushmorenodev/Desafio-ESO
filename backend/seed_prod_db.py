import asyncio
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
# Importa todos os modelos para que o Base.metadata saiba sobre eles
from app.models import cosmetic, user, inventory, transaction 
from app.tasks.sync_data import sync_all_cosmetics

# --- URL REAL DO SEU BANCO DE DADOS RENDER ---
# (Nós adicionamos o "postgresql+psycopg2://" no início)
RENDER_DB_URL = "postgresql+psycopg2://eso_db_pbpq_user:EFOyy9GYlrVHgpffQfk87a2plE3hOwqC@dpg-d44uc6idbo4c73atvsr0-a.oregon-postgres.render.com/eso_db_pbpq"

engine = create_engine(RENDER_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def seed_database():
    print(f"Conectando ao banco de dados de produção no Render...")
    db = SessionLocal()
    
    print("Criando tabelas (se não existirem)...")
    # Isso cria as tabelas (users, cosmetics, etc.) no seu banco online
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso.")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            print("--- INICIANDO SYNC MESTRA (Isso vai demorar 10-15 minutos) ---")
            await sync_all_cosmetics(db, client)
            print("--- Sincronização Mestra CONCLUÍDA ---")
        except Exception as e:
            print(f"Erro durante a sincronização: {e}")
            db.rollback()
        finally:
            db.close()

if __name__ == "__main__":
    print("Iniciando script de 'seeding' para o banco do Render...")
    asyncio.run(seed_database())