from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import mapped_column, Mapped

from db.base import Base


int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class Book(Base):
    """Represents a book in the library.

    Args:
        id (int): The unique identifier for the book.
        title (str): The title of the book.
        author (str): The author of the book.
        published_date (datetime): The date when the book was published.
        isbn (str): The International Standard Book Number of the book.
        pages (int): The number of pages in the book.

    """
    __tablename__ = 'books'
    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(index=True)
    author: Mapped[str]
    published_date: Mapped[datetime]
    isbn: Mapped[str]
    pages: Mapped[int]
