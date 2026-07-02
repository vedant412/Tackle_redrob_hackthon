from app.ranking.feature_vector import FeatureVector


class WeightedRanker:

    def __init__(self):

        # -------------------------------------------------
        # Feature Weights
        # -------------------------------------------------

        self.weights = {

            # Retrieval
            "dense_score": 0.20,
            "bm25_score": 0.15,
            "rrf_score": 0.20,

            # Skills
            "skill_overlap": 0.15,
            "preferred_skill_overlap": 0.05,

            # Career
            "title_similarity": 0.05,
            "industry_match": 0.05,

            # Experience
            "experience_gap": 0.05,

            # Candidate Quality
            "profile_completeness": 0.03,
            "github_score": 0.02,
            "recruiter_response_rate": 0.05,

            # Future Features
            "cross_encoder_score": 0.05,
        }

    # -------------------------------------------------

    def _score(self, feature: FeatureVector) -> float:

        score = 0.0

        for feature_name, weight in self.weights.items():

            value = getattr(feature, feature_name, 0.0)

            if value is None:
                value = 0.0

            score += value * weight

        return score

    # -------------------------------------------------

    def rank(

        self,

        feature_vectors: list[FeatureVector],

        top_k: int | None = None,

    ):

        for feature in feature_vectors:

            feature.final_score = self._score(feature)

        ranked = sorted(

            feature_vectors,

            key=lambda x: x.final_score,

            reverse=True,

        )

        if top_k is not None:

            ranked = ranked[:top_k]

        return ranked