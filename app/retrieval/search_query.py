from pydantic import BaseModel, Field


class SearchQuery(BaseModel):

    text: str

    weight: float = 1.0

    query_type: str

    category: str

    sources: list[str] = Field(default_factory=list)