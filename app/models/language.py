from pydantic import BaseModel, Field


class Language(BaseModel):
    """
    Represents a spoken language.
    """

    language: str = Field(
        ...,
        description="Language name"
    )

    proficiency: str = Field(
        ...,
        description="Language proficiency"
    )