from typing import Type, Optional, Dict, Any
from .reader_repository import ReaderRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from json import loads
from src.infrastructure.database.schemas import FavoriteBookSchema
from src.application.domain.models import FavoriteModel, FavoriteList


class FavoriteRepository:
    def __init__(
        self,
        session: AsyncSession,
        schema: Type[FavoriteBookSchema],
        model: Type[FavoriteModel],
        list_model: Type[FavoriteList],
        reader_repository: ReaderRepository,
    ):
        self.session = session  # Database session
        self.schema = schema
        self.model = model
        self.list_model = list_model
        self.reader_repository = reader_repository

    async def create(self, reader_id: str, book_id: str) -> Optional[Dict[str, Any]]:
        insert_stmt = (
            self.schema.__table__.insert()
            .returning(
                self.schema.id,
                self.schema.reader_id,
                self.schema.book_id,
                self.schema.created_at,
                self.schema.updated_at,
            )
            .values(reader_id=reader_id, book_id=book_id)
        )
        result = (await self.session.execute(insert_stmt)).fetchone()
        if result:
            result = loads(
                FavoriteModel(
                    id=result[0],
                    reader_id=result[1],
                    book_id=result[2],
                    created_at=result[3],
                    updated_at=result[4],
                ).model_dump_json()
            )
            await self.reader_repository.update_books_read_count(reader_id, 1)
        return result

    async def get_one(self, reader_id: str, book_id: str) -> Optional[Dict[str, Any]]:
        stmt = (
            select(self.schema)
            .where(self.schema.reader_id == reader_id)
            .where(self.schema.book_id == book_id)
            .limit(1)
        )
        result = (await self.session.execute(stmt)).fetchone()
        if result:
            item: FavoriteBookSchema = result[0]
            result = loads(
                FavoriteModel(
                    id=item.id,
                    reader_id=item.reader_id,
                    book_id=item.book_id,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                ).model_dump_json()
            )
        return result

    async def get_all(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        stmt = select(self.schema).filter_by(**filters["query"]).limit(filters["limit"])
        stream = await self.session.stream_scalars(stmt.order_by(self.schema.id))
        result = [item async for item in stream]
        return loads(self.list_model(root=result).model_dump_json())

    async def delete_one(self, reader_id: str, book_id: str) -> None:
        await self.session.execute(
            delete(self.schema)
            .where(self.schema.reader_id == reader_id)
            .where(self.schema.book_id == book_id)
        )
        await self.reader_repository.update_books_read_count(reader_id, -1)
