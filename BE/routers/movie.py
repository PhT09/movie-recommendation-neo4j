from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.schemas import Movie
from db.neo4j_conn import neo4j_conn

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

@router.get("/", response_model=List[Movie])
def get_movies(search: Optional[str] = "", genre: Optional[str] = ""):
    query = "MATCH (m:Movie) WHERE m.title IS NOT NULL"
    params = {}
    
    if search:
        query += " AND toLower(m.title) CONTAINS toLower($search)"
        params["search"] = search
        
    query += " RETURN m LIMIT 50"
    
    try:
        result = neo4j_conn.query(query, params)
        movies = []
        for row in result:
            m = dict(row["m"])
            movie_id = m.get("movieId") or m.get("id") or 0
            title = m.get("title", "Unknown")
            # If genres are stored as a string or list, handle it appropriately. 
            # We provide a fallback just in case.
            genres = m.get("genres", ["Action"])
            if isinstance(genres, str):
                genres = [g.strip() for g in genres.split("|")]
            
            # Simple genre filter logic if requested
            if genre and genre.lower() not in [g.lower() for g in genres]:
                continue
                
            movies.append(Movie(id=movie_id, title=title, genres=genres))
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
