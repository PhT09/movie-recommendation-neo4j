from models.schemas import Movie
from typing import List

# This is a mock service mimicking Member B's Python logic

def recommend_by_user(user_id: int) -> List[Movie]:
    # Mock data
    return [
        Movie(id=1, title="Inception", genres=["Sci-Fi", "Action"]),
        Movie(id=2, title="The Matrix", genres=["Sci-Fi", "Action"])
    ]

def recommend_by_movie(movie_id: int) -> List[Movie]:
    # Mock data
    return [
        Movie(id=3, title="Interstellar", genres=["Sci-Fi", "Drama"]),
        Movie(id=4, title="Arrival", genres=["Sci-Fi", "Drama"])
    ]
