from fastapi import APIRouter, HTTPException
from models.schemas import RatingCreate, RatingResponse, RatingDelete
from db.neo4j_conn import neo4j_conn
import time

router = APIRouter(
    prefix="/rating",
    tags=["Ratings"]
)

@router.post("/", response_model=RatingResponse, status_code=201)
def create_rating(rating_data: RatingCreate):
    query = """
    MERGE (u:User {id: $user_id})
    MERGE (m:Movie {id: $movie_id})
    MERGE (u)-[r:LIKE]->(m)
    SET r.rating = $rating, r.timestamp = $timestamp
    RETURN u.id AS user_id, m.id AS movie_id, r.rating AS rating, r.timestamp AS timestamp
    """
    timestamp = int(time.time())
    params = {
        "user_id": rating_data.user_id,
        "movie_id": rating_data.movie_id,
        "rating": rating_data.rating,
        "timestamp": timestamp
    }
    
    try:
        result = neo4j_conn.query(query, params)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create rating")
        
        record = result[0]
        return RatingResponse(
            user_id=record["user_id"],
            movie_id=record["movie_id"],
            rating=record["rating"],
            timestamp=record["timestamp"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/", response_model=RatingResponse)
def update_rating(rating_data: RatingCreate):
    query = """
    MATCH (u:User {id: $user_id})-[r:LIKE]->(m:Movie {id: $movie_id})
    SET r.rating = $rating, r.timestamp = $timestamp
    RETURN u.id AS user_id, m.id AS movie_id, r.rating AS rating, r.timestamp AS timestamp
    """
    timestamp = int(time.time())
    params = {
        "user_id": rating_data.user_id,
        "movie_id": rating_data.movie_id,
        "rating": rating_data.rating,
        "timestamp": timestamp
    }
    
    try:
        result = neo4j_conn.query(query, params)
        if not result:
            raise HTTPException(status_code=404, detail="Rating not found")
        
        record = result[0]
        return RatingResponse(
            user_id=record["user_id"],
            movie_id=record["movie_id"],
            rating=record["rating"],
            timestamp=record["timestamp"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/")
def delete_rating(rating_data: RatingDelete):
    query = """
    MATCH (u:User {id: $user_id})-[r:LIKE]->(m:Movie {id: $movie_id})
    DELETE r
    RETURN COUNT(r) AS deleted_count
    """
    params = {
        "user_id": rating_data.user_id,
        "movie_id": rating_data.movie_id
    }
    
    try:
        result = neo4j_conn.query(query, params)
        if not result or result[0]["deleted_count"] == 0:
            raise HTTPException(status_code=404, detail="Rating not found")
        
        return {"message": "Rating deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
