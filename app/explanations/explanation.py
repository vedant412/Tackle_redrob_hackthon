from pydantic import BaseModel, Field


class CandidateExplanation(BaseModel):

    # ---------------------------------------------------------
    # Basic Information
    # ---------------------------------------------------------

    candidate_id: str

    rank: int

    final_score: float

    confidence: float = 0.0

    # ---------------------------------------------------------
    # Matching Evidence
    # ---------------------------------------------------------

    matched_skills: list[str] = Field(default_factory=list)

    missing_skills: list[str] = Field(default_factory=list)

    matched_titles: list[str] = Field(default_factory=list)

    matched_industries: list[str] = Field(default_factory=list)

    matched_companies: list[str] = Field(default_factory=list)

    matched_locations: list[str] = Field(default_factory=list)

    # ---------------------------------------------------------
    # Retrieval Evidence
    # ---------------------------------------------------------

    retrieval_sources: list[str] = Field(default_factory=list)

    matched_queries: list[str] = Field(default_factory=list)

    dense_score: float = 0.0

    bm25_score: float = 0.0

    rrf_score: float = 0.0

    cross_encoder_score: float = 0.0

    # ---------------------------------------------------------
    # Candidate Quality
    # ---------------------------------------------------------

    experience: float = 0.0

    profile_completeness: float = 0.0

    recruiter_response_rate: float = 0.0

    github_score: float = 0.0

    # ---------------------------------------------------------
    # Human Readable
    # ---------------------------------------------------------

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)

    reasoning: str = ""

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: dict = Field(default_factory=dict)