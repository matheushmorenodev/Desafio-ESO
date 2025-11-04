from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..core.database import Base
from sqlalchemy.orm import relationship
#criando a tabela de inventario
class Inventory(Base):
    __tablename__ = "inventory"

    # Chave primária composta
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    cosmetic_id = Column(String(255), ForeignKey("cosmetics.id"), primary_key=True)
    
    acquired_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos (opcional, mas bom para o ORM)
    user = relationship("User")
    cosmetic = relationship("Cosmetic")
