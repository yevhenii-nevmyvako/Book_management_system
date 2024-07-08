FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN pip install -e .

RUN alembic upgrade head

RUN loading_books demo_and_test_data/books_data_fixture.json

CMD ["uvicorn", "main:app", "--reload"]
