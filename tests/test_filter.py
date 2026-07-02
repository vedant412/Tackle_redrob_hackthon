import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.llm.provider_manager import ProviderManager
from app.services.llm_job_parser import LLMJobParser
from app.services.hyre_generator import HYREGenerator

from app.retrieval.query_generator import QueryGenerator
from app.retrieval.hybrid_retriever import HybridRetriever

from backend.app.services.candidate_enricher import CandidateEnricher
from app.filtering.hard_constraint_filter import HardConstraintFilter

from app.services.candidate_repository import CandidateRepository


# --------------------------------------------------------
# Load Repository
# --------------------------------------------------------

repo = CandidateRepository()

repo.load(
    BASE_DIR / "data" / "candidates.jsonl"
)

# --------------------------------------------------------
# Pipeline
# --------------------------------------------------------

provider = ProviderManager()

parser = LLMJobParser(provider)

hyre_generator = HYREGenerator(provider)

query_generator = QueryGenerator()

retriever = HybridRetriever()

enricher = CandidateEnricher()

hard_filter = HardConstraintFilter()

# --------------------------------------------------------
# Job Description
# --------------------------------------------------------

jd = """
Senior AI Engineer

Python

Embeddings

Retrieval

Ranking

FAISS

Vector Database

Machine Learning

LLMs

5+ years experience

Hybrid

Pune
"""

# --------------------------------------------------------
# Execute
# --------------------------------------------------------

parsed = parser.parse(jd)

hyre = hyre_generator.generate(parsed)

queries = query_generator.generate_positive(hyre)

retrieved = retriever.search(
    queries,
    top_k=300,
)

print(f"\nRetrieved : {len(retrieved)}")

retrieved = enricher.enrich(retrieved)

filtered = hard_filter.filter(
    retrieved,
    parsed,
)

print(f"Filtered  : {len(filtered)}")

print()

print("=" * 80)

print("TOP FILTERED CANDIDATES")

print("=" * 80)

for candidate in filtered[:10]:

    print()

    print(candidate.candidate.profile.anonymized_name)

    print(candidate.candidate.profile.current_title)

    print(candidate.score)

    print(candidate.metadata)