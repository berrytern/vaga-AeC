from typing import Dict, Any
from src.infrastructure.database.schemas import ReaderSchema
from src.application.domain.models import ReaderModel, ReaderList
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy import select, delete
from json import loads


class ReaderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: Dict[str, Any], commit=True):
        insert_stmt = (
            ReaderSchema.__table__.insert()
            .returning(
                ReaderSchema.id,
                ReaderSchema.name,
                ReaderSchema.email,
                ReaderSchema.birthday,
                ReaderSchema.books_read_count,
                ReaderSchema.created_at,
                ReaderSchema.updated_at,
            )
            .values(**data)
        )
        result = (await self.session.execute(insert_stmt)).fetchone()
        if result:
            result = loads(
                ReaderModel(
                    id=result[0],
                    name=result[1],
                    email=result[2],
                    birthday=result[3],
                    books_read_count=result[4],
                    created_at=result[5],
                    updated_at=result[6],
                ).model_dump_json()
            )
            if commit:
                await self.session.commit()
        return result

    async def get_one(self, fields: Dict[str, Any]):
        get_one_stmt = select(ReaderSchema)
        for key, value in fields.items():
            get_one_stmt = get_one_stmt.where(
                ReaderSchema.__getattribute__(ReaderSchema, key) == value
            )
        get_one_stmt = get_one_stmt.limit(1)
        result = (await self.session.execute(get_one_stmt)).fetchone()
        if result:
            item: ReaderSchema = result[0]
            result = loads(
                ReaderModel(
                    id=item.id,
                    name=item.name,
                    email=item.email,
                    birthday=item.birthday,
                    books_read_count=item.books_read_count,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                ).model_dump_json()
            )
        return result

    async def get_all(self, filters={}):
        stmt = (
            select(ReaderSchema).filter_by(**filters["query"]).limit(filters["limit"])
        )
        stream = await self.session.stream_scalars(stmt.order_by(ReaderSchema.id))
        return loads(ReaderList(root=[item async for item in stream]).model_dump_json())

    async def update_one(self, id, data):
        update_stmt = (
            ReaderSchema.__table__.update()
            .returning(
                ReaderSchema.id,
                ReaderSchema.name,
                ReaderSchema.email,
                ReaderSchema.birthday,
                ReaderSchema.created_at,
                ReaderSchema.updated_at,
            )
            .where(ReaderSchema.id == id)
            .values(**data)
        )
        result = (await self.session.execute(update_stmt)).fetchone()
        if result:
            result = loads(
                ReaderModel(
                    id=result[0],
                    name=result[1],
                    email=result[2],
                    birthday=result[3],
                    books_read_count=result[4],
                    created_at=result[5],
                    updated_at=result[6],
                ).model_dump_json()
            )
            await self.session.commit()
        return result

    async def delete_one(self, id):
        await self.session.execute(delete(ReaderSchema).where(ReaderSchema.id == id))
        await self.session.commit()
