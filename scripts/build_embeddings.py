import sys
import pickle
from pathlib import Path

import numpy as np
from tqdm import tqdm

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from app.builders.candidate_document_builder import CandidateDocumentBuilder
from app.config import (
    CANDIDATE_DOCUMENTS_PATH,
    CANDIDATE_IDS_PATH,
    EMBEDDINGS_PATH,
)
from app.services.candidate_repository import CandidateRepository
from app.services.embedding_service import EmbeddingService


DATA_PATH = BASE_DIR / "data" / "candidates.jsonl"


print("=" * 60)
print("Loading Candidates...")
print("=" * 60)

repo = CandidateRepository()
repo.load(DATA_PATH)

print("=" * 60)
print("Loading Embedding Model...")
print("=" * 60)

embedder = EmbeddingService()

documents = []
candidate_ids = []

print("=" * 60)
print("Building Candidate Documents...")
print("=" * 60)

for candidate in tqdm(repo.get_all()):

    document = CandidateDocumentBuilder.build(candidate)

    documents.append(document)

    candidate_ids.append(candidate.candidate_id)

print("=" * 60)
print("Generating Embeddings...")
print("=" * 60)

embeddings = embedder.encode_batch(
    documents,
    batch_size=32,
)

print("=" * 60)
print("Saving Cache...")
print("=" * 60)

# Save embeddings
np.save(
    EMBEDDINGS_PATH,
    embeddings,
)

# Save candidate IDs
np.save(
    CANDIDATE_IDS_PATH,
    np.array(candidate_ids),
)

# Save candidate documents
with open(CANDIDATE_DOCUMENTS_PATH, "wb") as f:
    pickle.dump(documents, f)

print()
print("Done!")
print()
print("Embeddings :", EMBEDDINGS_PATH)
print("Candidate IDs :", CANDIDATE_IDS_PATH)
print("Documents :", CANDIDATE_DOCUMENTS_PATH)
print()
print("Embedding Shape:", embeddings.shape)
print("Total Candidates:", len(candidate_ids))