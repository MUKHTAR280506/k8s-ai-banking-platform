from sqlalchemy import  Column, Integer, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class TransferLimit(Base):
    __tablename__ = "transfer_limits"

    id = Column(Integer, primary_key=True)
    daily_limit = Column(Integer, nullable=False)
    per_transaction_limit = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    
