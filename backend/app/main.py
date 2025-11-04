from fastapi import FastAPI
from .core.database import engine, Base
from .models import user, cosmetic, inventory, transaction
from .routers import auth_router, cosmetic_router, profile_router, user_router, shop_router

from contextlib import asynccontextmanager
from .tasks.sync_data import update_shop_status 
from .core.database import SessionLocal
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicação...")
    print("Rodando 'update_shop_status' para sincronizar a loja...")
    
    db = SessionLocal()
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Rodamos o script de update rápido
            await update_shop_status(db, client)
            print("Sincronização da loja na inicialização concluída.")
        except Exception as e:
            print(f"ERRO ao sincronizar a loja na inicialização: {e}")
        finally:
            db.close()
    
    yield

    print("Desligando aplicação...")



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ESO Desafio Fortnite API",
    description="Backend para o processo seletivo da Sistema ESO.",
    lifespan=lifespan 
)

# Adiciona a middleware de CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], #porta do React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API do Desafio ESO!"}

#rotas
app.include_router(auth_router.router, prefix="/api")
app.include_router(cosmetic_router.router, prefix="/api")
app.include_router(profile_router.router, prefix="/api")
app.include_router(user_router.router, prefix="/api")
app.include_router(shop_router.router, prefix="/api")