from typing import cast, Type, Optional, List, Dict, Any
from src.application.domain.models import ReaderModel, ReaderList
from src.application.port import ReaderInterface
from src.infrastructure.database.schemas import ReaderSchema
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy import select, delete
from json import loads
from datetime import datetime
from uuid import UUID


class ReaderRepository:
    def __init__(
        self,
        session: AsyncSession,
        schema: Type[ReaderSchema],
        model: Type[ReaderModel],
        list_model: Type[ReaderList],
    ):
        self.session = session  # Database session
        self.schema = schema
        self.model = model
        self.list_model = list_model

    async def create(self, data: Dict[str, Any]) -> Optional[ReaderInterface]:
        insert_stmt = (
            self.schema.__table__.insert()
            .returning(
                self.schema.id,
                self.schema.name,
                self.schema.birthday,
                self.schema.books_read_count,
                self.schema.created_at,
                self.schema.updated_at,
            )
            .values(**data)
        )
        result = (await self.session.execute(insert_stmt)).fetchone()
        return loads(
            self.model(
                id=result[0],
                name=result[1],
                birthday=result[2],
                books_read_count=result[3],
                created_at=result[4],
                updated_at=result[5],
            ).model_dump_json()
        )

    async def get_one(self, fields: Dict[str, Any]) -> Optional[ReaderInterface]:
        get_one_stmt = select(self.schema)
        for key, value in fields.items():
            get_one_stmt = get_one_stmt.where(
                self.schema.__getattribute__(self.schema, key) == value
            )
        get_one_stmt = get_one_stmt.limit(1)
        result = (await self.session.execute(get_one_stmt)).fetchone()
        if result is not None:
            item: ReaderSchema = result[0]
            reader: ReaderInterface = loads(
                self.model(
                    id=cast(UUID, item.id),
                    name=cast(str, item.name),
                    birthday=cast(datetime, item.birthday),
                    books_read_count=item.books_read_count,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                ).model_dump_json()
            )
            return reader
        else:
            return result

    async def get_all(self, filters: Dict[str, Any]) -> List[ReaderInterface]:
        stmt = select(self.schema).filter_by(**filters["query"]).limit(filters["limit"])
        stream = await self.session.stream_scalars(stmt.order_by(self.schema.id))
        return loads(
            self.list_model(root=[item async for item in stream]).model_dump_json()
        )

    async def update_one(
        self, id: str, data: Dict[str, Any]
    ) -> Optional[ReaderInterface]:
        update_stmt = (
            self.schema.__table__.update()
            .returning(
                self.schema.id,
                self.schema.name,
                self.schema.birthday,
                self.schema.books_read_count,
                self.schema.created_at,
                self.schema.updated_at,
            )
            .where(self.schema.id == id)
            .values(**data)
        )
        result = (await self.session.execute(update_stmt)).fetchone()
        if result:
            result = loads(
                self.model(
                    id=result[0],
                    name=result[1],
                    birthday=result[2],
                    books_read_count=result[3],
                    created_at=result[4],
                    updated_at=result[5],
                ).model_dump_json()
            )
        return result

    async def update_books_read_count(
        self, id: str, count: int
    ) -> Optional[ReaderInterface]:
        update_stmt = (
            self.schema.__table__.update()
            .returning(
                self.schema.id,
                self.schema.name,
                self.schema.birthday,
                self.schema.books_read_count,
                self.schema.created_at,
                self.schema.updated_at,
            )
            .where(self.schema.id == id)
            .values(books_read_count=self.schema.books_read_count + count)
        )
        result = (await self.session.execute(update_stmt)).fetchone()
        if result:
            result = loads(
                self.model(
                    id=result[0],
                    name=result[1],
                    birthday=result[2],
                    books_read_count=result[3],
                    created_at=result[4],
                    updated_at=result[5],
                ).model_dump_json()
            )
        return result

    async def delete_one(self, id: str) -> None:
        await self.session.execute(delete(self.schema).where(self.schema.id == id))
