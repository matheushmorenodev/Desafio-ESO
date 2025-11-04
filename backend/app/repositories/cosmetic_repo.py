from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from ..models.cosmetic import Cosmetic
from ..models.inventory import Inventory
from ..models.transaction import TransactionHistory, TransactionType
from ..models.user import User
from typing import Optional, List, Tuple
from datetime import datetime
from sqlalchemy.orm import joinedload


# definindo os filtros
class CosmeticFilterParams:
    def __init__(
        self,
        name: Optional[str] = None,
        type: Optional[str] = None,
        rarity: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        is_new: Optional[bool] = None,
        is_on_sale: Optional[bool] = None,
        is_on_promotion: Optional[bool] = None,
    ):
        self.name = name
        self.type = type
        self.rarity = rarity
        self.date_from = date_from
        self.date_to = date_to
        self.is_new = is_new
        self.is_on_sale = is_on_sale
        self.is_on_promotion = is_on_promotion

#pegando cosmeticos por filtro
def get_cosmetics_with_filters(
    db: Session,
    filters: CosmeticFilterParams,
    page: int = 1,
    limit: int = 20
) -> Tuple[List[Cosmetic], int]:
    """
    Busca cosméticos no banco com filtros dinâmicos e paginação.
    Retorna uma tupla: (lista_de_itens, total_de_itens)
    """
    query = db.query(Cosmetic)

    # --- Aplicação dos Filtros ---
    if filters.name:
        # 'ilike' é case-insensitive
        query = query.filter(Cosmetic.name.ilike(f"%{filters.name}%"))
    
    if filters.type:
        query = query.filter(Cosmetic.type == filters.type)
        
    if filters.rarity:
        query = query.filter(Cosmetic.rarity == filters.rarity)
        
    if filters.date_from:
        query = query.filter(Cosmetic.added_at >= filters.date_from)
        
    if filters.date_to:
        query = query.filter(Cosmetic.added_at <= filters.date_to)
        
    if filters.is_new is not None:
        query = query.filter(Cosmetic.is_new == filters.is_new)
        
    if filters.is_on_sale is not None:
        query = query.filter(Cosmetic.is_on_sale == filters.is_on_sale)
        
    if filters.is_on_promotion is not None:
        query = query.filter(Cosmetic.is_on_promotion == filters.is_on_promotion)

    # --- Contagem Total (antes da paginação) ---
    # Faz uma subquery para otimizar a contagem com os filtros
    count_query = query.statement.with_only_columns(func.count()).order_by(None)
    total_items = db.execute(count_query).scalar()

    # --- Paginação ---
    offset = (page - 1) * limit
    query = query.order_by(desc(Cosmetic.added_at)).offset(offset).limit(limit)
    
    items = query.all()
    
    return (items, total_items)

#buscando cosmetico por ID
def get_cosmetic_by_id(db: Session, cosmetic_id: str) -> Optional[Cosmetic]:
    return db.query(Cosmetic).filter(Cosmetic.id == cosmetic_id).first()

#verificando se usuario ja possui o item
def get_inventory_item(db: Session, user_id: int, cosmetic_id: str) -> Optional[Inventory]:
    return db.query(Inventory).filter(
        Inventory.user_id == user_id,
        Inventory.cosmetic_id == cosmetic_id
    ).first()


#relaciona a ultima transacao de compra de um item para saber o preço pago
def get_last_purchase_transaction(db: Session, user_id: int, cosmetic_id: str) -> Optional[TransactionHistory]:
    return db.query(TransactionHistory).filter(
        TransactionHistory.user_id == user_id,
        TransactionHistory.cosmetic_id == cosmetic_id,
        TransactionHistory.type == TransactionType.PURCHASE
    ).order_by(desc(TransactionHistory.created_at)).first()

#adicionando um item ao inventario do usuario
def add_item_to_inventory(db: Session, user: User, cosmetic: Cosmetic) -> Inventory:
    db_inventory_item = Inventory(user_id=user.id, cosmetic_id=cosmetic.id)
    db.add(db_inventory_item)
    return db_inventory_item

#remove item do inventario do usuario
def remove_item_from_inventory(db: Session, inventory_item: Inventory):
    db.delete(inventory_item)

#registrando nova transação
def create_transaction(
    db: Session, 
    user: User,  
    type: TransactionType, 
    value: int,
    cosmetic: Optional[Cosmetic] = None, 
    offer_id: Optional[str] = None
) -> TransactionHistory:
    db_transaction = TransactionHistory(
        user_id=user.id,
        cosmetic_id=cosmetic.id if cosmetic else None,
        offer_id=offer_id,
        type=type,
        value=value # ex: -1200 (compra) ou +1200 (devolução)
    )
    db.add(db_transaction)
    return db_transaction
    
#buscando todos os cosmeticos que um usuario possui
def get_user_inventory(db: Session, user_id: int) -> list[Cosmetic]:
    # Faz um JOIN entre o Inventário e os Cosméticos
    items = db.query(Cosmetic).join(Inventory).filter(
        Inventory.user_id == user_id
    ).all()
    return items

#buscando historico de transacoes
def get_user_transaction_history(db: Session, user_id: int) -> list[TransactionHistory]:
    history = (
        db.query(TransactionHistory)
        .options(joinedload(TransactionHistory.cosmetic)) # <-- A MÁGICA!
        .filter(TransactionHistory.user_id == user_id)
        .order_by(desc(TransactionHistory.created_at))
        .all()
    )
    return history

