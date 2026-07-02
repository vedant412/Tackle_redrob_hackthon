from typing import Any

from pydantic import BaseModel, Field

from app.models.candidate import Candidate


class RetrievalResult(BaseModel):

    # ==========================================================
    # Candidate
    # ==========================================================

    candidate_id: str

    candidate: Candidate | None = None

    # ==========================================================
    # Retrieval Scores
    # ==========================================================

    dense_score: float = 0.0

    bm25_score: float = 0.0

    rrf_score: float = 0.0

    final_score: float = 0.0

    # ==========================================================
    # Retrieval Ranks
    # ==========================================================

    dense_rank: int | None = None

    bm25_rank: int | None = None

    rrf_rank: int | None = None

    # ==========================================================
    # Metadata
    # ==========================================================

    retriever: str = ""

    matched_queries: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    # ==========================================================
    # Convenience
    # ==========================================================

    def add_query(self, query: str):

        if query not in self.matched_queries:

            self.matched_queries.append(query)

    def add_source(self, source: str):

        sources = self.metadata.setdefault("sources", [])

        if source not in sources:

            sources.append(source)