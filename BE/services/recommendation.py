from database.connection import driver
from database.recommendation import (
    get_recommendations_by_user_similarity,
    get_recommendations_by_genre,
    get_top_rated_movies,
    get_similar_movies_by_movie
)

def recommend_by_user(user_id: int, limit: int = 10):
    """
    Combines different recommendation strategies for a user using Waterfall logic.
    1. Collaborative Filtering
    2. Fallback to Genre (Content-Based)
    3. Fallback to Top Rated (Cold Start)
    """
    # 1. Collaborative Filtering
    movies = get_recommendations_by_user_similarity(driver, user_id, limit)
    
    # 2. Content-Based (Genre)
    if not movies:
        movies = get_recommendations_by_genre(driver, user_id, limit)
        
    # 3. Cold Start (Top Rated)
    if not movies:
        movies = get_top_rated_movies(driver, limit)
        
    return movies

def recommend_by_movie(movie_id: int, limit: int = 10):
    """
    Finds similar movies for a given movie based on genres.
    """
    return get_similar_movies_by_movie(driver, movie_id, limit)
