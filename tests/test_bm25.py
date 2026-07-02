import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.retrieval.bm25_retriever import BM25Retriever

bm25 = BM25Retriever()

results = bm25.search(

    "Python embeddings retrieval",

    top_k=10,

)

for r in results:

    print(r)