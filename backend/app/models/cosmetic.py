from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.sql import func
from ..core.database import Base

#criando a tabela de cosmeticos
class Cosmetic(Base):
    __tablename__ = "cosmetics"

    # Usamos o ID da API como nossa Chave Primária
    id = Column(String(255), primary_key=True, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(100), index=True) 
    rarity = Column(String(100), index=True) 
    
    # Preço atual (/shop)
    price = Column(Integer, default=0) 
    
    image_url = Column(String(1024), nullable=True)
    
    # Data de inclusão (/cosmetics)
    added_at = Column(DateTime(timezone=True), index=True) 

    # Status 
    is_new = Column(Boolean, default=False, index=True)
    is_on_sale = Column(Boolean, default=False, index=True)
    is_on_promotion = Column(Boolean, default=False, index=True)
    
    # Controle interno
    last_sync = Column(DateTime(timezone=True), server_default=func.now())