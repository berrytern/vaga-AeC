from typing import Optional, List
from .credential_model import CreateAuthModel
from .query_model import QueryModel
from pydantic import (
    BaseModel,
    RootModel,
    ConfigDict,
    Field,
    field_serializer,
    EmailStr,
    StrictStr,
)
from uuid import UUID
from datetime import datetime


class CreateAdminModel(CreateAuthModel):
    name: StrictStr = Field(..., min_length=10, max_length=60)
    email: EmailStr = Field(..., min_length=10, max_length=250)


class UpdateAdminModel(BaseModel):
    name: Optional[StrictStr] = Field(None, min_length=10, max_length=60)
    email: Optional[EmailStr] = Field(None, min_length=10, max_length=250)


class AdminModel(BaseModel):
    id: Optional[UUID] = None
    name: Optional[StrictStr] = None
    email: Optional[EmailStr] = None
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now().replace(microsecond=0)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now().replace(microsecond=0)
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
        json_encoders={
            datetime: lambda dt: dt.replace(microsecond=0).isoformat() + "Z"
        },
    )

    @field_serializer("id")
    def serialize_id(self, id):
        return str(id)


class AdminList(RootModel):
    root: List[AdminModel]


class AdminQueryModel(QueryModel):
    id: Optional[UUID] = None
    name: Optional[StrictStr] = None
    email: Optional[StrictStr] = None
