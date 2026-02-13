from app.core.database import engine, Base
from app.models import beneficiary_table  # force model import
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.crm_table import CRMComplaint
from app.models.limits_table import TransferLimit

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

