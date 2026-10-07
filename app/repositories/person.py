from typing import List

from app.models.person import Person
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.person import CreatePersonSchema


class PersonRepository(BaseRepository):

    model = Person

    async def create_person(self, **kwargs) -> Person:
        person =  await self.create(**kwargs)
        await self.session.commit()
        return person

    async def get_person_by_id(self,person_id: int) -> Person:
        return await self.get_one(id=person_id)

    async def get_user_person_by_id(self, person_id:int , user:User) -> Person:
        return await self.get_one(id=person_id,owner_user_id=user.id)

    async def get_all_user_persons(self,user: User) -> List[Person]:
        return await self.get_many(owner_user_id=user.id)

