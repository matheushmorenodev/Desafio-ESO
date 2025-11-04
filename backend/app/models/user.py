from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.sql import func
from ..core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    vbucks = Column(Integer, nullable=False, default=10000) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())