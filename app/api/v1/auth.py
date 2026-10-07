from urllib import response

from fastapi import APIRouter, Depends, Response , Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import LoginAuthSchema, RegistrationAuthSchema
from app.services.auth import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

service = AuthService()

@router.post("/register")
async def register(
    response: Response,
    user: RegistrationAuthSchema,
    session: AsyncSession = Depends(get_db),
):
    return await service.register(
        response=response,
        session=session,
        data=user,
    )

@router.post("/login")
async def login(
    response: Response,
    user: LoginAuthSchema,
    session: AsyncSession = Depends(get_db),
):
    return await service.login(
        response=response,
        session=session,
        data=user,
    )

@router.post("/logout")
async def logout(response: Response):
    return await service.logout(response)
