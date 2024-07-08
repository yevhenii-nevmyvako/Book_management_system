from datetime import date

from pydantic import BaseModel, validator, Field

from book_table.contrib import _parse_date


class Book(BaseModel):
    id: int
    title: str
    author: str
    published_date: date
    isbn: str
    pages: int

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str
    author: str
    published_date: date
    isbn: str = Field(..., max_length=13)
    pages: int

    @validator('published_date', pre=True)
    def parse_published_date(cls, value):
        return _parse_date(value)


class PaginatedBooks(BaseModel):
    total: int
    items: list[Book]
