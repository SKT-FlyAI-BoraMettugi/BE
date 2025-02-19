from schemas.ranking import Ranking
from schemas.score import Score

def calculate_ranking(scores: list[Score]) -> list[Ranking]:
    sorted_scores = sorted(scores, key=lambda x: x.score, reverse=True)
    rankings = [Ranking(user_id=score.user_id, score=score.score, rank=idx + 1)
                for idx, score in enumerate(sorted_scores)]
    return rankings

def calculate_user_ranking(scores: list[Score], user_id) -> Ranking:
    sorted_scores = sorted(scores, key=lambda x: x.score, reverse=True)
    for idx, score in enumerate(sorted_scores):
        if score.user_id == user_id:
            return Ranking(user_id=score.user_id, score=score.score, rank=idx + 1)