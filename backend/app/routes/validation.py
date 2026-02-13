from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal,qdrant
from app.core.security import authenticate
from app.models.beneficiary_table import Beneficiary
from langchain_community.embeddings import OpenAIEmbeddings
from app.models.account import Account
from app.models.limits_table import TransferLimit
from uuid import uuid4
from app.models.transaction import Transaction


router = APIRouter(prefix ="/api/transfer")
embeddings = OpenAIEmbeddings()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def embed (text: str)->list[float]:
    
    vector = embeddings.embed_query(text)
    return vector

def check_sanctions(beneficiary: dict):
    tokens = {
        beneficiary["country"].lower().strip(),
        beneficiary["bank_name"].lower().strip(),
        beneficiary["name"].lower().strip()
    }

    results = qdrant.scroll(
        collection_name="rules",
        limit=1000
    )[0]

    sanctioned_values = {
        p.payload["text"].lower().strip()
        for p in results
    }

    # EXACT MATCH
    for token in tokens:
        if token in sanctioned_values:
            return False  

    return True  

def get_transfer_limit(db: Session) -> dict:
    limit = (
        db.query(TransferLimit)
        .order_by(TransferLimit.updated_at.desc())
        .first()
    )

    if not limit:
        return {
            "daily_limit": 0,
            "per_transaction_limit": 0
        }

    return {
        "daily_limit": limit.daily_limit,
        "per_transaction_limit": limit.per_transaction_limit
    }

def fetch_balance(user_id: str, db: Session) -> float:
    account = db.query(Account).filter(Account.user_id == user_id).first()

    if not account:
        raise ValueError("Account not found")

    return account.balance


@router.get("/balance")
def get_balance(user_id: str, db: Session = Depends(get_db)):
    balance = fetch_balance(user_id, db)
    return {"balance": balance}

    

@router.post("/validate")
def validate_transfer(payload: dict, db: Session = Depends(get_db)):
    print(1)
    beneficiary = payload["beneficiary"]
    amount = payload["amount"]
    user_id = payload["user_id"]

    print(2)
    if not check_sanctions(beneficiary):
        return {"allowed": False, "reason": "Sanctions restriction"}

    print(3)
    balance = fetch_balance(user_id, db)
    if amount > balance:
        return {"allowed": False, "reason": "Insufficient balance"}

    print(4)
   
    limits = get_transfer_limit(db)

    if amount > limits["per_transaction_limit"]:
       return {"allowed": False, "reason": "Per transaction limit exceeded"}

    if amount > limits["daily_limit"]:
       return {"allowed": False, "reason": "Daily limit exceeded"}
    return {"allowed": True, "payload":payload}

@router.get("/history")
def txn_history(
    user_id: str,
    number: int = 10,
    db: Session = Depends(get_db)
):
    """
    Fetch last N transactions for a user
    """

    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.created_at.desc())
        .limit(number)
        .all()
    )

    if not transactions:
        return {"transactions": []}

    return {
        "transactions": [
            {
                "txn_id": txn.id,
                "date": txn.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "type": txn.txn_type,
                "amount": txn.amount,
                "beneficiary": txn.beneficiary_name,
                "status": txn.status
            }
            for txn in transactions
        ]
    }
    


@router.post("/execute")
def execute_transfer(payload: dict, db: Session = Depends(get_db)):
    user_id = payload["user_id"]
    amount = payload["amount"]
    beneficiary = payload["beneficiary"]

    try:
        #  Lock account row (prevents race conditions)
        account = (
            db.query(Account)
            .filter(Account.user_id == user_id)
            .with_for_update()
            .first()
        )

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        if account.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        # Debit balance
        account.balance -= amount

        #  Create transaction record
        txn = Transaction(
            user_id=user_id,
            amount=amount,
            txn_type="DEBIT",
            beneficiary_name=beneficiary["name"],
            status="SUCCESS"
        )

        db.add(txn)
        db.commit()
        db.refresh(txn)

        return {
            "status": "SUCCESS",
            "transaction_id": txn.id,
            "message": (
                f"₹{amount} debited from your account. "
                f"Beneficiary {beneficiary['name']} credited successfully."
            ),
            "remaining_balance": account.balance
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



