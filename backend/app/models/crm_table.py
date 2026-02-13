from sqlalchemy import Column,Integer, String, Float, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime
from app.core.database import Base

class CRMComplaint(Base):
    __tablename__ = "crm_complaints"

    complaint_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String)
    account_id = Column(Integer)
    complaint_text = Column(Text)
    complaint_category = Column(String)
    severity = Column(String)
    sentiment_score = Column(Float)
    status = Column(String, default="OPEN")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
