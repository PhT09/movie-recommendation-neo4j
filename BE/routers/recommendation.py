from fastapi import APIRouter, HTTPException
from services.recommendation_service import recommend_by_user, recommend_by_movie
from models.schemas import MovieRecommendationResponse

router = APIRouter(
    prefix="/recommend",
    tags=["Recommendations"]
)

@router.get("/user/{user_id}", response_model=MovieRecommendationResponse)
def get_recommendations_for_user(user_id: int):
    try:
        movies = recommend_by_user(user_id)
        return MovieRecommendationResponse(user_id=user_id, recommendations=movies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/movie/{movie_id}", response_model=MovieRecommendationResponse)
def get_similar_movies(movie_id: int):
    try:
        movies = recommend_by_movie(movie_id)
        return MovieRecommendationResponse(movie_id=movie_id, recommendations=movies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
