from fastapi import APIRouter, UploadFile
from sqlalchemy.orm import Session
from app.rag.ingestion import ingest
from app.core.database import SessionLocal
from app.models.limits_table import TransferLimit
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.beneficiary_table import Beneficiary
from pydantic import BaseModel

router = APIRouter(prefix="/api/admin", tags=["Admin"])

# ---------- REQUEST SCHEMA ----------
class WalletRequest(BaseModel):
    customer_id: str
    amount: float
    type: str  # "credit" or "debit"


# ---------- FILE UPLOAD ----------
@router.post("/upload")
async def upload(file: UploadFile):
    text = (await file.read()).decode("utf-8")
    ingest(text)
    return {"status": "uploaded to vector db"}


# ---------- LIMIT CONFIG ----------
class LimitRequest(BaseModel):
    daily_limit: int
    per_transaction_limit: int


@router.post("/limits")
def set_limits(payload: LimitRequest):
    db: Session = SessionLocal()

    # Keep only ONE active row
    db.query(TransferLimit).delete()

    limits = TransferLimit(
        daily_limit=payload.daily_limit,
        per_transaction_limit=payload.per_transaction_limit
    )

    db.add(limits)
    db.commit()
    db.close()

    return {"status": "limits updated"}
@router.get("/customers")
def list_customers():
    db: Session = SessionLocal()
    try:
        customers = db.query(Account).all()
        print(customers)
        for c in customers:
            print(c.user_id)
            print(c.balance)
        return [
            {
                "user_id": c.user_id,
                "balance": c.balance
            }
            for c in customers
        ]

    finally:
        db.close()

@router.get("/customer")
def get_customer_details():
    db: Session = SessionLocal()
    try:
        customers = db.query(Account).all()
        print(customers)
        for c in customers:
            print(c.user_id)
            print(c.balance)
        return [
            {
                "user_id": c.user_id,
                "balance": c.balance
            }
            for c in customers
        ]

    finally:
        db.close()        



@router.get("/customer/{customer_id}")
def get_customer_details(customer_id: str):
    db: Session = SessionLocal()

    try:
        # Fetch account
        account = (
            db.query(Account)
            .filter(Account.user_id == customer_id)
            .first()
        )

        if not account:
            raise HTTPException(status_code=404, detail="Customer not found")

        #  Fetch beneficiaries
        beneficiaries = (
            db.query(Beneficiary)
            .filter(Beneficiary.user_id == customer_id)
            .all()
        )

        #  Build response (UI-friendly)
        return {
            "balance": account.balance,
            "beneficiaries": [
                {   "id":   b.id,
                    "name": b.name,
                    "iban": b.iban,
                    "bank": b.bank_name,
                    "country": b.country
                }
                for b in beneficiaries
            ]
        }

    finally:
        db.close()


# ---------- WALLET CREDIT / DEBIT ----------

@router.post("/wallet")
def update_wallet(payload: WalletRequest):
    db: Session = SessionLocal()

    try:
        account = (
            db.query(Account)
            .filter(Account.user_id == payload.customer_id)
            .with_for_update()   # lock row (important)
            .first()
        )

        if not account:
            raise HTTPException(status_code=404, detail="Customer not found")

        if payload.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")

        if payload.type == "credit":
            account.balance += payload.amount

        elif payload.type == "debit":
            if account.balance < payload.amount:
                raise HTTPException(
                    status_code=400,
                    detail="Insufficient balance for debit"
                )
            account.balance -= payload.amount

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid operation type. Use 'credit' or 'debit'"
            )

        db.commit()
        db.refresh(account)

        return {
            "status": "SUCCESS",
            "customer_id": payload.customer_id,
            "operation": payload.type,
            "amount": payload.amount,
            "updated_balance": account.balance
        }

    finally:
        db.close()



# ---------- DELETE BENEFICIARY ----------

@router.delete("/beneficiary/{beneficiary_id}")
def delete_beneficiary(beneficiary_id: int):
    db: Session = SessionLocal()

    try:
        beneficiary = (
            db.query(Beneficiary)
            .filter(Beneficiary.id == beneficiary_id)
            .first()
        )

        if not beneficiary:
            raise HTTPException(
                status_code=404,
                detail="Beneficiary not found"
            )

        db.delete(beneficiary)
        db.commit()

        return {
            "status": "SUCCESS",
            "message": "Beneficiary deleted successfully",
            "beneficiary_id": beneficiary_id
        }

    finally:
        db.close()

