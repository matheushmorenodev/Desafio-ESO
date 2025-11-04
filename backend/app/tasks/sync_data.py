import asyncio
import httpx
from datetime import datetime, timezone # <-- MUDANÇA AQUI (adicionei timezone)
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Importa a SessionLocal e a Base do nosso app
from ..core.database import SessionLocal, Base, engine
# Importa todos os nossos modelos
from ..models import cosmetic, user, inventory, transaction 
from ..models.cosmetic import Cosmetic # Importa a classe específica

# URL base da API do Fortnite
FORTNITE_API_BASE_URL = "https://fortnite-api.com/v2"

# -------------------------------------------------------------------
# FUNÇÃO 1: Sincronizar o Catálogo Mestre (/cosmetics/br)
# -------------------------------------------------------------------
async def sync_all_cosmetics(db: Session, client: httpx.AsyncClient):
    """
    Busca TODOS os cosméticos da API e os salva no banco (UPSERT).
    Esta é a operação mais pesada e demorada.
    """
    print("Iniciando Sincronização Mestra de Cosméticos...")
    try:
        response = await client.get(f"{FORTNITE_API_BASE_URL}/cosmetics/br")
        response.raise_for_status() # Lança erro se a resposta não for 200 OK
        
        api_items = response.json().get("data", [])
        if not api_items:
            print("Nenhum item encontrado na API /cosmetics/br.")
            return

        print(f"Encontrados {len(api_items)} itens no catálogo mestre.")
        
        # Pega todos os IDs que já existem no banco para otimizar
        existing_ids = set(
            row[0] for row in db.query(Cosmetic.id).all()
        )
        print(f"Encontrados {len(existing_ids)} itens existentes no banco local.")

        new_items_count = 0
        updated_items_count = 0

        for api_item in api_items:
            if not api_item.get("id"):
                continue

            item_id = api_item["id"]
            
            # --- Parse da Data ---
            added_at_str = api_item.get("added")
            added_at_date = None
            if added_at_str:
                try:
                    # Converte a string ISO (ex: "2021-10-12T08:35:19Z") para datetime
                    added_at_date = datetime.fromisoformat(added_at_str.replace('Z', '+00:00'))
                except ValueError:
                    print(f"Formato de data inválido para {item_id}: {added_at_str}")
                    added_at_date = None
            
            # --- Parse da Imagem ---
            image_url = None
            if api_item.get("images") and api_item["images"].get("icon"):
                image_url = api_item["images"]["icon"]
            
            # --- Cria o objeto do modelo ---
            cosmetic_data = {
                "id": item_id,
                "name": api_item.get("name"),
                "description": api_item.get("description"),
                "type": api_item.get("type", {}).get("value"),
                "rarity": api_item.get("rarity", {}).get("value"),
                "image_url": image_url,
                "added_at": added_at_date,
                "last_sync": datetime.now(timezone.utc) 
            }

            # --- Lógica de UPSERT (Update ou Insert) ---
            if item_id in existing_ids:
                # Atualiza
                db.query(Cosmetic).filter(Cosmetic.id == item_id).update(cosmetic_data)
                updated_items_count += 1
            else:
                # Insere
                db.add(Cosmetic(**cosmetic_data))
                new_items_count += 1
        
        db.commit() # Comita todas as mudanças de uma vez
        print(f"Sincronização Mestra Concluída: {new_items_count} novos, {updated_items_count} atualizados.")

    except httpx.HTTPStatusError as e:
        print(f"Erro HTTP ao buscar /cosmetics/br: {e}")
    except Exception as e:
        print(f"Erro inesperado no sync_all_cosmetics: {e}")
        db.rollback()
# -------------------------------------------------------------------
# FUNÇÃO 2: Atualizar Status da Loja (/shop e /cosmetics/new)
# -------------------------------------------------------------------
async def update_shop_status(db: Session, client: httpx.AsyncClient):
    """
    Atualiza os status (is_new, is_on_sale, price) dos cosméticos
    que já estão no nosso banco.
    """
    print("Iniciando atualização de status da loja...")
    
    try:
        # --- ETAPA A: Limpa todos os status ---
        print("Resetando status de todos os itens...")
        db.query(Cosmetic).update({
            "is_new": False,
            "is_on_sale": False,
            "is_on_promotion": False,
            "price": 0
        })
        db.commit()

        # --- ETAPA B: Busca a Loja Atual (/shop) ---
        print("Buscando /shop...")
        shop_response = await client.get(f"{FORTNITE_API_BASE_URL}/shop")
        shop_response.raise_for_status()
        
        shop_entries = shop_response.json().get("data", {}).get("entries", [])
        print(f"Encontrados {len(shop_entries)} itens na loja.")

        items_on_sale_ids = set()
        for entry in shop_entries:
            if not entry.get("brItems"):
                continue
            
            final_price = entry.get("finalPrice", 0)
            is_promo = entry.get("regularPrice", 0) > final_price

            for item in entry["brItems"]:
                item_id = item.get("id")
                if item_id:
                    items_on_sale_ids.add(item_id)
                    # Atualiza o item no banco
                    db.query(Cosmetic).filter(Cosmetic.id == item_id).update({
                        "is_on_sale": True,
                        "price": final_price,
                        "is_on_promotion": is_promo,
                        "last_sync": datetime.now(timezone.utc)
                    })
        
        # --- ETAPA C: Busca Itens Novos (/cosmetics/new) ---
        print("Buscando /cosmetics/new...")
        new_response = await client.get(f"{FORTNITE_API_BASE_URL}/cosmetics/new")
        new_response.raise_for_status()
        
        new_items = new_response.json().get("data", {}).get("items", [])
        print(f"Encontrados {len(new_items)} itens novos.")

        for item_id in new_items:
            
            if isinstance(item_id, str):
                # Atualiza o item no banco
                db.query(Cosmetic).filter(Cosmetic.id == item_id).update({
                    "is_new": True,
                    "last_sync": datetime.now(timezone.utc)
                })
            elif isinstance(item_id, dict) and item_id.get("id"):
                db.query(Cosmetic).filter(Cosmetic.id == item_id.get("id")).update({
                    "is_new": True,
                    "last_sync": datetime.now(timezone.utc)
                })
        
        db.commit() 
        print("Atualização de status da loja concluída.")
        
    except httpx.HTTPStatusError as e:
        print(f"Erro HTTP ao atualizar status da loja: {e}")
    except Exception as e:
        print(f"Erro inesperado no update_shop_status: {e}")
        db.rollback()

# -------------------------------------------------------------------
# FUNÇÃO PRINCIPAL (Runner)
# -------------------------------------------------------------------
async def main_sync():
    """
    Função principal que orquestra a sincronização.
    """
    print("="*30)
    print(f"Iniciando Sincronização - {datetime.now()}")
    print("="*30)
    
    # Precisamos criar as tabelas se elas não existirem
    # (Exatamente como no main.py)
    Base.metadata.create_all(bind=engine)
    
    # Cria uma sessão de banco de dados
    db = SessionLocal()
    
    # Cria um cliente HTTP assíncrono
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # 1. Sincroniza o catálogo mestre 
            #await sync_all_cosmetics(db, client)
            
            # 2. Atualiza os status
            await update_shop_status(db, client)
            
        finally:
            db.close()
            
    print("="*30)
    print("Sincronização Finalizada.")
    print("="*30)

# --- Ponto de entrada para rodar o script ---
if __name__ == "__main__":
    # Esta parte permite rodar o script diretamente
    # Ex: python -m app.tasks.sync_data
    print("Rodando script como módulo...")
    asyncio.run(main_sync())