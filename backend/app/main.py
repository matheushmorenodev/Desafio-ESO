from fastapi import FastAPI
from .core.database import engine, Base
from .models import user, cosmetic, inventory, transaction
from .routers import auth_router, cosmetic_router, profile_router, user_router, shop_router

# --- IMPORTS DO LIFESPAN ---
from contextlib import asynccontextmanager
# 1. ADICIONE A IMPORTAÇÃO FALTANTE:
from .tasks.sync_data import update_shop_status, sync_all_cosmetics 
from .core.database import SessionLocal
import httpx
from sqlalchemy import text
# --- FIM DOS IMPORTS ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicação...")
    db = SessionLocal()
    
    # --- 2. MOVA O CREATE_ALL PARA DENTRO DO LIFESPAN ---
    # Isso roda ANTES dos workers e previne a 'race condition'
    try:
        print("Inicializando tabelas do banco de dados (Base.metadata.create_all)...")
        Base.metadata.create_all(bind=engine)
        print("Tabelas inicializadas.")
    except Exception as e:
        print(f"ERRO ao inicializar tabelas: {e}")
    # --- FIM DA MUDANÇA ---
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # --- Lógica de Sync (sem mudanças) ---
            cosmetic_count = db.execute(text("SELECT COUNT(id) FROM cosmetics")).scalar()
            
            if cosmetic_count == 0:
                print("Banco de dados vazio. Rodando Sincronização Mestra (pode demorar)...")
                await sync_all_cosmetics(db, client)
            else:
                print("Banco de dados já populado.")

            print("Rodando 'update_shop_status' para sincronizar a loja...")
            await update_shop_status(db, client)
            print("Sincronização da loja na inicialização concluída.")
            
        except Exception as e:
            print(f"ERRO ao sincronizar a loja na inicialização: {e}")
        finally:
            db.close()
    
    yield 
    print("Desligando aplicação...")

# --- O CREATE_ALL FOI REMOVIDO DAQUI ---
# Base.metadata.create_all(bind=engine) <-- LINHA ANTIGA REMOVIDA

app = FastAPI(
    title="ESO Desafio Fortnite API",
    description="Backend para o processo seletivo da Sistema ESO.",
    lifespan=lifespan 
)

# Adiciona a middleware de CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        # (No futuro, adicione a URL do seu Vercel aqui)
    ], 
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