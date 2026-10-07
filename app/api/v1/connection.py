from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.connection import CreateConnectionSchema, UpdateConnectionSchema
from app.services.connection import ConnectionService

router = APIRouter(
    tags=["connections"],
    prefix="/connections",
)

service = ConnectionService()

@router.post("/create")
async def create_connection(
    data: CreateConnectionSchema,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await service.create_connection(
        data=data,
        user=user,
        session=session,
    )
@router.get("")
async def get_all_user_connections(
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await service.get_all_user_connections(
        user=user,
        session=session,
    )

@router.patch("")
async def update_person(
        connection_id: int,
        data: UpdateConnectionSchema,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
):
    return await service.update_connection(
        session=session,
        connection_id=connection_id,
        user=user,
        data = data,
    )
