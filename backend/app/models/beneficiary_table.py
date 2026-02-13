# backend/app/models/beneficiary_table.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    name = Column(String)
    iban = Column(String)
    bank_name = Column(String)
    country = Column(String)
