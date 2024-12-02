from typing import Dict, Any
from src.infrastructure.database.schemas import BookSchema
from src.application.domain.models import BookModel, BookList
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from json import loads


class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session  # Database session

    async def create(self, data: Dict[str, Any]):
        insert_stmt = (
            BookSchema.__table__.insert()
            .returning(
                BookSchema.id,
                BookSchema.title,
                BookSchema.description,
                BookSchema.author,
                BookSchema.price,
                BookSchema.created_at,
                BookSchema.updated_at,
            )
            .values(**data)
        )
        result = (await self.session.execute(insert_stmt)).fetchone()
        if result:
            result = loads(
                BookModel(
                    id=result[0],
                    title=result[1],
                    description=result[2],
                    author=result[3],
                    price=result[4],
                    created_at=result[5],
                    updated_at=result[6],
                ).model_dump_json()
            )
        return result

    async def get_one(self, fields: Dict[str, Any]):
        get_one_stmt = select(BookSchema)
        for key, value in fields.items():
            get_one_stmt = get_one_stmt.where(
                BookSchema.__getattribute__(BookSchema, key) == value
            )
        get_one_stmt = get_one_stmt.limit(1)
        result = (await self.session.execute(get_one_stmt)).fetchone()
        if result:
            item: BookSchema = result[0]
            result = loads(
                BookModel(
                    id=item.id,
                    title=item.title,
                    description=item.description,
                    author=item.author,
                    price=item.price,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                ).model_dump_json()
            )
        return result

    async def get_all(self, filters={}):
        stmt = select(BookSchema).filter_by(**filters["query"]).limit(filters["limit"])
        stream = await self.session.stream_scalars(stmt.order_by(BookSchema.id))
        return loads(BookList(root=[item async for item in stream]).model_dump_json())

    async def update_one(self, id, data):
        update_stmt = (
            BookSchema.__table__.update()
            .returning(
                BookSchema.id,
                BookSchema.title,
                BookSchema.description,
                BookSchema.author,
                BookSchema.price,
                BookSchema.created_at,
                BookSchema.updated_at,
            )
            .where(BookSchema.id == id)
            .values(**data)
        )
        result = (await self.session.execute(update_stmt)).fetchone()
        if result:
            result = loads(
                BookModel(
                    id=result[0],
                    title=result[1],
                    description=result[2],
                    author=result[3],
                    price=result[4],
                    created_at=result[5],
                    updated_at=result[6],
                ).model_dump_json()
            )
        return result

    async def delete_one(self, id):
        await self.session.execute(delete(BookSchema).where(BookSchema.id == id))
