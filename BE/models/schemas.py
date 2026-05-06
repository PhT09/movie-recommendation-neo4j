from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: int
    title: str
    genres: List[str]
    avg_rating: Optional[float] = None

class MovieRecommendationResponse(BaseModel):
    user_id: Optional[int] = Field(None, alias='userId')
    movie_id: Optional[int] = Field(None, alias='movieId')
    recommendations: List[Movie]

class RatingCreate(BaseModel):
    user_id: int = Field(..., alias='userId')
    movie_id: int = Field(..., alias='movieId')
    rating: int

class RatingDelete(BaseModel):
    user_id: int = Field(..., alias='userId')
    movie_id: int = Field(..., alias='movieId')

class RatingResponse(BaseModel):
    user_id: int = Field(..., alias='userId')
    movie_id: int = Field(..., alias='movieId')
    rating: int
    timestamp: Optional[int] = None

class UserResponse(BaseModel):
    user_id: int = Field(..., alias='userId')
    name: Optional[str] = None

class UserCreate(BaseModel):
    name: str

