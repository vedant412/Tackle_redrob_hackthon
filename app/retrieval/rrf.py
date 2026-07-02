from app.retrieval.retrieval_result import RetrievalResult


class ReciprocalRankFusion:

    def __init__(self, k: int = 60):

        self.k = k

    def fuse(
        self,
        *rankings,
        top_k=500,
    ):

        fused = {}

        for ranking in rankings:

            for rank, result in enumerate(ranking, start=1):

                cid = result.candidate_id

                rrf_score = 1 / (self.k + rank)

                if cid not in fused:

                    fused[cid] = RetrievalResult(

                        candidate_id=cid,

                        candidate=result.candidate,

                        dense_score=result.dense_score,

                        bm25_score=result.bm25_score,

                        dense_rank=result.dense_rank,

                        bm25_rank=result.bm25_rank,

                        rrf_score=rrf_score,

                        final_score=rrf_score,

                        retriever="rrf",

                        matched_queries=result.matched_queries.copy(),

                        metadata={
                            "sources": [result.retriever]
                        }

                    )

                else:

                    current = fused[cid]

                    # -------------------------
                    # RRF Score
                    # -------------------------

                    current.rrf_score += rrf_score

                    current.final_score = current.rrf_score

                    # -------------------------
                    # Preserve Dense Score
                    # -------------------------

                    if result.dense_score > current.dense_score:

                        current.dense_score = result.dense_score

                        current.dense_rank = result.dense_rank

                    # -------------------------
                    # Preserve BM25 Score
                    # -------------------------

                    if result.bm25_score > current.bm25_score:

                        current.bm25_score = result.bm25_score

                        current.bm25_rank = result.bm25_rank

                    # -------------------------
                    # Merge Queries
                    # -------------------------

                    current.matched_queries = sorted(

                        set(current.matched_queries)

                        | set(result.matched_queries)

                    )

                    # -------------------------
                    # Merge Sources
                    # -------------------------

                    if result.retriever not in current.metadata["sources"]:

                        current.metadata["sources"].append(

                            result.retriever

                        )

        results = sorted(

            fused.values(),

            key=lambda x: x.rrf_score,

            reverse=True,

        )

        return results[:top_k]