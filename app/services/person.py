from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.person import Person
from app.repositories.person import PersonRepository
from app.schemas.person import CreatePersonSchema, ReadPersonSchema, UpdatePersonSchema
from app.services.integrity import is_unique_conflict


class PersonService:

    async def get_by_id(self,session:AsyncSession , person_id: int) -> ReadPersonSchema:
        repo = PersonRepository(session=session)
        person =  await repo.get_by_id(person_id)
        return ReadPersonSchema.model_validate(person)


    async def create_person(self,user:User ,session:AsyncSession,data: CreatePersonSchema) -> ReadPersonSchema:
        repo = PersonRepository(session=session)
        if data.is_self and await repo.get_one(owner_user_id=user.id, is_self=True) is not None:
            raise HTTPException(status_code=409, detail="You already have a self person")
        try:
            person = await repo.create_person(
                owner_user_id=user.id,
                name=data.name,
                note=data.note,
                is_self=data.is_self,
                is_favourite=data.is_favourite,
            )
        except IntegrityError as exc:
            await session.rollback()
            if is_unique_conflict(exc, "uq_person_self_per_owner"):
                raise HTTPException(status_code=409, detail="You already have a self person") from exc
            raise
        return ReadPersonSchema.model_validate(person)

    async def get_all_user_persons(self,session:AsyncSession , user:User) -> List[ReadPersonSchema]:
        repo = PersonRepository(session=session)
        persons = await repo.get_all_user_persons(
            user=user
        )
        return [ReadPersonSchema.model_validate(p) for p in persons]

    async def update_person(self, session: AsyncSession, user:User , data:UpdatePersonSchema ,person_id: int) -> ReadPersonSchema:
        repo = PersonRepository(session=session)
        person = await repo.get_user_person_by_id(person_id=person_id,user=user)

        if person is None:
            raise HTTPException(status_code=404, detail="Person not found")

        if data.is_self is True:
            existing_person = await repo.get_one(owner_user_id=user.id, is_self=True)
            if existing_person is not None and existing_person.id != person.id:
                raise HTTPException(status_code=409, detail="You already have a self person")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(person, field, value)

        try:
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            if is_unique_conflict(exc, "uq_person_self_per_owner"):
                raise HTTPException(status_code=409, detail="You already have a self person") from exc
            raise
        return ReadPersonSchema.model_validate(person)




