import email

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):

    model = User

    async def create_user(self, **kwargs):
        user = await self.create(**kwargs)
        await self.session.commit()
        return user

    async def get_user(self, **kwargs):
        return await self.get_one(**kwargs)

    async def exist_user(self,**kwargs):
        return await self.exists(**kwargs)

