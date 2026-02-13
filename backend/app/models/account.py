from sqlalchemy import Column, Integer, Float, String
from app.core.database import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    balance = Column(Float)
