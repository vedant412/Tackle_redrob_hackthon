from app.ranking.lightgbm_ranker import LightGBMRanker


_ranker = None


def get_ranker():

    global _ranker

    if _ranker is None:

        _ranker = LightGBMRanker()

    return _ranker