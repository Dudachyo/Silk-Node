from typing import List
from app.models.user import User
from app.repositories.base import BaseRepository
from app.models.connection import Connection


class ConnectionRepository(BaseRepository):

    model = Connection

    async def get_user_connection_by_id(self, connection_id: int , user:User) -> Connection:
        connection = await self.get_one(id=connection_id , owner_user_id=user.id)
        return connection

    async def get_user_connection_by_both_person(self, person_a_id: int, person_b_id: int , user:User) -> Connection:
        connection = await self.get_one(person_a_id=person_a_id, person_b_id=person_b_id, owner_user_id=user.id)
        return connection

    async def create_connection(self, **kwargs) -> Connection:
        connection =  await self.create(**kwargs)
        await self.session.commit()
        return connection

    async def get_all_user_connections(self,user: User) -> List[Connection]:
        return await self.get_many(owner_user_id=user.id)