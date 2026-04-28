from fastapi import APIRouter, HTTPException
from services.recommendation import recommend_by_user, recommend_by_movie
from models.schemas import MovieRecommendationResponse, Movie

router = APIRouter(
    prefix="/recommend",
    tags=["Recommendations"]
)

@router.get("/user/{user_id}", response_model=MovieRecommendationResponse)
def get_recommendations_for_user(user_id: int):
    try:
        results = recommend_by_user(user_id)
        movies = [Movie(id=r["movieId"], title=r["title"], genres=r.get("genres", []), avg_rating=r.get("avg_rating")) for r in results]
        return MovieRecommendationResponse(userId=user_id, recommendations=movies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/movie/{movie_id}", response_model=MovieRecommendationResponse)
def get_similar_movies(movie_id: int):
    try:
        results = recommend_by_movie(movie_id)
        movies = [Movie(id=r["movieId"], title=r["title"], genres=r.get("genres", []), avg_rating=r.get("avg_rating")) for r in results]
        return MovieRecommendationResponse(movieId=movie_id, recommendations=movies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
