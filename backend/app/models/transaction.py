from sqlalchemy import Column, Integer, Float, String, DateTime
from app.core.database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    amount = Column(Float)
    txn_type = Column(String)
    beneficiary_name = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
