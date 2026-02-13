from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pymongo import MongoClient
from qdrant_client import QdrantClient
from app.core.config import POSTGRES_URL, MONGO_URL, QDRANT_HOST, QDRANT_PORT

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["crm"]

# qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
qdrant = QdrantClient(
    url="http://qdrant:6333",   
    prefer_grpc=False              
)
