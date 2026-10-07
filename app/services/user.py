from app.models.user import User
from app.repositories.user import UserRepository
from fastapi import Depends, HTTPException, Response, status,Request
from app.schemas.user import ReadUser
from app.services.security import Security


class UserService:

    async def get_user(self,user:User) -> ReadUser:
        return ReadUser.model_validate(user)
