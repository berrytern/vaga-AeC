from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from json import loads
from src.infrastructure.database.schemas import FavoriteBookSchema
from src.application.domain.models import FavoriteModel, FavoriteList


class FavoriteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, reader_id: str, book_id: str) -> Optional[Dict[str, Any]]:
        insert_stmt = (
            FavoriteBookSchema.__table__.insert()
            .returning(
                FavoriteBookSchema.id,
                FavoriteBookSchema.reader_id,
                FavoriteBookSchema.book_id,
                FavoriteBookSchema.created_at,
                FavoriteBookSchema.updated_at,
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
        return result

    async def get_one(self, reader_id: str, book_id: str) -> Optional[Dict[str, Any]]:
        stmt = (
            select(FavoriteBookSchema)
            .where(FavoriteBookSchema.reader_id == reader_id)
            .where(FavoriteBookSchema.book_id == book_id)
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
        stmt = (
            select(FavoriteBookSchema)
            .filter_by(**filters["query"])
            .limit(filters["limit"])
        )
        stream = await self.session.stream_scalars(stmt.order_by(FavoriteBookSchema.id))
        result = [item async for item in stream]
        return loads(FavoriteList(root=result).model_dump_json())

    async def delete_one(self, reader_id: str, book_id: str) -> None:
        await self.session.execute(
            delete(FavoriteBookSchema)
            .where(FavoriteBookSchema.reader_id == reader_id)
            .where(FavoriteBookSchema.book_id == book_id)
        )
