import re

from app.models import ParsedJob


class JobNormalizer:

    EXPERIENCE_REGEX = re.compile(r"(\d+)\+?\s*years?", re.I)

    def normalize(self, job: ParsedJob) -> ParsedJob:

        # ---------------------------------
        # Experience
        # ---------------------------------

        if job.minimum_experience is None:

            for text in job.hard_constraints:

                match = self.EXPERIENCE_REGEX.search(text)

                if match:

                    job.minimum_experience = int(match.group(1))
                    break

        # ---------------------------------
        # Work Mode
        # ---------------------------------

        if job.work_mode is None:

            for text in job.hard_constraints:

                lower = text.lower()

                if "remote" in lower:

                    job.work_mode = "Remote"

                elif "hybrid" in lower:

                    job.work_mode = "Hybrid"

                elif "onsite" in lower:

                    job.work_mode = "Onsite"

        # ---------------------------------
        # Preferred Locations
        # ---------------------------------

        if not job.preferred_locations:

            for text in job.hard_constraints:

                if " or " in text:

                    location = text.split(" or ")[0].strip()

                    if location.lower() not in {

                        "remote",
                        "hybrid",
                        "onsite",

                    }:

                        job.preferred_locations.append(location)

        # ---------------------------------
        # Skills
        # ---------------------------------

        job.required_skills = sorted(

            set(job.required_skills)

        )

        job.preferred_skills = sorted(

            set(job.preferred_skills)

        )

        job.must_have = sorted(

            set(job.must_have)

        )

        return job
    def merge_hyre(
        self,
        job: ParsedJob,
        hyre,):

        if not job.required_skills:
            job.required_skills = hyre.skills.copy()

        if not job.industries:
            job.industries = hyre.industries.copy()

        if not job.preferred_companies:
            job.preferred_companies = hyre.preferred_companies.copy()

        if not job.preferred_locations:
            job.preferred_locations = hyre.locations.copy()

        if not job.work_mode:
            job.work_mode = hyre.work_mode

        return job