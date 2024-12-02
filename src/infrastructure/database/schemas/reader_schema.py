import uuid
from sqlalchemy import Column, String, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from . import Base


class ReaderSchema(Base):
    __tablename__ = "reader"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(60))
    email = Column(String, unique=True)
    birthday = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return (
            '{"id": "'
            + str(self.id)
            + '", "name": "'
            + str(self.name)
            + '", "email": "'
            + str(self.email)
            + '", "birthday": "'
            + str(self.birthday)
            + '", "created_at": "'
            + str(self.created_at)
            + '", "updated_at": "'
            + str(self.updated_at)
            + '"}'
        )