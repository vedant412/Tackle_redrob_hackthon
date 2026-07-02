import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.embedding_service import EmbeddingService

from app.retrieval.dense_retriever import DenseRetriever
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.rrf import ReciprocalRankFusion

embedder = EmbeddingService()

dense = DenseRetriever()

bm25 = BM25Retriever()

query = "Python embeddings retrieval"

embedding = embedder.encode(query)

dense_results = dense.search(
    embedding,
    query,
    top_k=50,
)

bm25_results = bm25.search(
    query,
    top_k=50,
)

rrf = ReciprocalRankFusion()

results = rrf.fuse(
    dense_results,
    bm25_results,
)

for r in results[:20]:

    print(r)