from typing import Type, Tuple, List, Dict, Any
from src.infrastructure.database.schemas import BookSchema
from src.application.domain.models import BookModel, BookList
from src.utils.default import get_db_session, get_aux_db_session, aux_db_session_var
from sqlalchemy import select, insert, update, delete, func
from asyncio import gather
from json import loads
from uuid import UUID


class BookRepository:
    def __init__(
        self,
        schema: Type[BookSchema],
        model: Type[BookModel],
        list_model: Type[BookList],
    ):
        self.schema = schema
        self.model = model
        self.list_model = list_model

    async def create(self, data: Dict[str, Any]):
        session = get_db_session()
        insert_stmt = (
            insert(self.schema.__table__)
            .returning(
                self.schema.id,
                self.schema.title,
                self.schema.description,
                self.schema.author,
                self.schema.price,
                self.schema.created_at,
                self.schema.updated_at,
            )
            .values(**data)
        )
        result = (await session.execute(insert_stmt)).fetchone()
        if result:
            result = loads(
                self.model(
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
        session = get_db_session()
        get_one_stmt = select(self.schema)
        for key, value in fields.items():
            get_one_stmt = get_one_stmt.where(
                self.schema.__getattribute__(self.schema, key) == value
            )
        get_one_stmt = get_one_stmt.limit(1)
        result = (await session.execute(get_one_stmt)).fetchone()
        if result:
            item: BookSchema = result[0]
            result = loads(
                self.model(
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

    async def get_all(self, filters={}) -> Tuple[List[Dict[str, Any]], int]:
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

    async def update_one(self, id: UUID, data: Dict[str, Any]):
        session = get_db_session()
        update_stmt = (
            update(self.schema.__table__)
            .returning(
                self.schema.id,
                self.schema.title,
                self.schema.description,
                self.schema.author,
                self.schema.price,
                self.schema.created_at,
                self.schema.updated_at,
            )
            .where(self.schema.id == id)
            .values(**data)
        )
        result = (await session.execute(update_stmt)).fetchone()
        if result:
            result = loads(
                self.model(
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

    async def delete_one(self, id: UUID):
        session = get_db_session()
        await session.execute(delete(self.schema).where(self.schema.id == id))
