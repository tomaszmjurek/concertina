import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                    'postgresql://localhost/concertina'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


db = SQLAlchemy()
migrate = Migrate()


def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
