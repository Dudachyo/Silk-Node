from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException , Response

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import RegistrationAuthSchema, LoginAuthSchema
from app.services.security import Security


class AuthService:

    async def login(self,response:Response ,session:AsyncSession , data:LoginAuthSchema) -> dict:
        repo = UserRepository(session)

        user = await repo.get_user(email=data.email)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if not Security.verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        access_token = Security.create_access_token(
            {
                'sub': str(user.id),
            }
        )
        refresh_token = Security.create_refresh_token(
            {
                "sub": str(user.id),
            }
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24 * Security.REFRESH_TOKEN_EXPIRE_DAY,
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            samesite="lax",
            max_age=60 * Security.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        return {'message': 'login successful'}


    async def logout(self, response:Response):
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return {'message': 'logout successful'}


    async def register(self, response:Response, session:AsyncSession, data:RegistrationAuthSchema ) -> dict:
        repo = UserRepository(session)

        if await repo.exist_user(email=data.email):
            raise HTTPException(status_code=400, detail="Email already using")

        hashed_password = Security.hash_password(data.password)
        await repo.create_user(
            email=data.email,
            hashed_password=hashed_password,
        )

        await self.login(response=response,session=session,data=data)

        return {'message': 'user created successfully'}

