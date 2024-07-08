import json
from datetime import datetime

from db.base import create_session
from db.models import Book
from scripts.loading_books_to_db.const import DATE, BookParam
from scripts.loading_books_to_db.validate import validate_book_params, validate_file_extensions


# TODO: If we connecting postgre change to on_conflict_do_nothing.

def _load_books_to_db(books_data: list[dict]) -> None:
    """Loads books into the SQLite database, avoiding duplicate IDs."""
    with create_session() as session:
        for book_data in books_data:
            existing_book = session.query(Book).filter_by(id=book_data[BookParam.ID]).first()
            if not existing_book:
                book = Book(
                    id=book_data[BookParam.ID],
                    title=book_data[BookParam.TITLE],
                    author=book_data[BookParam.AUTHOR],
                    published_date=datetime.strptime(book_data[BookParam.PUBLISHED_DATE], DATE),
                    isbn=book_data[BookParam.ISBN],
                    pages=book_data[BookParam.PAGES]
                )
                session.add(book)
        session.commit()


def _get_data_from_json(src_filepath: str) -> list[dict]:
    """Gets data from json file.

    Args:
        src_filepath: Path to source json file.

    Return:
        data: Data from json file.

    """
    with open(src_filepath, 'r') as json_file:
        data = json.load(json_file)
        return data


def loading_books_to_db(src_filepath: str) -> None:
    """Validate and loading data to database.

    Args:
        src_filepath: Path to source file.

    """
    validate_file_extensions(src_filepath)
    books_data = _get_data_from_json(src_filepath)
    validate_book_params(books_data)
    _load_books_to_db(books_data)
