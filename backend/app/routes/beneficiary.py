# backend/app/routes/beneficiary.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import authenticate
from app.models.beneficiary_table import Beneficiary

router = APIRouter(prefix="/api/beneficiary")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add")
def add_beneficiary(data: dict, user=Depends(authenticate), db: Session = Depends(get_db)):
    
    beneficiary = Beneficiary(
        user_id=user,
        name=data["name"],
        iban=data["iban"],
        bank_name=data["bank_name"],
        country=data["country"]
    )
    
    db.add(beneficiary)
    db.commit()
    return {"message": "Beneficiary added successfully"}


@router.get("/list")
def list_beneficiaries(user=Depends(authenticate), db: Session = Depends(get_db)):
    return db.query(Beneficiary).filter(Beneficiary.user_id == "customer").all()  # making default to customer user id
