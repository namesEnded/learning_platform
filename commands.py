import click
from database import db
from models import Course


def create_db():
    """ Creates a database """
    db.create_all()


def drop_db():
    """ Deletes data from the database """
    db.drop_all()


def create_tables():
    """ Creates all tables for all models """
    Course.__table__.create(db.engine)


def start_app(app):
    for command in [create_db, drop_db, create_tables]:
        app.cli.add_command(app.cli.command()(command))
