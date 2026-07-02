import pickle
from pathlib import Path

from rank_bm25 import BM25Okapi

from app.config import (
    BM25_INDEX_PATH,
    CANDIDATE_DOCUMENTS_PATH,
    CANDIDATE_IDS_PATH,
)
from app.retrieval.retrieval_result import RetrievalResult

import numpy as np


class BM25Retriever:

    _bm25 = None
    _candidate_ids = None

    def __init__(self):

        if BM25Retriever._bm25 is None:

            self._load_or_build()

        self.bm25 = BM25Retriever._bm25
        self.candidate_ids = BM25Retriever._candidate_ids

    # --------------------------------------------------

    def _tokenize(self, text: str):

        return text.lower().split()

    # --------------------------------------------------

    def _load_or_build(self):

        if BM25_INDEX_PATH.exists():

            print("Loading BM25 Index...")

            with open(BM25_INDEX_PATH, "rb") as f:

                BM25Retriever._bm25 = pickle.load(f)

            BM25Retriever._candidate_ids = np.load(
                CANDIDATE_IDS_PATH,
                allow_pickle=True,
            )

            return

        print("Building BM25 Index...")

        with open(CANDIDATE_DOCUMENTS_PATH, "rb") as f:

            documents = pickle.load(f)

        tokenized = [

            self._tokenize(doc)

            for doc in documents

        ]

        bm25 = BM25Okapi(tokenized)

        with open(BM25_INDEX_PATH, "wb") as f:

            pickle.dump(bm25, f)

        BM25Retriever._bm25 = bm25

        BM25Retriever._candidate_ids = np.load(
            CANDIDATE_IDS_PATH,
            allow_pickle=True,
        )

    # --------------------------------------------------

    def search(
    self,
    query: str,
    weight: float = 1.0,
    top_k: int = 300,
):

        tokens = self._tokenize(query)

        scores = self.bm25.get_scores(tokens)

        indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for rank, idx in enumerate(indices, start=1):

            score = float(scores[idx])

            if score <= 0:
                continue

            results.append(

                RetrievalResult(

                    candidate_id=str(self.candidate_ids[idx]),

                    bm25_score=score,

                    bm25_rank=rank,

                    final_score=score * weight,

                    retriever="bm25",

                    matched_queries=[query],

                )

            )

        return results