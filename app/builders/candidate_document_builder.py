from app.models.candidate import Candidate


class CandidateDocumentBuilder:
    """
    Builds a semantic document for candidate retrieval.

    This document is embedded using the dense embedding model.

    IMPORTANT:
    Do NOT include behavioral signals such as:
        - recruiter response rate
        - open to work
        - salary
        - notice period
        - profile views

    Those belong in the ranking model.
    """

    @staticmethod
    def build(candidate: Candidate) -> str:

        profile = candidate.profile

        sections = []

        # ==================================================
        # HEADER
        # ==================================================

        sections.append("### PROFESSIONAL PROFILE ###")

        sections.append(f"Headline: {profile.headline}")

        sections.append(f"Summary:\n{profile.summary}")

        sections.append(
            f"""
Current Position
Role: {profile.current_title}
Company: {profile.current_company}
Industry: {profile.current_industry}
Company Size: {profile.current_company_size}
Experience: {profile.years_of_experience} years
Location: {profile.location}, {profile.country}
""".strip()
        )

        # ==================================================
        # SKILLS
        # ==================================================

        if candidate.skills:

            skill_section = ["### TECHNICAL SKILLS ###"]

            for skill in candidate.skills:

                duration = (
                    f"{skill.duration_months} months"
                    if skill.duration_months
                    else "Unknown"
                )

                skill_section.append(
                    f"""
Skill: {skill.name}
Proficiency: {skill.proficiency}
Experience: {duration}
Endorsements: {skill.endorsements}
""".strip()
                )

            sections.append("\n\n".join(skill_section))

        # ==================================================
        # CAREER
        # ==================================================

        if candidate.career_history:

            career_section = ["### CAREER HISTORY ###"]

            for job in candidate.career_history:

                end = "Present" if job.is_current else job.end_date

                career_section.append(
                    f"""
Company: {job.company}

Title: {job.title}

Industry: {job.industry}

Company Size: {job.company_size}

Duration:
{job.start_date} to {end}

Total Duration:
{job.duration_months} months

Responsibilities:
{job.description}
""".strip()
                )

            sections.append("\n\n".join(career_section))

        # ==================================================
        # EDUCATION
        # ==================================================

        if candidate.education:

            education = ["### EDUCATION ###"]

            for edu in candidate.education:

                education.append(
                    f"""
Institution: {edu.institution}

Degree: {edu.degree}

Field: {edu.field_of_study}

Years:
{edu.start_year}-{edu.end_year}

Tier:
{edu.tier}

Grade:
{edu.grade or "Not Provided"}
""".strip()
                )

            sections.append("\n\n".join(education))

        # ==================================================
        # CERTIFICATIONS
        # ==================================================

        if candidate.certifications:

            certs = ["### CERTIFICATIONS ###"]

            for cert in candidate.certifications:

                certs.append(
                    f"""
Certification:
{cert.name}

Issuer:
{cert.issuer}

Year:
{cert.year}
""".strip()
                )

            sections.append("\n\n".join(certs))

        # ==================================================
        # LANGUAGES
        # ==================================================

        if candidate.languages:

            langs = ["### LANGUAGES ###"]

            for lang in candidate.languages:

                langs.append(
                    f"{lang.language} ({lang.proficiency})"
                )

            sections.append("\n".join(langs))

        return "\n\n".join(sections)