from fastapi import FastAPI
from .core.database import engine, Base
from .models import user, cosmetic, inventory, transaction
from .routers import auth_router, cosmetic_router, profile_router, user_router, shop_router

# --- IMPORTS DO LIFESPAN ---
from contextlib import asynccontextmanager
from .tasks.sync_data import update_shop_status, sync_all_cosmetics 
from .core.database import SessionLocal
import httpx
from sqlalchemy import text
# --- FIM DOS IMPORTS ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Função executada na inicialização e desligamento da API.
    """
    print("Iniciando aplicação...")
    db = SessionLocal()
    
    # 1. CRIA AS TABELAS (Movemos para dentro do lifespan)
    #    Isso roda ANTES dos workers e previne a 'race condition'
    #    de 'duplicate key (transactiontype)'
    try:
        print("Inicializando tabelas do banco de dados (Base.metadata.create_all)...")
        Base.metadata.create_all(bind=engine)
        print("Tabelas inicializadas.")
    except Exception as e:
        print(f"ERRO ao inicializar tabelas: {e}")
    
    # 2. RODA A SINCRONIZAÇÃO
    #    (Removemos o 'sync_all_cosmetics' daqui para evitar
    #    o erro 'Ran out of memory' de 512MB do Render)
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Roda apenas o update rápido (que não vai quebrar)
            print("Rodando 'update_shop_status' para sincronizar a loja...")
            await update_shop_status(db, client)
            print("Sincronização da loja na inicialização concluída.")
            
        except Exception as e:
            print(f"ERRO ao sincronizar a loja na inicialização: {e}")
        finally:
            db.close()
    
    yield 
    print("Desligando aplicação...")

# --- O 'Base.metadata.create_all' foi removido daqui ---

app = FastAPI(
    title="ESO Desafio Fortnite API",
    description="Backend para o processo seletivo da Sistema ESO.",
    lifespan=lifespan 
)

# Adiciona a middleware de CORS
from fastapi.middleware.cors import CORSMiddleware

# --- 3. CORREÇÃO DO CORS (Lista de Permissão) ---
origins = [
    # Permite o localhost (para desenvolvimento)
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "https://desafio-eso.vercel.app",
    
    
    # A URL de preview do seu Vercel 
    "https://desafio-eso-git-main-matheus-projects-e7534acb.vercel.app",
    "https://desafio-eso-latcomj8-matheus-projects-e7534acb.vercel.app",
    
    "https://eso-api.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message":"Bem-vindo à API do Desafio ESO!"}

# --- Inclui os roteadores com o prefixo /api global ---
app.include_router(auth_router.router, prefix="/api")
app.include_router(cosmetic_router.router, prefix="/api")
app.include_router(profile_router.router, prefix="/api")
app.include_router(user_router.router, prefix="/api")
app.include_router(shop_router.router, prefix="/api")