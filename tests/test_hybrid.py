import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.llm.provider_manager import ProviderManager
from app.services.llm_job_parser import LLMJobParser
from app.services.hyre_generator import HYREGenerator

from app.retrieval.query_generator import QueryGenerator
from app.retrieval.hybrid_retriever import HybridRetriever

provider = ProviderManager()

parser = LLMJobParser(provider)

hyre_generator = HYREGenerator(provider)

query_generator = QueryGenerator()

retriever = HybridRetriever()

jd = """
We are hiring a Senior AI Engineer with strong Python,
Embeddings, Retrieval, FAISS,
Vector Databases,
LLMs,
Ranking Systems,
Machine Learning,
Hybrid Search,
Evaluation Metrics,
NDCG,
MRR.
"""

parsed = parser.parse(jd)

hyre = hyre_generator.generate(parsed)

queries = query_generator.generate_positive(hyre)

results = retriever.search(
    queries,
    top_k=200,
)

print()

print("=" * 60)

print("TOP RESULTS")

print("=" * 60)

for r in results[:20]:

    print(r)