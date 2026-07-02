from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService

query = """
Senior AI Engineer

Strong Python

Vector Databases

FAISS

Embeddings

Retrieval Systems

Ranking Models

Machine Learning
"""

embedder = EmbeddingService()

retriever = RetrievalService()

query_embedding = embedder.encode(query)

results = retriever.search(
    query_embedding,
    top_k=10,
)

print()

print("=" * 60)

print("Top Results")

print("=" * 60)

for result in results:

    print(result)