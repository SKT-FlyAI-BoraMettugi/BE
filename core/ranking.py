from schemas.ranking import Ranking
from schemas.score import Score

def calculate_ranking(scores: list[Score]) -> list[Ranking]:
    sorted_scores = sorted(scores, key=lambda x: x.score, reverse=True)
    rankings = [Ranking(user_id=score.user_id, score=score.score, rank=idx + 1)
                for idx, score in enumerate(sorted_scores)]
    return rankings