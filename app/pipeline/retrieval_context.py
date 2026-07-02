from pydantic import BaseModel, Field

from app.models.parsed_job import ParsedJob
from app.models.hyre_profile import HYREProfile
from app.retrieval.search_query import SearchQuery
from app.retrieval.retrieval_result import RetrievalResult


class RetrievalContext(BaseModel):

    parsed_job: ParsedJob

    hyre: HYREProfile

    queries: list[SearchQuery]

    retrieved: list[RetrievalResult] = Field(default_factory=list)

    filtered: list[RetrievalResult] = Field(default_factory=list)

    features: dict = Field(default_factory=dict)