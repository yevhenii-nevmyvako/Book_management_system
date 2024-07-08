import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from book_table.books import router as books_router
from db.base import Base, engine

app = FastAPI()

templates = Jinja2Templates(directory="book_table/templates")

Base.metadata.create_all(bind=engine)

script_dir = os.path.dirname(__file__)
static_dir = os.path.join(script_dir, "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# app.mount("/static", StaticFiles(directory="./static"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(books_router, prefix="/books", tags=["books"])
