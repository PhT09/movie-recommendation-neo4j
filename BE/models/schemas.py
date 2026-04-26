from pydantic import BaseModel
from typing import List, Optional

class Movie(BaseModel):
    id: int
    title: str
    genres: List[str]

class MovieRecommendationResponse(BaseModel):
    user_id: Optional[int] = None
    movie_id: Optional[int] = None
    recommendations: List[Movie]

class RatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: int

class RatingResponse(BaseModel):
    user_id: int
    movie_id: int
    rating: int
    timestamp: Optional[int] = None
