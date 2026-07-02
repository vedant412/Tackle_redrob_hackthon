from app.ranking.feature_vector import FeatureVector


class FeatureEngineer:

    def build(self, results, parsed_job):

        features = []

        for result in results:

            candidate = result.candidate

            fv = FeatureVector(

                candidate_id=result.candidate_id,

                # Retrieval
                rrf_score=result.rrf_score,

                dense_score=result.dense_score,

                bm25_score=result.bm25_score,
                # Candidate Signals
                recruiter_response_rate=(
                    candidate.redrob_signals.recruiter_response_rate
                ),

                github_score=max(
                    candidate.redrob_signals.github_activity_score,
                    0.0,
                ),

                profile_completeness=(
                    candidate.redrob_signals.profile_completeness_score
                ),

            )

            # Keep reference for later stages
            fv.candidate = candidate

            fv.matched_queries = result.matched_queries

            fv.metadata = result.metadata.copy()

            # -------------------------
            # Feature Groups
            # -------------------------

            fv.skill_overlap = self._skill_overlap(
                candidate,
                parsed_job,
            )

            fv.preferred_skill_overlap = self._preferred_skill_overlap(
                candidate,
                parsed_job,
            )

            fv.experience_gap = self._experience_gap(
                candidate,
                parsed_job,
            )

            fv.title_similarity = self._title_similarity(
                candidate,
                parsed_job,
            )

            fv.industry_match = self._industry_match(
                candidate,
                parsed_job,
            )

            fv.location_match = self._location_match(
                candidate,
                parsed_job,
            )

            fv.metadata.update({

                "current_title": candidate.profile.current_title,

                "current_company": candidate.profile.current_company,

                "experience": candidate.profile.years_of_experience,

            })

            features.append(fv)

        return features

    # ==========================================================
    # Skill Features
    # ==========================================================

    def _skill_overlap(self, candidate, job):

        if not job.required_skills:
            return 0.0

        candidate_skills = {
            skill.name.lower()
            for skill in candidate.skills
        }

        required = {
            skill.lower()
            for skill in job.required_skills
        }

        return len(candidate_skills & required) / len(required)

    def _preferred_skill_overlap(self, candidate, job):

        if not job.preferred_skills:
            return 0.0

        candidate_skills = {
            skill.name.lower()
            for skill in candidate.skills
        }

        preferred = {
            skill.lower()
            for skill in job.preferred_skills
        }

        return len(candidate_skills & preferred) / len(preferred)

    # ==========================================================
    # Experience
    # ==========================================================

    def _experience_gap(self, candidate, job):

        if job.minimum_experience is None:
            return 0.0

        return (
            candidate.profile.years_of_experience
            - job.minimum_experience
        )

    # ==========================================================
    # Title
    # ==========================================================

    def _title_similarity(self, candidate, job):

        if not job.title:
            return 0.0

        jt = job.title.lower()

        ct = candidate.profile.current_title.lower()

        if jt == ct:
            return 1.0

        if jt in ct or ct in jt:
            return 0.8

        return 0.0

    # ==========================================================
    # Industry
    # ==========================================================

    def _industry_match(self, candidate, job):

        if not job.industries:
            return 0.0

        return float(

            candidate.profile.current_industry.lower()

            in {

                industry.lower()

                for industry in job.industries

            }

        )

    # ==========================================================
    # Location
    # ==========================================================

    def _location_match(self, candidate, job):

        if not job.preferred_locations:
            return 0.0

        return float(

            candidate.profile.location.lower()

            in {

                location.lower()

                for location in job.preferred_locations

            }

        )