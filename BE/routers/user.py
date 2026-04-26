from fastapi import APIRouter, HTTPException
from models.schemas import UserResponse
from db.neo4j_conn import neo4j_conn

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    # Try finding user by userId or id
    query = "MATCH (u:User) WHERE u.userId = $user_id OR u.id = $user_id RETURN u LIMIT 1"
    params = {"user_id": user_id}
    
    try:
        result = neo4j_conn.query(query, params)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
            
        u = dict(result[0]["u"])
        return UserResponse(
            user_id=u.get("userId") or u.get("id"),
            name=u.get("name", f"User {user_id}")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
