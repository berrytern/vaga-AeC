from src.application.domain.models import (
    AdminQueryModel,
    UpdateAdminModel,
    CreateAdminModel,
)
from src.application.services import AdminService


class AdminController:
    def __init__(self, service: AdminService):
        self.service = service

    async def create(self, admin: CreateAdminModel):
        result = await self.service.create(admin)
        return result, 201, {}

    async def get_one(self, admin_id: str):
        result = await self.service.get_one(admin_id)
        return result, 200, {}

    async def get_all(self, query: AdminQueryModel):
        result = await self.service.get_all(query)
        return result, 200, {}

    async def update_one(self, admin_id: str, admin: UpdateAdminModel):
        result = await self.service.update_one(admin_id, admin)
        return result, 200, {}

    async def delete_one(self, admin_id: str):
        await self.service.delete_one(admin_id)
        return None, 204, {}
