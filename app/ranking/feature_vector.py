from typing import Any

from pydantic import BaseModel, Field

from app.models.candidate import Candidate


class FeatureVector(BaseModel):

    candidate_id: str

    # -----------------------------
    # Retrieval Scores
    # -----------------------------

    dense_score: float = 0.0
    bm25_score: float = 0.0
    rrf_score: float = 0.0
    cross_encoder_score: float = 0.0
    final_score: float = 0.0

    # -----------------------------
    # Matching Features
    # -----------------------------

    skill_overlap: float = 0.0
    preferred_skill_overlap: float = 0.0
    experience_gap: float = 0.0
    title_similarity: float = 0.0
    industry_match: float = 0.0
    location_match: float = 0.0

    # -----------------------------
    # Candidate Signals
    # -----------------------------

    github_score: float = 0.0
    recruiter_response_rate: float = 0.0
    profile_completeness: float = 0.0

    # -----------------------------
    # Pipeline Context
    # -----------------------------

    candidate: Candidate | None = None

    matched_queries: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)