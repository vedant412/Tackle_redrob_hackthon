from pydantic import BaseModel, Field


class Education(BaseModel):
    """
    Represents one educational qualification.
    """

    institution: str = Field(
        ...,
        description="Name of the educational institution"
    )

    degree: str = Field(
        ...,
        description="Degree obtained"
    )

    field_of_study: str = Field(
        ...,
        description="Major or specialization"
    )

    start_year: int = Field(
        ...,
        ge=1970,
        le=2035
    )

    end_year: int = Field(
        ...,
        ge=1970,
        le=2035
    )

    grade: str | None = Field(
        default=None,
        description="GPA, percentage, or class"
    )

    tier: str | None = Field(
        default="unknown",
        description="Institution tier"
    )