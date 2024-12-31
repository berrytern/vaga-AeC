import uuid
from sqlalchemy import Column, String, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, TEXT, DOUBLE_PRECISION
from sqlalchemy.sql import func

from . import Base


class BookSchema(Base):
    __tablename__ = "book"

    __table_args__ = (UniqueConstraint("title", "author", name="uq_title_author"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(60), nullable=False)
    description = Column(TEXT, nullable=False)
    author = Column(String(60), nullable=False)
    price = Column(DOUBLE_PRECISION, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return (
            '{"id": "'
            + str(self.id)
            + '", "title": "'
            + str(self.title)
            + '", "description": "'
            + str(self.description)
            + '", "author": "'
            + str(self.author)
            + '", "created_at": "'
            + str(self.created_at)
            + '", "updated_at": "'
            + str(self.updated_at)
            + '"}'
        )
