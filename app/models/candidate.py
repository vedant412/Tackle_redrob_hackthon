from pydantic import BaseModel, Field

from .profile import Profile
from .career import CareerEntry
from .education import Education
from .skill import Skill
from .certification import Certification
from .language import Language
from .redrob_signals import RedrobSignals


class Candidate(BaseModel):
    """
    Complete candidate profile.
    """

    candidate_id: str = Field(
        ...,
        description="Unique Candidate ID"
    )

    profile: Profile

    career_history: list[CareerEntry]

    education: list[Education]

    skills: list[Skill]

    certifications: list[Certification] = Field(
        default_factory=list
    )

    languages: list[Language] = Field(
        default_factory=list
    )

    redrob_signals: RedrobSignals