from typing import Type, Dict, Any
from src.infrastructure.database.schemas import AdminSchema
from src.application.domain.models import AdminModel, AdminList
from src.utils.default import get_db_session
from sqlalchemy import select, delete
from json import loads


class AdminRepository:
    def __init__(
        self,
        schema: Type[AdminSchema],
        model: Type[AdminModel],
        list_model: Type[AdminList],
    ):
        self.schema = schema
        self.model = model
        self.list_model = list_model

    async def create(self, data: Dict[str, Any]):
        session = get_db_session()
        insert_stmt = (
            self.schema.__table__.insert()
            .returning(
                self.schema.id,
                self.schema.name,
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
                    name=result[1],
                    created_at=result[2],
                    updated_at=result[3],
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
            item: AdminSchema = result[0]
            result = loads(
                self.model(
                    id=item.id,
                    name=item.name,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                ).model_dump_json()
            )
        return result

    async def get_all(self, filters={}):
        session = get_db_session()
        stmt = select(self.schema).filter_by(**filters["query"]).limit(filters["limit"])
        stream = await session.stream_scalars(stmt.order_by(self.schema.id))
        return loads(
            self.list_model(root=[item async for item in stream]).model_dump_json()
        )

    async def update_one(self, id, data):
        session = get_db_session()
        update_stmt = (
            self.schema.__table__.update()
            .where(self.schema.id == id)
            .returning(
                self.schema.id,
                self.schema.name,
                self.schema.created_at,
                self.schema.updated_at,
            )
            .values(**data)
        )
        result = (await session.execute(update_stmt)).fetchone()
        if result:
            result = loads(
                self.model(
                    id=result[0],
                    name=result[1],
                    created_at=result[2],
                    updated_at=result[3],
                ).model_dump_json()
            )
        return result

    async def delete_one(self, id):
        session = get_db_session()
        await session.execute(delete(self.schema).where(self.schema.id == id))
