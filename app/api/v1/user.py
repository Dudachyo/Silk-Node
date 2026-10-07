
from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

service = UserService()

@router.get("/me")
async def get_user(
    user: User = Depends(get_current_user),
):
    return await service.get_user(user=user)

