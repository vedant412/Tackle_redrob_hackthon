from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.llm.provider_manager import ProviderManager
from app.services.llm_job_parser import LLMJobParser
from app.services.hyre_generator import HYREGenerator
from app.retrieval.query_generator import QueryGenerator
from app.retrieval.hybrid_retriever import HybridRetriever
from app.services.candidate_repository import CandidateRepository
from app.services.candidate_enricher import CandidateEnricher
from app.filtering.hard_constraint_filter import HardConstraintFilter
from app.ranking.feature_engineer import FeatureEngineer


# ----------------------------------------------------
# Load Candidates
# ----------------------------------------------------

repo = CandidateRepository()

repo.load(
    BASE_DIR / "data" / "candidates.jsonl"
)

print(f"\nLoaded {repo.count()} candidates")

# ----------------------------------------------------
# Services
# ----------------------------------------------------

provider = ProviderManager()

parser = LLMJobParser(provider)

hyre_generator = HYREGenerator(provider)

query_generator = QueryGenerator()

retriever = HybridRetriever()

enricher = CandidateEnricher(repo)

hard_filter = HardConstraintFilter()

feature_engineer = FeatureEngineer()

# ----------------------------------------------------
# Job Description
# ----------------------------------------------------

jd = """
We are hiring a Senior AI Engineer.

Requirements:

- 5+ years experience
- Python
- Embeddings
- Retrieval Systems
- Ranking
- FAISS
- Vector Databases
- Hybrid Search
- Machine Learning
- LLMs
- Pune or Hybrid preferred
"""

# ----------------------------------------------------
# Pipeline
# ----------------------------------------------------

parsed = parser.parse(jd)

hyre = hyre_generator.generate(parsed)

print("\n================ PARSED JOB ================\n")
print(parsed.model_dump())

print("\n================ HYRE PROFILE ================\n")
print(hyre.model_dump())

positive = query_generator.generate_positive(hyre)

negative = query_generator.generate_negative(hyre)

queries = positive + negative

results = retriever.search(
    queries,
    top_k=300,
)

print("\nRetrieved:", len(results))

results = enricher.enrich(results)

filtered = hard_filter.filter(
    results,
    parsed,
)

print("Filtered :", len(filtered))

print()

print("=" * 80)
print("FEATURE VECTORS")
print("=" * 80)

for result in filtered[:10]:

    fv = feature_engineer.build(
        result,
        parsed,
    )

    print()

    print(fv)