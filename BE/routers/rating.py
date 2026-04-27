from fastapi import APIRouter, HTTPException
from models.schemas import RatingCreate, RatingResponse, RatingDelete
from services.rating_service import rate_movie, get_ratings_by_user
import time

router = APIRouter(
    prefix="/rating",
    tags=["Ratings"]
)

@router.post("/", response_model=RatingResponse, status_code=201)
def create_rating(rating_data: RatingCreate):
    try:
        result = rate_movie(rating_data.user_id, rating_data.movie_id, rating_data.rating)
        return RatingResponse(
            userId=result["userId"],
            movieId=result["movieId"],
            rating=result["rating"],
            timestamp=int(time.time())
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/", response_model=RatingResponse)
def update_rating(rating_data: RatingCreate):
    try:
        result = rate_movie(rating_data.user_id, rating_data.movie_id, rating_data.rating)
        return RatingResponse(
            userId=result["userId"],
            movieId=result["movieId"],
            rating=result["rating"],
            timestamp=int(time.time())
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/")
def delete_rating(rating_data: RatingDelete):
    try:
        # Using 0 as rating to trigger deletion in our sync_rating_edge logic
        rate_movie(rating_data.user_id, rating_data.movie_id, 0)
        return {"message": "Rating deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}")
def get_user_ratings_endpoint(user_id: int):
    try:
        ratings = get_ratings_by_user(user_id)
        return [
            RatingResponse(
                userId=r["userId"],
                movieId=r["movieId"],
                rating=r["rating"],
                timestamp=r["timestamp"]
            ) for r in ratings
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
