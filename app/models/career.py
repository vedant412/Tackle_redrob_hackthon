from datetime import date
from pydantic import BaseModel, Field


class CareerEntry(BaseModel):
    """
    Represents one employment record in a candidate's career history.
    """

    company: str = Field(
        ...,
        description="Company name"
    )

    title: str = Field(
        ...,
        description="Job title"
    )

    start_date: date

    end_date: date | None = None

    duration_months: int = Field(
        ...,
        ge=0,
        description="Employment duration in months"
    )

    is_current: bool

    industry: str

    company_size: str

    description: str = Field(
        ...,
        description="Role responsibilities and achievements"
    )