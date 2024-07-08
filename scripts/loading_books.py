import click

from scripts.loading_books_to_db.base import loading_books_to_db


@click.command()
@click.argument('src_filepath', type=click.Path(exists=True, file_okay=True))
def loading_books_to_db_cli(src_filepath: str) -> None:
    """Script for loading books suits from SRC_FILEPATH json file to database."""
    loading_books_to_db(src_filepath)
    click.echo(f"Books loaded from {src_filepath} to the database.")


if __name__ == '__main__':
    loading_books_to_db_cli()
