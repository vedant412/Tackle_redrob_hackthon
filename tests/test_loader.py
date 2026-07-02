from pathlib import Path

from app.services.candidate_repository import CandidateRepository

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "candidates.jsonl"

repo = CandidateRepository()
repo.load(DATA_PATH)

print(f"Candidates Loaded: {repo.count()}")

candidate = repo.get_candidate("CAND_0000001")

print(candidate.profile.headline)

print(repo.exists("CAND_0000001"))

print(len(repo.get_candidates([
    "CAND_0000001",
    "CAND_0000002",
    "CAND_0000003"
])))