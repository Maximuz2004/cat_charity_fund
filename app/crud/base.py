from typing import Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

Model = TypeVar('Model', bound=Base)
Schema = TypeVar('Schema', bound=BaseModel)


class CRUDBase(Generic[Model, Schema]):

    def __init__(self, model: Model):
        self.model = model

    async def create(
            self,
            object_in: Schema,
            session: AsyncSession,
            commit: bool = True,
            user: Optional[User] = None,
    ) -> Optional[Model]:
        object_in_data = object_in.dict()
        if user:
            object_in_data['user_id'] = user.id
        db_object = self.model(**object_in_data)
        session.add(db_object)
        if commit:
            await session.commit()
            await session.refresh(db_object)
        return db_object

    async def get(
            self,
            object_id: int,
            session: AsyncSession,
    ) -> Optional[Model]:
        db_object = await session.execute(
            select(self.model).where(self.model.id == object_id)
        )
        return db_object.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession,
    ) -> list[Optional[Model]]:
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def update(
            self,
            db_object: Model,
            object_in: Schema,
            session: AsyncSession,
    ) -> Optional[Model]:
        object_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)
        for field in object_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def remove(
            self,
            db_object: Model,
            session: AsyncSession,
    ) -> Optional[Model]:
        await session.delete(db_object)
        await session.commit()
        return db_object

    async def get_open_objects(
            self,
            session: AsyncSession
    ) -> list[Optional[Model]]:
        query = await session.execute(
            select(
                self.model
            ).where(
                ~self.model.fully_invested
            ).order_by(
                self.model.create_date
            )
        )
        return query.scalars().all()
