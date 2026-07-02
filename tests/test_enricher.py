import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.services.candidate_enricher import CandidateEnricher
from app.retrieval.hybrid_retriever import HybridRetriever
from app.retrieval.query_generator import QueryGenerator
from app.services.candidate_repository import CandidateRepository
from app.services.hyre_generator import HYREGenerator
from app.services.llm_job_parser import LLMJobParser
from app.llm.provider_manager import ProviderManager


repo = CandidateRepository()

repo.load(
    BASE_DIR / "data" / "candidates.jsonl"
)

provider = ProviderManager()

parser = LLMJobParser(provider)

hyre_generator = HYREGenerator(provider)

generator = QueryGenerator()

retriever = HybridRetriever()

enricher = CandidateEnricher()

jd = """
Senior AI Engineer

Python

Embeddings

Retrieval

FAISS

Vector Database

LLMs
"""

parsed = parser.parse(jd)

hyre = hyre_generator.generate(parsed)

queries = generator.generate_positive(hyre)

results = retriever.search(queries)

results = enricher.enrich(results)

print(results[0].candidate)