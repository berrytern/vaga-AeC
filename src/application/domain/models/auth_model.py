from typing import Optional
from pydantic import (
    BaseModel,
    Field,
    StrictStr,
    EmailStr,
)
from uuid import UUID
from datetime import datetime


class AuthModel(BaseModel):
    id: Optional[UUID] = None
    username: Optional[StrictStr] = None
    email: EmailStr = Field(..., min_length=10, max_length=250)
    user_type: Optional[StrictStr] = None
    password: Optional[StrictStr] = None
    refresh_token: Optional[StrictStr] = None
    last_login: Optional[datetime] = Field(
        default_factory=lambda: datetime.now().replace(microsecond=0)
    )
    foreign_id: Optional[UUID] = None
