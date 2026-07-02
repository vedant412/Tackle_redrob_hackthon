import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.embedding_service import EmbeddingService
from app.retrieval.dense_retriever import DenseRetriever

embedding_service = EmbeddingService()

retriever = DenseRetriever()

query = "Python Embeddings Retrieval"

embedding = embedding_service.encode(query)

results = retriever.search(
    embedding,
    query,
    weight=1.0,
    top_k=10,
)

for result in results:
    print(result)