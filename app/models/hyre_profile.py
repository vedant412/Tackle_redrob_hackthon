from pydantic import BaseModel, Field


class HYREProfile(BaseModel):

    headline: str

    summary: str

    target_titles: list[str] = Field(default_factory=list)

    skills: list[str] = Field(default_factory=list)

    technologies: list[str] = Field(default_factory=list)

    industries: list[str] = Field(default_factory=list)

    company_types: list[str] = Field(default_factory=list)

    preferred_companies: list[str] = Field(default_factory=list)

    excluded_companies: list[str] = Field(default_factory=list)

    education: list[str] = Field(default_factory=list)

    certifications: list[str] = Field(default_factory=list)

    experience_years: str | None = None

    locations: list[str] = Field(default_factory=list)

    work_mode: str | None = None

    behavioural_traits: list[str] = Field(default_factory=list)

    recruiter_intent: list[str] = Field(default_factory=list)

    positive_queries: list[str] = Field(default_factory=list)

    negative_queries: list[str] = Field(default_factory=list)

    search_keywords: list[str] = Field(default_factory=list)