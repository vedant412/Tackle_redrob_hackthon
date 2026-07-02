import sys
from pathlib import Path

import faiss
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.config import (
    EMBEDDINGS_PATH,
    CANDIDATE_IDS_PATH,
    FAISS_INDEX_PATH,
)


print("=" * 60)
print("Loading Embeddings...")
print("=" * 60)

embeddings = np.load(EMBEDDINGS_PATH)
candidate_ids = np.load(CANDIDATE_IDS_PATH)

print(f"Embeddings Shape : {embeddings.shape}")
print(f"Candidates       : {len(candidate_ids)}")

# -----------------------------------------------------
# Ensure float32
# -----------------------------------------------------

embeddings = embeddings.astype(np.float32)

dimension = embeddings.shape[1]

print(f"\nEmbedding Dimension : {dimension}")

# -----------------------------------------------------
# Cosine Similarity
# -----------------------------------------------------

base_index = faiss.IndexFlatIP(dimension)

index = faiss.IndexIDMap2(base_index)

numeric_ids = np.arange(len(candidate_ids), dtype=np.int64)

print("\nAdding vectors to FAISS...")

index.add_with_ids(
    embeddings,
    numeric_ids,
)

print("Done.")

print("\nSaving FAISS Index...")

faiss.write_index(
    index,
    str(FAISS_INDEX_PATH),
)

print(f"\nSaved to:\n{FAISS_INDEX_PATH}")