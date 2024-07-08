import click

from db.base import create_database


@click.group()
def cli():
    pass


@cli.command()
def create_db_cli():
    """Create database and table 'books'."""
    create_database()


if __name__ == '__main__':
    cli()
