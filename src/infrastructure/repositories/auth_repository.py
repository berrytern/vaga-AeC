from typing import Dict, Any
from src.application.domain.models import AuthModel
from src.infrastructure.database.schemas import AuthSchema
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy import select, delete
from json import loads


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: Dict[str, Any]):
        insert_stmt = (
            AuthSchema.__table__.insert()
            .returning(
                AuthSchema.id,
                AuthSchema.username,
                AuthSchema.user_type,
                AuthSchema.last_login,
                AuthSchema.foreign_id,
            )
            .values(**data)
        )
        result = (await self.session.execute(insert_stmt)).fetchone()
        if result:
            result = loads(
                AuthModel(
                    id=result[0],
                    username=result[1],
                    user_type=result[2],
                    last_login=result[3],
                    foreign_id=result[4],
                ).model_dump_json(exclude_none=True)
            )
        return result

    async def get_one(self, fields: Dict[str, Any]):
        get_one_stmt = select(AuthSchema)
        for key, value in fields.items():
            get_one_stmt = get_one_stmt.where(
                AuthSchema.__getattribute__(AuthSchema, key) == value
            )
        get_one_stmt = get_one_stmt.limit(1)
        result = (await self.session.execute(get_one_stmt)).fetchone()
        if result:
            item: AuthSchema = result[0]
            result = loads(
                AuthModel(
                    id=item.id,
                    username=item.username,
                    password=item.password,
                    user_type=item.user_type,
                    last_login=item.last_login,
                    foreign_id=item.foreign_id,
                ).model_dump_json()
            )
        return result

    async def get_one_by_username(self, username):
        get_one_stmt = (
            select(AuthSchema).where(AuthSchema.username == username).limit(1)
        )
        result = (await self.session.execute(get_one_stmt)).fetchone()
        return result

    async def get_all(self):
        stmt = select(AuthSchema).limit(100)
        stream = await self.session.stream_scalars(stmt.order_by(AuthSchema.id))
        return [item async for item in stream]

    async def update_one(self, id, data):
        update_stmt = (
            AuthSchema.__table__.update()
            .returning(
                AuthSchema.id,
                AuthSchema.username,
                AuthSchema.last_login,
                AuthSchema.user_type,
                AuthSchema.foreign_id,
            )
            .where(AuthSchema.id == id)
            .values(**data)
        )
        result = (await self.session.execute(update_stmt)).fetchone()
        if result:
            result = loads(
                AuthModel(
                    id=result.id,
                    username=result.username,
                    user_type=result.user_type,
                    last_login=result.last_login,
                    foreign_id=result.foreign_id,
                ).model_dump_json()
            )
        return result

    async def delete_one(self, id):
        await self.session.execute(delete(AuthSchema).where(AuthSchema.id == id))
