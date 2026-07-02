from pathlib import Path

import joblib
import lightgbm as lgb
import pandas as pd

from app.config import LIGHTGBM_MODEL_PATH


class LightGBMRanker:

    def __init__(self):

        self.model = None

        if Path(LIGHTGBM_MODEL_PATH).exists():

            self.model = joblib.load(
                LIGHTGBM_MODEL_PATH
            )

    # ------------------------------

    def train(

        self,

        X,

        y,

        group,

    ):

        self.model = lgb.LGBMRanker(

            objective="lambdarank",

            metric="ndcg",

            learning_rate=0.05,

            n_estimators=300,

            num_leaves=64,

            random_state=42,

        )

        self.model.fit(

            X,

            y,

            group=group,

        )

        joblib.dump(

            self.model,

            LIGHTGBM_MODEL_PATH,

        )

    # ------------------------------

    def predict(

        self,

        X,

    ):

        if self.model is None:

            raise RuntimeError(
                "Ranker not trained."
            )

        return self.model.predict(X)