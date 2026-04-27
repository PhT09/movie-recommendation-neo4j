from database.connection import driver
from database.crud import sync_rating_edge, get_user_ratings

def rate_movie(user_id: int, movie_id: int, rating: float):
    # sync_rating_edge handles both creating/updating (>= 3) and deleting (< 3)
    sync_rating_edge(driver, user_id, movie_id, rating)
    return {"userId": user_id, "movieId": movie_id, "rating": rating}

def get_ratings_by_user(user_id: int):
    return get_user_ratings(driver, user_id)
