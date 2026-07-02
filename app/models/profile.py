from pydantic import BaseModel, Field


class Profile(BaseModel):
    """
    Basic professional information about a candidate.
    """

    anonymized_name: str = Field(..., description="Anonymized candidate name")

    headline: str = Field(
        ...,
        description="Professional headline"
    )

    summary: str = Field(
        ...,
        description="Professional summary"
    )

    location: str = Field(
        ...,
        description="City or region"
    )

    country: str

    years_of_experience: float = Field(
        ...,
        ge=0,
        le=50
    )

    current_title: str

    current_company: str

    current_company_size: str

    current_industry: str