from pydantic import BaseModel, Field


class Certification(BaseModel):
    """
    Represents a professional certification.
    """

    name: str = Field(
        ...,
        description="Certification name"
    )

    issuer: str = Field(
        ...,
        description="Issuing organization"
    )

    year: int = Field(
        ...,
        ge=1970,
        le=2035
    )