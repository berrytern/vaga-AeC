import uuid
from sqlalchemy import Column, ForeignKey, DateTime, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base
from .reader_schema import ReaderSchema


class FavoriteBookSchema(Base):
    __tablename__ = "favorite_book"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    reader_id = Column(
        UUID(as_uuid=True), ForeignKey("reader.id", ondelete="CASCADE"), nullable=False
    )
    book_id = Column(
        UUID(as_uuid=True), ForeignKey("book.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

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


# Event listeners to update books_read_count
@event.listens_for(FavoriteBookSchema, "after_insert")
def increment_books_read_count(mapper, connection, target):
    connection.execute(
        ReaderSchema.__table__.update()
        .where(ReaderSchema.id == target.reader_id)
        .values(books_read_count=ReaderSchema.books_read_count + 1)
    )


@event.listens_for(FavoriteBookSchema, "after_delete")
def decrement_books_read_count(mapper, connection, target):
    connection.execute(
        ReaderSchema.__table__.update()
        .where(ReaderSchema.id == target.reader_id)
        .values(books_read_count=ReaderSchema.books_read_count - 1)
    )
