import uuid
from sqlalchemy import Column, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base


class FavoriteBookSchema(Base):
    __tablename__ = "favorite_book"

    __table_args__ = (
        UniqueConstraint("reader_id", "book_id", name="uq_reader_favorite_book"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    reader_id = Column(
        UUID(as_uuid=True), ForeignKey("reader.id", ondelete="CASCADE"), nullable=False
    )
    book_id = Column(
        UUID(as_uuid=True), ForeignKey("book.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    reader = relationship("ReaderSchema", backref="favorite_books")
    book = relationship("BookSchema")

    def __repr__(self) -> str:
        return (
            '{"id": "'
            + str(self.id)
            + '", "reader_id": "'
            + str(self.reader_id)
            + '", "book_id": "'
            + str(self.book_id)
            + '", "created_at": "'
            + str(self.created_at)
            + '", "updated_at": "'
            + str(self.updated_at)
            + '"}'
        )
