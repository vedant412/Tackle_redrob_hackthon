import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.llm.provider_manager import ProviderManager
from app.pipeline.ranking_pipeline import RankingPipeline

provider = ProviderManager()

pipeline = RankingPipeline(provider)

pipeline.load_candidates(

    BASE_DIR / "data" / "candidates.jsonl"

)

job_description = """

Looking for a Senior Machine Learning Engineer.

Must have:

Python

FAISS

Embeddings

Vector Databases

Machine Learning

5+ years experience.

Hybrid.

"""

pipeline.run(

    job_description,

    output_csv="outputs/final_submission.csv",

    top_k=100,

)