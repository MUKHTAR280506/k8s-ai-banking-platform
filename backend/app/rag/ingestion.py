from langchain_community.embeddings import OpenAIEmbeddings
from qdrant_client.models import PointStruct, VectorParams, Distance

import uuid

from app.core.database import qdrant

embeddings = OpenAIEmbeddings()
def embed (text: str)->list[float]:
    
    vector = embeddings.embed_query(text)
    return vector


COLLECTION_NAME = "rules"

def ingest(text: str):
    sanctions = [
        line.strip().lower()
        for line in text.splitlines()
        if line.strip()
    ]

    if not qdrant.collection_exists(COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )

    points = []
    for sanction in sanctions:
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embed(sanction),
                payload={"text": sanction}
            )
        )

    qdrant.upsert(COLLECTION_NAME, points)
