from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.dense_retriever import DenseRetriever
from app.retrieval.rrf import ReciprocalRankFusion
from app.services.embedding_service import EmbeddingService
from app.services.candidate_repository import CandidateRepository


class HybridRetriever:

    def __init__(self):

        self.embedder = EmbeddingService()

        self.dense = DenseRetriever()

        self.bm25 = BM25Retriever()

        self.rrf = ReciprocalRankFusion()

    def search(
        self,
        queries,
        top_k=500,
    ):

        positive_queries = [

            q

            for q in queries

            if q.query_type == "positive"

        ]

        texts = [

            q.text

            for q in positive_queries

        ]

        embeddings = self.embedder.encode_batch(texts)

        dense_results = []

        bm25_results = []

        for query, embedding in zip(

            positive_queries,

            embeddings,

        ):

            dense_results.extend(

                self.dense.search(

                    embedding,

                    query.text,

                    query.weight,

                    top_k,

                )

            )

            bm25_results.extend(

                self.bm25.search(

                    query.text,

                    query.weight,

                    top_k,

                )

            )

        return self.rrf.fuse(

            dense_results,

            bm25_results,

            top_k=top_k,

        )