from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.models import Book as BookModel


def _parse_date(date_str):
    formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_str}")


def get_book_or_404(db: Session, book_id: int):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


def validate_isbn_length(isbn: str):
    if len(isbn) > 13:
        raise HTTPException(status_code=400, detail="ISBN cannot exceed 13 characters")
