import os
from typing import NoReturn

from scripts.loading_books_to_db.const import BookParam, Extension


def validate_file_extensions(src_filepath: str) -> NoReturn:
    """Validate file extensions should be `.json`

    Args:
        src_filepath: Path to source json file.

    """
    if os.path.splitext(src_filepath)[1] != Extension.JSON:
        raise ValueError(f'Invalid file extension. Expected {Extension.JSON}')


def validate_book_params(book_suits: list[dict]) -> NoReturn:
    """Validate book data and print missing or null fields if invalid.

    Args:
        book_suits: Suit of book with params.

    """
    errors = []

    for index, params in enumerate(book_suits, 1):
        missing_params = BookParam.get_fields() - set(params.keys())

        if missing_params:
            errors.append(f"Missing or unexpected fields for book number {index}: {', '.join(missing_params)}")

    if errors:
        raise ValueError("\n".join(errors))
