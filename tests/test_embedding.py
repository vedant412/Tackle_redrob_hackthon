from pathlib import Path

from app.builders.candidate_document_builder import CandidateDocumentBuilder
from app.services.candidate_repository import CandidateRepository
from app.services.embedding_service import EmbeddingService

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "candidates.jsonl"

repo = CandidateRepository()
repo.load(DATA_PATH)

candidate = repo.get_candidate("CAND_0000001")

document = CandidateDocumentBuilder.build(candidate)

embedding_service = EmbeddingService()

embedding = embedding_service.encode(document)

print("Embedding Shape:", embedding.shape)

print(embedding[:10]) 