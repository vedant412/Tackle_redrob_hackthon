from typing import Optional

from pydantic import BaseModel, Field


class ParsedJob(BaseModel):

    # ==========================================================
    # BASIC INFORMATION
    # ==========================================================

    title: Optional[str] = None
    summary: Optional[str] = None
    seniority: Optional[str] = None
    employment_type: Optional[str] = None
    work_mode: Optional[str] = None

    # ==========================================================
    # EXPERIENCE
    # ==========================================================

    minimum_experience: Optional[int] = None
    maximum_experience: Optional[int] = None

    # ==========================================================
    # SKILLS
    # ==========================================================

    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    excluded_skills: list[str] = Field(default_factory=list)

    # ==========================================================
    # EDUCATION
    # ==========================================================

    education: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)

    # ==========================================================
    # COMPANY / INDUSTRY
    # ==========================================================

    industries: list[str] = Field(default_factory=list)

    preferred_companies: list[str] = Field(default_factory=list)

    excluded_companies: list[str] = Field(default_factory=list)

    # ==========================================================
    # LOCATION
    # ==========================================================

    preferred_locations: list[str] = Field(default_factory=list)

    relocation_allowed: Optional[bool] = None

    # ==========================================================
    # SALARY
    # ==========================================================

    salary_min: Optional[float] = None
    salary_max: Optional[float] = None

    # ==========================================================
    # HARD CONSTRAINTS
    # ==========================================================

    must_have: list[str] = Field(default_factory=list)

    nice_to_have: list[str] = Field(default_factory=list)

    hard_constraints: list[str] = Field(default_factory=list)

    # ==========================================================
    # NEGATIVE SIGNALS
    # ==========================================================

    avoid_backgrounds: list[str] = Field(default_factory=list)

    avoid_industries: list[str] = Field(default_factory=list)

    avoid_titles: list[str] = Field(default_factory=list)

    negative_keywords: list[str] = Field(default_factory=list)

    # ==========================================================
    # BEHAVIOURAL SIGNALS
    # ==========================================================

    behavioural_traits: list[str] = Field(default_factory=list)

    culture_fit: list[str] = Field(default_factory=list)

    # ==========================================================
    # HIRING INTENT
    # ==========================================================

    hiring_priorities: list[str] = Field(default_factory=list)

    recruiter_preferences: list[str] = Field(default_factory=list)

    # ==========================================================
    # RETRIEVAL
    # ==========================================================

    positive_queries: list[str] = Field(default_factory=list)

    negative_queries: list[str] = Field(default_factory=list)

    kg_entities: list[str] = Field(default_factory=list)

    # ==========================================================
    # HYRE
    # ==========================================================

    ideal_candidate_summary: Optional[str] = None