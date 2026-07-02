import pandas as pd


class RankInference:

    def __init__(

        self,

        ranker,

    ):

        self.ranker = ranker

    def rank(

        self,

        feature_vectors,

    ):

        X = pd.DataFrame(

            [

                fv.model_dump()

                for fv in feature_vectors

            ]

        )

        metadata = X.pop("metadata")

        candidate_ids = X.pop("candidate_id")

        scores = self.ranker.predict(X)

        ranking = []

        for cid, score, meta in zip(

            candidate_ids,

            scores,

            metadata,

        ):

            ranking.append(

                {

                    "candidate_id": cid,

                    "rank_score": float(score),

                    "metadata": meta,

                }

            )

        ranking.sort(

            key=lambda x: x["rank_score"],

            reverse=True,

        )

        return ranking