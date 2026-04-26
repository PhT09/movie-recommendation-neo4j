from fastapi import APIRouter, HTTPException
from models.schemas import UserResponse, UserCreate
from db.neo4j_conn import neo4j_conn

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user_data: UserCreate):
    # Find the max userId or id and create a new one
    query_max_id = "MATCH (u:User) RETURN MAX(u.userId) AS maxUserId, MAX(u.id) AS maxId"
    
    try:
        result = neo4j_conn.query(query_max_id)
        max_user_id = result[0]["maxUserId"] if result and result[0]["maxUserId"] is not None else 0
        max_id = result[0]["maxId"] if result and result[0]["maxId"] is not None else 0
        
        new_id = max(max_user_id, max_id) + 1
        
        # Create new user
        query_create = """
        CREATE (u:User {userId: $new_id, id: $new_id, name: $name})
        RETURN u
        """
        params = {"new_id": new_id, "name": user_data.name}
        
        create_result = neo4j_conn.query(query_create, params)
        u = dict(create_result[0]["u"])
        
        return UserResponse(
            user_id=u.get("userId") or u.get("id"),
            name=u.get("name")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
