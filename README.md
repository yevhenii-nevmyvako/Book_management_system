# Book Management System with FastAPI

### Overview
This project implements a book management system using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+. It integrates SQLAlchemy for database operations and Jinja2 templates for rendering HTML pages.

### Features

* CRUD Operations: Endpoints for creating, reading, updating, and deleting books.
* Pagination: Handles pagination of book records.
* HTML Templates: Uses Jinja2 templates to render HTML responses.
* Static Files: Serves static files like CSS and images.

### API Endpoints
* GET /books/: Fetches a paginated list of books.
* GET /books/{book_id}: Fetches detailed information about a specific book.
* GET /books/create/new: Renders a form to create a new book.
* POST /books/: Creates a new book.
* GET /books/{book_id}/edit: Renders a form to edit an existing book.
* PUT /books/{book_id}/update: Updates an existing book.
* DELETE /books/{book_id}: Deletes a book by its ID.

### Technologies Used
* FastAPI: Web framework.
* SQLAlchemy: ORM for database operations.
* Jinja2: Template engine for rendering HTML.
* Python: Programming language.
* Click: For command line interface.
* Html: For structured web interface.
* Unit test for testing endpoints.
* Docker for containerization image application.
* Alembic for migrations.
* Sqlite3 for create book_table.
* Setuptools for setup the project.

### Installation
Clone repozitory by SSH key:
```bash
git clone git@github.com:yevhenii-nevmyvako/Book_management_system.git
```
Follow to project directory:
```bash
cd <project_directory>
```
Create environment:
```bash
python -m venv venv
```
Setup the project by setup tools:
```bash
pip install -e .
```
Create database & run migrations by alembic:
```bash
alembic upgrade head
```
Upload the data from fixture:
```bash
loading_books demo_and_test_data/books_data_fixture.json
```
Run the server:
```bash
uvicorn main:app --reload
```

### Install & Run by docker:
Create docker image:
```bash
docker build -t myapp .
```
Run docker image in container:
```bash
 docker run myapp:latest
```
Notes: in docker version all setup of application - automatically.
