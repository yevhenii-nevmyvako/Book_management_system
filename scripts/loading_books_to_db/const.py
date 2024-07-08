DATE = '%Y-%m-%d'


class EnumClass:
    @classmethod
    def get_fields(cls):
        """Gets list <classes>Enum fields."""
        return {
            getattr(cls, attr) for attr in dir(cls) if
            not attr.startswith("__") and not callable(getattr(cls, attr))
        }


class Extension(EnumClass):
    JSON = '.json'


class BookParam(EnumClass):
    """Name of book params in the library."""
    ID = 'id'
    TITLE = 'title'
    AUTHOR = 'author'
    PUBLISHED_DATE = 'published_date'
    ISBN = 'isbn'
    PAGES = 'pages'

