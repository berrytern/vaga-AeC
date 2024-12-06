from typing import Dict, Any
from src.infrastructure.database.schemas import AdminSchema
from src.application.domain.models import AdminModel, AdminList
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy import select, delete
from json import loads


class AdminRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session  # Database session

    async def create(self, data: Dict[str, Any]):
        insert_stmt = (
            AdminSchema.__table__.insert()
            .returning(
                AdminSchema.id,
                AdminSchema.name,
                AdminSchema.email,
                AdminSchema.created_at,
                AdminSchema.updated_at,
            )
            .values(**data)
        )
        result = (await self.session.execute(insert_stmt)).fetchone()
        if result:
            result = loads(
                AdminModel(
                    id=result[0],
                    name=result[1],
                    email=result[2],
                    created_at=result[3],
                    updated_at=result[4],
                ).model_dump_json()
            )
        return result

    async def get_one(self, fields: Dict[str, Any]):
        get_one_stmt = select(AdminSchema)
        for key, value in fields.items():
            get_one_stmt = get_one_stmt.where(
                AdminSchema.__getattribute__(AdminSchema, key) == value
            )
        get_one_stmt = get_one_stmt.limit(1)
        result = (await self.session.execute(get_one_stmt)).fetchone()
        if result:
            item: AdminSchema = result[0]
            result = loads(
                AdminModel(
                    id=item.id,
                    name=item.name,
                    email=item.email,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                ).model_dump_json()
            )
        return result

    async def get_all(self, filters={}):
        stmt = select(AdminSchema).filter_by(**filters["query"]).limit(filters["limit"])
        stream = await self.session.stream_scalars(stmt.order_by(AdminSchema.id))
        return loads(AdminList(root=[item async for item in stream]).model_dump_json())

    async def update_one(self, id, data):
        update_stmt = (
            AdminSchema.__table__.update()
            .where(AdminSchema.id == id)
            .returning(
                AdminSchema.id,
                AdminSchema.name,
                AdminSchema.email,
                AdminSchema.created_at,
                AdminSchema.updated_at,
            )
            .values(**data)
        )
        result = (await self.session.execute(update_stmt)).fetchone()
        if result:
            result = loads(
                AdminModel(
                    id=result[0],
                    name=result[1],
                    email=result[2],
                    created_at=result[3],
                    updated_at=result[4],
                ).model_dump_json()
            )
        return result

    async def delete_one(self, id):
        await self.session.execute(delete(AdminSchema).where(AdminSchema.id == id))
