#tabela de histórico de transação
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from ..core.database import Base
from sqlalchemy.orm import relationship
import enum

#tipo de transação
class TransactionType(str, enum.Enum):
    PURCHASE = "purchase" #compra
    RETURN = "return"     #devolução

class TransactionHistory(Base):
    __tablename__ = "transaction_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cosmetic_id = Column(String(255), ForeignKey("cosmetics.id"), nullable=True)

    offer_id = Column(String(255), nullable=True, index=True)
    
    type = Column(Enum(TransactionType), nullable=False)
    value = Column(Integer, nullable=False) # ex: -1200 (compra), +1200 (devolução)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    user = relationship("User")
    cosmetic = relationship("Cosmetic")