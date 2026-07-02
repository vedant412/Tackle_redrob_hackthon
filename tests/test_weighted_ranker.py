import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.llm.provider_manager import ProviderManager
from app.services.llm_job_parser import LLMJobParser
from app.services.hyre_generator import HYREGenerator
from app.services.query_generator import QueryGenerator
from app.retrieval.hybrid_retriever import HybridRetriever
from app.services.candidate_repository import CandidateRepository
from app.services.candidate_enricher import CandidateEnricher
from app.filtering.hard_constraint_filter import HardConstraintFilter
from app.ranking.feature_engineer import FeatureEngineer
from app.ranking.weighted_ranker import WeightedRanker

# -------------------------------------------------
# Load Repository
# -------------------------------------------------

repo = CandidateRepository()

repo.load(BASE_DIR / "data" / "candidates.jsonl")

# -------------------------------------------------
# Initialize Components
# -------------------------------------------------

provider = ProviderManager()

parser = LLMJobParser(provider)

hyre_generator = HYREGenerator(provider)

query_generator = QueryGenerator()

retriever = HybridRetriever()

enricher = CandidateEnricher(repo)

hard_filter = HardConstraintFilter()

feature_engineer = FeatureEngineer()

ranker = WeightedRanker()

# -------------------------------------------------
# Test JD
# -------------------------------------------------

jd = """
Looking for a Senior Machine Learning Engineer.

Must have:

Python
FAISS
Embeddings
Retrieval
Machine Learning

5+ years experience.

Hybrid.

"""

# -------------------------------------------------
# Pipeline
# -------------------------------------------------

parsed = parser.parse(jd)

hyre = hyre_generator.generate(parsed)

queries = query_generator.generate(
    parsed,
    hyre,
)

results = retriever.search(
    queries,
)

results = enricher.enrich(
    results,
)

results = hard_filter.filter(
    results,
    parsed,
)

features = feature_engineer.build(
    results,
    parsed,
)

ranked = ranker.rank(
    features,
    top_k=10,
)

# -------------------------------------------------
# Output
# -------------------------------------------------

print()
print("=" * 80)
print("TOP RANKED CANDIDATES")
print("=" * 80)
print()

for i, candidate in enumerate(ranked, start=1):

    print(f"{i}. {candidate.candidate_id}")

    print(f"Score : {candidate.final_score:.4f}")

    print(candidate.metadata)

    print()