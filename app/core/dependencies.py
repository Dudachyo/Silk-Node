from fastapi import Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.security import Security
from app.models.user import User


async def get_current_user(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db),
) -> User:

    return await Security.get_user_object(
        session=session,
        request=request,
        response=response,
    )