from database.connection import driver
from database.crud import search_movies, fetch_genres

def list_movies(search: str = "", genre: str = "", skip: int = 0, limit: int = 50):
    return search_movies(driver, search_term=search, genre=genre, skip=skip, limit=limit)

def list_genres():
    return fetch_genres(driver)
