from app.filtering.filter_config import FilterConfig


class HardConstraintFilter:

    def __init__(self, config: FilterConfig | None = None):

        self.config = config or FilterConfig()

    def filter(self, results, parsed_job):

        filtered = []

        for result in results:

            candidate = result.candidate

            if candidate is None:
                result.metadata["filter_status"] = "rejected"
                result.metadata["filter_failures"] = ["candidate_not_loaded"]
                continue

            failures = []

            if not self._experience(candidate, parsed_job):
                failures.append("experience")

            if not self._location(candidate, parsed_job):
                failures.append("location")

            if not self._work_mode(candidate, parsed_job):
                failures.append("work_mode")

            if not self._employment_type(candidate, parsed_job):
                failures.append("employment_type")

            if not self._required_skills(candidate, parsed_job):
                failures.append("required_skills")

            if not self._education(candidate, parsed_job):
                failures.append("education")

            if not self._blacklisted_company(candidate, parsed_job):
                failures.append("blacklisted_company")

            if failures:

                result.metadata["filter_status"] = "rejected"
                result.metadata["filter_failures"] = failures

            else:

                result.metadata["filter_status"] = "passed"
                result.metadata["filter_failures"] = []

                filtered.append(result)

        return filtered

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    def _experience(self, candidate, job):

        if job.minimum_experience is None:
            return True

        return (
            candidate.profile.years_of_experience >=
            job.minimum_experience -
            self.config.experience_tolerance_years
        )

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    def _location(self, candidate, job):

        if self.config.allow_location_mismatch:
            return True

        if not job.preferred_locations:
            return True

        return (
            candidate.profile.location.lower()
            in {loc.lower() for loc in job.preferred_locations}
        )

    # --------------------------------------------------------
    # Work Mode
    # --------------------------------------------------------

    def _work_mode(self, candidate, job):

        if self.config.allow_workmode_mismatch:
            return True

        if not job.work_mode:
            return True

        preferred = candidate.redrob_signals.preferred_work_mode

        if preferred is None:
            return True

        return preferred.lower() == job.work_mode.lower()

    # --------------------------------------------------------
    # Employment Type
    # --------------------------------------------------------

    def _employment_type(self, candidate, job):

        # Your dataset currently doesn't store this.
        # Placeholder for future datasets.

        return True

    # --------------------------------------------------------
    # Required Skills
    # --------------------------------------------------------

    def _required_skills(self, candidate, job):

        if not job.required_skills:
            return True

        candidate_skills = {

            skill.name.lower()

            for skill in candidate.skills

        }

        required = {

            skill.lower()

            for skill in job.required_skills

        }

        overlap = len(candidate_skills & required) / len(required)

        if self.config.remove_missing_required_skills:

            return overlap >= self.config.min_required_skill_overlap

        return True

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    def _education(self, candidate, job):

        if not self.config.strict_education:
            return True

        if not job.education:
            return True

        candidate_degrees = {

            edu.degree.lower()

            for edu in candidate.education

        }

        required = {

            degree.lower()

            for degree in job.education

        }

        return len(candidate_degrees & required) > 0

    # --------------------------------------------------------
    # Blacklisted Companies
    # --------------------------------------------------------

    def _blacklisted_company(self, candidate, job):

        if not self.config.remove_blacklisted_companies:
            return True

        if not job.excluded_companies:
            return True

        blacklist = {
            company.lower()
            for company in job.excluded_companies
        }

        for entry in candidate.career_history:

            if entry.company.lower() in blacklist:
                return False

        return True