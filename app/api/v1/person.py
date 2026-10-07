from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.person import Person
from app.models.user import User
from app.schemas.person import CreatePersonSchema , UpdatePersonSchema
from app.services.person import PersonService

router = APIRouter(
    prefix="/person",
    tags=["person"],
)

service = PersonService()

@router.post("/create")
async def create_person(
        data: CreatePersonSchema,
        session: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
):
    return await service.create_person(
        data=data,
        session=session,
        user=user,
    )
@router.get("")
async def get_all_user_persons(
        session: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
):
    return await service.get_all_user_persons(
        session=session,
        user=user,
    )

@router.patch("")
async def update_person(
        person_id: int,
        data: UpdatePersonSchema,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
):
    return await service.update_person(
        person_id=person_id,
        data=data,
        session=session,
        user=user,
    )
