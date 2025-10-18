from typing import Type, Optional, Tuple, Dict, List, Any
from .reader import ReaderRepository
from src.infrastructure.database.schemas import FavoriteBookSchema
from src.application.domain.models import FavoriteModel, FavoriteList
from src.utils.default import get_db_session, get_aux_db_session, aux_db_session_var
from sqlalchemy import select, insert, delete, func
from asyncio import gather
from json import loads
from uuid import UUID


class FavoriteRepository:
    def __init__(
        self,
        schema: Type[FavoriteBookSchema],
        model: Type[FavoriteModel],
        list_model: Type[FavoriteList],
        reader_repository: ReaderRepository,
    ):
        self.schema = schema
        self.model = model
        self.list_model = list_model
        self.reader_repository = reader_repository

    async def create(self, reader_id: UUID, book_id: UUID) -> Optional[Dict[str, Any]]:
        session = get_db_session()
        insert_stmt = (
            insert(self.schema.__table__)
            .returning(
                self.schema.id,
                self.schema.reader_id,
                self.schema.book_id,
                self.schema.created_at,
                self.schema.updated_at,
            )
            .values(reader_id=reader_id, book_id=book_id)
        )
        result = (await session.execute(insert_stmt)).fetchone()
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

    async def get_one(self, reader_id: UUID, book_id: UUID) -> Optional[Dict[str, Any]]:
        session = get_db_session()
        stmt = (
            select(self.schema)
            .where(self.schema.reader_id == reader_id)
            .where(self.schema.book_id == book_id)
            .limit(1)
        )
        result = (await session.execute(stmt)).fetchone()
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

    async def get_all(
        self, filters: Dict[str, Any]
    ) -> Tuple[List[Dict[str, Any]], int]:
        session = get_db_session()
        token, count_session = get_aux_db_session()
        stmt = select(self.schema).filter_by(**filters["query"])
        search_conditions = []
        for key, value in filters["like"].items():
            if hasattr(self.schema, key):
                search_conditions.append(getattr(self.schema, key).ilike(value))
        stmt = stmt.filter(*search_conditions)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        sort = getattr(self.schema, filters["sort"])
        if filters["sort_direction"] < 0:
            sort = sort.desc()
        total_count, stream = await gather(
            count_session.execute(count_stmt),
            session.stream_scalars(
                stmt.order_by(sort)
                .offset((filters["page"] - 1) * filters["limit"])
                .limit(filters["limit"])
            ),
        )
        total_count = total_count.scalar_one()
        if token is not None:
            aux_db_session_var.reset(token)
            await count_session.aclose()

        return loads(
            self.list_model(root=[item async for item in stream]).model_dump_json()
        ), total_count

    async def delete_one(self, reader_id: UUID, book_id: UUID) -> None:
        session = get_db_session()
        await session.execute(
            delete(self.schema)
            .where(self.schema.reader_id == reader_id)
            .where(self.schema.book_id == book_id)
        )
        await self.reader_repository.update_books_read_count(reader_id, -1)
