from pydantic import BaseModel, Field


class Skill(BaseModel):
    """
    Represents a candidate skill.
    """

    name: str = Field(
        ...,
        description="Skill name"
    )

    proficiency: str = Field(
        ...,
        description="Skill proficiency"
    )

    endorsements: int = Field(
        default=0,
        ge=0,
        description="Number of endorsements"
    )

    duration_months: int | None = Field(
        default=0,
        ge=0,
        description="Months of experience using this skill"
    )