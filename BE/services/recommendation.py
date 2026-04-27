from database.connection import driver
from database.recommendation import (
    get_recommendations_by_genre,
    get_recommendations_by_user_similarity,
    get_similar_movies_by_movie
)

def recommend_by_user(user_id: int, limit: int = 10):
    """
    Combines different recommendation strategies for a user.
    """
    # For now, let's just use user similarity (collaborative filtering)
    return get_recommendations_by_user_similarity(driver, user_id, limit)

def recommend_by_movie(movie_id: int, limit: int = 10):
    """
    Finds similar movies for a given movie.
    """
    return get_similar_movies_by_movie(driver, movie_id, limit)
