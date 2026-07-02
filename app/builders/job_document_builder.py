class JobDocumentBuilder:
    """
    Builds the semantic document used for embedding jobs.

    Initially this simply combines

    - Parsed Job Description
    - HYRE output

    Later this builder will be expanded.
    """

    @staticmethod
    def build(
        parsed_job: dict,
        hyre_profile: str,
    ) -> str:

        sections = []

        sections.append("### JOB PROFILE ###")

        if "title" in parsed_job:
            sections.append(f"Role: {parsed_job['title']}")

        if "summary" in parsed_job:
            sections.append(f"Summary:\n{parsed_job['summary']}")

        if "skills" in parsed_job:

            skills = "\n".join(parsed_job["skills"])

            sections.append(
                "Required Skills:\n" + skills
            )

        if "experience" in parsed_job:

            sections.append(
                f"Required Experience: {parsed_job['experience']}"
            )

        sections.append("### IDEAL CANDIDATE ###")

        sections.append(hyre_profile)

        return "\n\n".join(sections)