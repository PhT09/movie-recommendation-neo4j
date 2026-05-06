from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.schemas import Movie
from services.movie_service import list_movies, list_genres

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

@router.get("/genres", response_model=List[str])
def get_genres():
    try:
        return list_genres()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Movie])
def get_movies(
    search: Optional[str] = "", 
    genre: Optional[str] = "",
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100)
):
    try:
        results = list_movies(search=search, genre=genre, skip=skip, limit=limit)
        # Map DB results to Movie schema
        movies = []
        for r in results:
            movies.append(Movie(id=r["movieId"], title=r["title"], genres=[])) # Genres fetch can be improved if needed
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
