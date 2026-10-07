from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.repositories.connection import ConnectionRepository
from app.repositories.person import PersonRepository
from app.schemas.connection import CreateConnectionSchema, ReadConnectionSchema, UpdateConnectionSchema
from app.services.integrity import is_unique_conflict


class ConnectionService:

    async def create_connection(
            self,
            session: AsyncSession,
            user: User,
            data:CreateConnectionSchema
    ) -> ReadConnectionSchema | HTTPException:

        repo = ConnectionRepository(session=session)
        a_id, b_id = sorted([data.person_id_a, data.person_id_b])
        if a_id == b_id:
            raise HTTPException(status_code=400, detail="You can't create a connection with same person")

        person_repo = PersonRepository(session=session)
        person_a = await person_repo.get_user_person_by_id(
            person_id = a_id,
            user = user,
        )
        person_b = await person_repo.get_user_person_by_id(
            person_id = b_id,
            user = user,
        )
        if person_a is None or person_b is None:
            raise HTTPException(status_code=404, detail='Person not found')

        if await repo.get_user_connection_by_both_person(person_a_id=person_a.id, person_b_id=person_b.id, user=user) is not None:
            raise HTTPException(status_code=409, detail="You already have this connection")



        try:
            connection = await repo.create_connection(
                owner_user_id=user.id,
                person_a_id=a_id,
                person_b_id=b_id,
                via=data.via,
            )
        except IntegrityError as exc:
            await session.rollback()
            if is_unique_conflict(exc, "uq_connection_pair_per_owner"):
                raise HTTPException(status_code=409, detail="You already have this connection") from exc
            raise
        return ReadConnectionSchema.model_validate(connection)



    async def get_all_user_connections(
            self,
            session: AsyncSession,
            user:User
    ) -> list[ReadConnectionSchema]:

        repo = ConnectionRepository(session=session)
        connections = await repo.get_all_user_connections(
            user = user,
        )
        return [ReadConnectionSchema.model_validate(c) for c in connections]




    async def update_connection(
            self,
            session: AsyncSession,
            connection_id: int,
            user:User,
            data:UpdateConnectionSchema
    ) -> ReadConnectionSchema | dict:

        repo = ConnectionRepository(session=session)
        person_repo = PersonRepository(session=session)
        connection = await repo.get_user_connection_by_id(
            connection_id = connection_id,
            user = user,
        )
        if connection is None:
            raise HTTPException(status_code=404, detail='Connection not found')


        person_a = await person_repo.get_user_person_by_id(
            user=user,
            person_id=data.person_a_id if data.person_a_id is not None else connection.person_a_id,
        )

        person_b = await person_repo.get_user_person_by_id(
            user=user,
            person_id=data.person_b_id if data.person_b_id is not None else connection.person_b_id,
        )

        if (person_a is None) or (person_b is None):
            raise HTTPException(status_code=404, detail="Person not found")

        id_a , id_b = sorted([person_a.id , person_b.id])

        if id_a == id_b:
            raise HTTPException(status_code=400, detail="You can't create a connection with same person")

        existing_connection = await repo.get_user_connection_by_both_person(
            person_a_id=id_a,
            person_b_id=id_b,
            user=user,
        )
        if existing_connection is not None and existing_connection.id != connection.id:
            raise HTTPException(status_code=409, detail="You already have this connection")

        update_dict = {
            'person_a_id': id_a ,
            'person_b_id': id_b,
            'via': data.via if data.via is not None else connection.via,
        }


        for field, value in update_dict.items():
            setattr(connection, field, value)

        try:
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            if is_unique_conflict(exc, "uq_connection_pair_per_owner"):
                raise HTTPException(status_code=409, detail="You already have this connection") from exc
            raise

        return ReadConnectionSchema.model_validate(connection)

