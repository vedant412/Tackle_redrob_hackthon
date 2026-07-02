from dataclasses import dataclass


@dataclass
class FilterConfig:
    """
    Configuration for recruiter hard filters.
    """

    # Experience
    experience_tolerance_years: float = 1.0

    # Skills
    min_required_skill_overlap: float = 0.35
    remove_missing_required_skills: bool = False

    # Location
    allow_location_mismatch: bool = True

    # Work Mode
    allow_workmode_mismatch: bool = True

    # Education
    strict_education: bool = False

    # Company Filters
    remove_blacklisted_companies: bool = True