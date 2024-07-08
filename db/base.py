import os
from contextlib import contextmanager
from dataclasses import dataclass

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = 'sqlite:///./books.db'
DATABASE_FILE = './books.db'


class Base(DeclarativeBase):
    pass


@dataclass
class Config:
    """Gets the URL object for the database."""
    driver_name: str = "sqlite"
    database: str = os.environ.get('DATABASE_URL', f'{DATABASE_FILE}')

    def get_url_object(self):
        """Gets objects url"""
        return URL.create(
            drivername=self.driver_name,
            database=self.database,
        )


engine = create_engine(Config().get_url_object(), echo=True)


def create_database():
    Base.metadata.create_all(engine)
    print(f"Database '{DATABASE_FILE}' and table 'books' created successfully.")


@contextmanager
def create_session():
    """Context manager for creating a session."""
    session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
