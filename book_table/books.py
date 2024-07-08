from fastapi import APIRouter, Query, Request, HTTPException, Form

from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates

from book_table.contrib import _parse_date, get_book_or_404, validate_isbn_length
from book_table.schemas import Book as BookSchema, BookCreate
from db.base import create_session
from db.models import Book as BookModel

router = APIRouter()
templates = Jinja2Templates(directory="book_table/templates")


@router.get("/", response_class=HTMLResponse)
async def get_books_list(
        request: Request, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)
) -> templates.TemplateResponse:
    """Fetch a paginated list of books.

    Args:
        request (Request): The request object.
        skip (int): The number of records to skip. Must be greater than or equal to 0.
        limit (int): The number of records to return. Must be between 1 and 50.

    Returns:
        HTMLResponse: An HTML response with the list of books.

    """
    with create_session() as db:
        total = db.query(BookModel).count()
        books = db.query(BookModel).offset(skip).limit(limit).all()
        more_books = db.query(BookModel).offset(skip + limit).first() is not None
        next_skip = skip + limit if more_books else None
        return templates.TemplateResponse("books.html", {
            "request": request,
            "books": books,
            "more_books": more_books,
            "next_skip": next_skip,
            "limit": limit,
            "total": total,
            "skip": skip,
        })


@router.get("/{book_id}", response_model=BookSchema)
async def get_book_detail(request: Request, book_id: int) -> templates.TemplateResponse:
    """Fetch detailed information about a specific book by its ID.

    Args:
        request (Request): The request object.
        book_id (int): The ID of the book to retrieve.

    Returns:
        HTMLResponse: An HTML response with the book details.

    """
    with create_session() as db:
        book = get_book_or_404(db, book_id)
        return templates.TemplateResponse("book_detail.html", {"request": request, "book": book})


@router.get("/create/new", response_class=HTMLResponse)
async def create_book_form(request: Request) -> templates.TemplateResponse:
    """Render a form to create a new book.

    Args:
        request (Request): The request object.

    Returns:
        HTMLResponse: An HTML response with the book creation form.

    """
    return templates.TemplateResponse("create_book.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def create_book(
        request: Request, title: str = Form(...), author: str = Form(...),
        published_date: str = Form(...), isbn: str = Form(...), pages: int = Form(...)
) -> templates.TemplateResponse:
    """Create a new book.

    Args:
        request (Request): The request object.
        title (str): The title of the book.
        author (str): The author of the book.
        published_date (str): The published date of the book.
        isbn (str): The ISBN of the book.
        pages (int): The number of pages in the book.

    Returns:
        HTMLResponse: An HTML response with the created book's details.

    Raises:
        HTTPException: If there is a validation error with the provided data.

    """
    validate_isbn_length(isbn)
    with create_session() as db:
        try:
            book_create = BookCreate(title=title, author=author, published_date=published_date, isbn=isbn, pages=pages)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        book = BookModel(
            title=book_create.title,
            author=book_create.author,
            published_date=book_create.published_date,
            isbn=book_create.isbn,
            pages=book_create.pages
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        return templates.TemplateResponse("book_detail.html", {"request": request, "book": book})


@router.get("/{book_id}/edit", response_class=HTMLResponse)
async def edit_book_form(request: Request, book_id: int) -> templates.TemplateResponse:
    """Render a form to edit an existing book.

    Args:
        request (Request): The request object.
        book_id (int): The ID of the book to edit.

    Returns:
        HTMLResponse: An HTML response with the book edit form.

    Raises:
        HTTPException: If the book with the specified ID does not exist.

    """
    with create_session() as db:
        book = get_book_or_404(db, book_id)
        return templates.TemplateResponse("book_update.html", {"request": request, "book": book})


@router.put("/{book_id}/update", response_class=HTMLResponse)
async def update_book(
        request: Request, book_id: int, title: str = Form(...), author: str = Form(...),
        published_date: str = Form(...), isbn: str = Form(...), pages: int = Form(...)
) -> templates.TemplateResponse:
    """Update an existing book.

    Args:
        request (Request): The request object.
        book_id (int): The ID of the book to update.
        title (str): The title of the book.
        author (str): The author of the book.
        published_date (str): The published date of the book.
        isbn (str): The ISBN of the book.
        pages (int): The number of pages in the book.

    Returns:
        HTMLResponse: An HTML response with the updated book's details.

    Raises:
        HTTPException: If the book with the specified ID does not exist.

    """
    with create_session() as db:
        book = get_book_or_404(db, book_id)
        validate_isbn_length(isbn)

        book.title = title
        book.author = author
        book.published_date = _parse_date(published_date)
        book.isbn = isbn
        book.pages = pages

        db.commit()
        return templates.TemplateResponse("book_detail.html", {"request": request, "book": book})


@router.delete("/{book_id}", response_class=JSONResponse)
def delete_book(book_id: int) -> dict:
    """Delete a book by its ID.

    Args:
        book_id (int): The ID of the book to delete.

    Returns:
        JSONResponse: A JSON response confirming the deletion.

    Raises:
        HTTPException: If the book with the specified ID does not exist.

    """
    with create_session() as db:
        book = get_book_or_404(db, book_id)
        db.delete(book)
        db.commit()
        return {"message": "Book deleted successfully"}
