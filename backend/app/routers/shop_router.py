from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import httpx 
from typing import List, Optional

from ..core.database import get_db
from ..core.security import get_current_active_user, get_optional_current_user
from ..models.user import User
from ..models.inventory import Inventory
from ..models.transaction import TransactionType
from ..repositories import cosmetic_repo
from ..schemas.shop_schema import OfferBuyRequest
from ..schemas.user_schema import UserPublic

router = APIRouter(
    prefix="/shop",
    tags=["Loja (Bundles e Ofertas)"]
)

# URL da API do Fortnite
FORTNITE_API_URL = "https://fortnite-api.com/v2/shop"

async def fetch_live_shop_data() -> List[dict]:
    """Função para buscar dados ao vivo da loja."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(FORTNITE_API_URL)
            response.raise_for_status()
            return response.json().get("data", {}).get("entries", [])
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=503, detail="Não foi possível buscar os dados da loja Fortnite.")

@router.get("/", response_model=dict)
async def get_live_shop(
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Busca os dados da loja ao vivo da API do Fortnite e 
    com os dados de 'is_acquired' do usuário logado.
    """
    shop_entries = await fetch_live_shop_data()
    
    acquired_ids = set()
    if current_user:
        # Busca o inventário do usuário
        user_inventory = db.query(Inventory.cosmetic_id).filter(
            Inventory.user_id == current_user.id
        ).all()
        acquired_ids = {item_id for (item_id,) in user_inventory}
        
    # 'Enriquece' os dados
    for entry in shop_entries:
        if entry.get("brItems"):
            for item in entry["brItems"]:
                if item.get("id") in acquired_ids:
                    item["is_acquired"] = True
                else:
                    item["is_acquired"] = False
                    
    return {"entries": shop_entries}


@router.post("/buy", response_model=UserPublic)
async def buy_offer_or_bundle(
    request_data: OfferBuyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user) # Obrigatório
):
    """
     Compra uma oferta da loja (item ou bundle)
    usando o 'offerId'.
    """
    shop_entries = await fetch_live_shop_data()
    
    # 1. Encontra a oferta que o usuário quer comprar
    target_offer = None
    for entry in shop_entries:
        if entry.get("offerId") == request_data.offer_id:
            target_offer = entry
            break
            
    if not target_offer:
        raise HTTPException(status_code=404, detail="Oferta não encontrada na loja atual.")
        
    price = target_offer.get("finalPrice", 0)
    
    
    if price <= 0:
        raise HTTPException(status_code=400, detail="Este item não pode ser comprado (preço inválido).")
    
    if current_user.vbucks < price:
        raise HTTPException(status_code=400, detail="V-Bucks insuficientes.")
        
    items_in_bundle = target_offer.get("brItems", [])
    if not items_in_bundle:
        raise HTTPException(status_code=400, detail="Oferta não contém itens.")

    try:
        # 3. Debita os V-Bucks (uma vez pelo bundle)
        current_user.vbucks -= price
        db.add(current_user)
        
        items_added_count = 0
        
        # adicionando todos os itens do bundle
        for item in items_in_bundle:
            cosmetic_id = item.get("id")
            if not cosmetic_id:
                continue
            
            # Verificando se o cosmético existe no nosso banco
            cosmetic = cosmetic_repo.get_cosmetic_by_id(db, cosmetic_id)
            if not cosmetic:
                print(f"Aviso: Item de bundle {cosmetic_id} não encontrado no banco local. Pulando.")
                continue

            #verificando se o usuário já possui este item específico
            existing_item = cosmetic_repo.get_inventory_item(db, current_user.id, cosmetic_id)
            if not existing_item:
                #adicionando ao inventário
                cosmetic_repo.add_item_to_inventory(db, current_user, cosmetic)
                items_added_count += 1
        
        #registro de transação do bundle
        cosmetic_repo.create_transaction(
            db,
            user=current_user,
            type=TransactionType.PURCHASE,
            value= -price,
            offer_id=request_data.offer_id 
        )
        
        #usuário já tinha tudo do bundle
        if items_added_count == 0:
            db.rollback() # Desfaz o débito de V-Bucks
            raise HTTPException(
                status_code=400, 
                detail="Você já possui todos os itens deste pacote."
            )
            
        db.commit()
        db.refresh(current_user)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Ocorreu um erro ao processar a compra: {str(e)}"
        )
        
    return current_user