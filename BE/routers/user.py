from fastapi import APIRouter, HTTPException
from models.schemas import UserResponse, UserCreate
from services.user_service import create_user, get_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user_endpoint(user_data: UserCreate):
    try:
        user = create_user(user_data.name)
        if not user:
            raise HTTPException(status_code=500, detail="Failed to register user")
        return UserResponse(userId=user["userId"], name=user["name"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int):
    try:
        user = get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(userId=user["userId"], name=user["name"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
