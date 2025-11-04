from fastapi import FastAPI
from .core.database import engine, Base
from .models import user, cosmetic, inventory, transaction
from .routers import auth_router, cosmetic_router, profile_router, user_router, shop_router

from contextlib import asynccontextmanager
from .tasks.sync_data import update_shop_status 
from .core.database import SessionLocal
import httpx
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicação...")
    db = SessionLocal()
    
    try:
        print("Inicializando tabelas do banco de dados (Base.metadata.create_all)...")
        Base.metadata.create_all(bind=engine)
        print("Tabelas inicializadas.")
    except Exception as e:
        print(f"ERRO ao inicializar tabelas: {e}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # --- 2. REMOVA A LÓGICA DE 'sync_all_cosmetics' ---
            # (Nós vamos rodar isso manualmente)
            
            # Deixe apenas o update rápido (que não vai quebrar)
            print("Rodando 'update_shop_status' para sincronizar a loja...")
            await update_shop_status(db, client)
            print("Sincronização da loja na inicialização concluída.")
            
        except Exception as e:
            print(f"ERRO ao sincronizar a loja na inicialização: {e}")
        finally:
            db.close()
    
    yield 
    print("Desligando aplicação...")

# ... (O resto do arquivo é o mesmo) ...
# (Criação do app FastAPI, CORS, routers, etc.)

app = FastAPI(
    title="ESO Desafio Fortnite API",
    description="Backend para o processo seletivo da Sistema ESO.",
    lifespan=lifespan 
)

# Adiciona a middleware de CORS
from fastapi.middleware.cors import CORSMiddleware

origins = [
    # Permite o localhost (para desenvolvimento)
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    
    # 1. A URL do frontend
    "https://desafio-eso-git-main-matheus-projects-e754.vercel.app",

    "https://eso-api.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # <-- Usa a nova lista de 'origins'
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API do Desafio ESO!"}

# --- Inclui os roteadores ---
app.include_router(auth_router.router, prefix="/api")
app.include_router(cosmetic_router.router, prefix="/api")
app.include_router(profile_router.router, prefix="/api")
app.include_router(user_router.router, prefix="/api")
app.include_router(shop_router.router, prefix="/api")