# from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from app.core.database import qdrant

def fetch_rules(query: str): 
    return ["No special rules found."]
