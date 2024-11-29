from typing import Optional
from pydantic import BaseModel, StrictStr, Field
from uuid import UUID
from datetime import datetime


class AuthModel(BaseModel):

    id: Optional[UUID] = None
    username: StrictStr
    user_type: StrictStr
    password: StrictStr
    refresh_token: Optional[StrictStr] = None
    last_login: Optional[datetime] = Field(
        default_factory=lambda: datetime.now().replace(microsecond=0)
    )
    foreign_id: UUID
