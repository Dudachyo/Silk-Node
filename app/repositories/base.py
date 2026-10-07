from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:

    model = None

    def __init__(self, session:AsyncSession):
        self.session = session

    async def create(self, **kwargs):
        self.check_attribute(**kwargs)
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj


    async def get_one(self, **kwargs):
        conditions = self.check_attribute(create_condition=True,**kwargs)
        query = select(self.model).where(*conditions)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_many(self, **kwargs):
        conditions = self.check_attribute(create_condition=True,**kwargs)
        query = select(self.model).where(*conditions)
        result = await self.session.execute(query)
        return result.scalars().all()


    async def exists(self, **kwargs):
        conditions = self.check_attribute(create_condition=True,**kwargs)
        query = select(self.model).where(*conditions)
        result = await self.session.execute(query)
        return  result.scalar_one_or_none() is not None




    def check_attribute(self, create_condition=False, **kwargs):
        conditions = []
        for key, value in kwargs.items():
            if not hasattr(self.model, key):
                raise AttributeError(
                    f"Model '{self.model.__name__}' has no column '{key}'"
                )
            if create_condition:
                conditions.append(
                    getattr(self.model, key) == value
                )
        return conditions
