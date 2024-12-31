from typing import Optional, Dict, List, Any
from src.application.domain.models import (
    BookQueryModel,
    UpdateBookModel,
    CreateBookModel,
)
from src.infrastructure.repositories import BookRepository


class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def create(self, book: CreateBookModel) -> Dict[str, Any]:
        """
        Create a new book record

        Args:
            book (CreateBookModel): Book data to create

        Returns:
            Dict[str, Any]: Created book data
        """
        result = await self.repository.create(
            book.model_dump(
                exclude_none=True,
                exclude={"id"},
            )
        )
        return result

    async def get_one(self, book_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a single book by ID

        Args:
            book_id (str): ID of the book to retrieve

        Returns:
            Optional[Dict[str, Any]]: Book data if found, None otherwise
        """
        return await self.repository.get_one({"id": book_id})

    async def get_all(self, query: BookQueryModel) -> List[Dict[str, Any]]:
        """
        Get all books matching the query parameters

        Args:
            query (BookQueryModel): Query parameters for filtering books

        Returns:
            List[Dict[str, Any]]: List of matching books
        """
        return await self.repository.get_all(query)

    async def update_one(
        self, book_id: str, book: UpdateBookModel
    ) -> Optional[Dict[str, Any]]:
        """
        Update a book's information

        Args:
            book_id (str): ID of the book to update
            book (UpdateBookModel): Updated book data

        Returns:
            Optional[Dict[str, Any]]: Updated book data if successful, None otherwise
        """
        return await self.repository.update_one(
            book_id, book.model_dump(exclude_none=True)
        )

    async def delete_one(self, book_id: str) -> None:
        """
        Delete a book by ID

        Args:
            book_id (str): ID of the book to delete
        """
        await self.repository.delete_one(book_id)
