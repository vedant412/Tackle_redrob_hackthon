from app.explanations.explanation import CandidateExplanation


class ExplanationGenerator:

    def generate(

        self,

        ranked_candidates,

        parsed_job,

    ):

        explanations = []

        for rank, candidate in enumerate(

            ranked_candidates,

            start=1,

        ):

            profile = candidate.metadata

            matched_skills = []
            missing_skills = []

            # ----------------------------------------
            # Skills
            # ----------------------------------------

            candidate_skills = {

                s.name.lower()

                for s in candidate.candidate.skills

            }

            required_skills = {

                s.lower()

                for s in parsed_job.required_skills

            }

            for skill in required_skills:

                if skill in candidate_skills:

                    matched_skills.append(skill)

                else:

                    missing_skills.append(skill)

            # ----------------------------------------
            # Strengths
            # ----------------------------------------

            strengths = []

            if candidate.dense_score > 0.5:

                strengths.append(

                    "High semantic similarity"

                )

            if candidate.bm25_score > 2:

                strengths.append(

                    "Strong keyword match"

                )

            if len(matched_skills) >= 3:

                strengths.append(

                    "Excellent skill overlap"

                )

            if candidate.profile_completeness >= 70:

                strengths.append(

                    "Complete profile"

                )

            if candidate.recruiter_response_rate >= 0.5:

                strengths.append(

                    "High recruiter response rate"

                )

            # ----------------------------------------
            # Weaknesses
            # ----------------------------------------

            weaknesses = []

            if len(missing_skills):

                weaknesses.append(

                    "Missing some required skills"

                )

            if candidate.profile_completeness < 50:

                weaknesses.append(

                    "Profile is incomplete"

                )

            if candidate.github_score < 10:

                weaknesses.append(

                    "Limited GitHub activity"

                )

            # ----------------------------------------
            # Confidence
            # ----------------------------------------

            confidence = min(

                1.0,

                candidate.final_score,

            )

            # ----------------------------------------
            # Reasoning
            # ----------------------------------------

            reasoning = (

                f"Strong semantic retrieval "

                f"(Dense={candidate.dense_score:.2f}), "

                f"BM25={candidate.bm25_score:.2f}, "

                f"matched {len(matched_skills)} required skills "

                f"with {profile['experience']} years of experience."

            )

            explanations.append(

                CandidateExplanation(

                    candidate_id=candidate.candidate_id,

                    rank=rank,

                    final_score=candidate.final_score,

                    confidence=confidence,

                    matched_skills=matched_skills,

                    missing_skills=missing_skills,

                    matched_titles=[

                        profile["current_title"]

                    ],

                    matched_industries=[],

                    matched_companies=[

                        profile["current_company"]

                    ],

                    matched_locations=[],

                    retrieval_sources=candidate.metadata.get(

                        "sources",

                        [],

                    ),

                    matched_queries=candidate.matched_queries,

                    dense_score=candidate.dense_score,

                    bm25_score=candidate.bm25_score,

                    rrf_score=candidate.rrf_score,

                    cross_encoder_score=getattr(

                        candidate,

                        "cross_encoder_score",

                        0.0,

                    ),

                    experience=profile["experience"],

                    profile_completeness=candidate.profile_completeness,

                    recruiter_response_rate=candidate.recruiter_response_rate,

                    github_score=candidate.github_score,

                    strengths=strengths,

                    weaknesses=weaknesses,

                    reasoning=reasoning,

                    metadata=profile,

                )

            )

        return explanations