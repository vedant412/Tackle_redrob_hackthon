from app.config import FAISS_INDEX_PATH, CANDIDATE_IDS_PATH

import faiss
import numpy as np

from app.retrieval.retrieval_result import RetrievalResult


class DenseRetriever:

    _index = None
    _candidate_ids = None

    def __init__(self):

        if DenseRetriever._index is None:

            print("Loading FAISS index...")

            DenseRetriever._index = faiss.read_index(
                str(FAISS_INDEX_PATH)
            )

            print("Loading Candidate IDs...")

            DenseRetriever._candidate_ids = np.load(
                CANDIDATE_IDS_PATH,
                allow_pickle=True,
            )

            print(
                f"Loaded {len(DenseRetriever._candidate_ids)} candidates."
            )

        self.index = DenseRetriever._index
        self.candidate_ids = DenseRetriever._candidate_ids

    def search(
        self,
        embedding,
        query_text,
        weight=1.0,
        top_k=300,
    ):

        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)

        embedding = embedding.astype(np.float32)

        scores, indices = self.index.search(
            embedding,
            top_k,
        )

        results = []

        for rank, (score, idx) in enumerate(
            zip(scores[0], indices[0]),
            start=1,
        ):

            if idx == -1:
                continue

            candidate_id = str(self.candidate_ids[idx])

            results.append(

                RetrievalResult(

                    candidate_id=candidate_id,

                    dense_score=float(score),

                    dense_rank=rank,

                    final_score=float(score) * weight,

                    retriever="faiss",

                    matched_queries=[query_text],

                )

            )

        return results