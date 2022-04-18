from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)


from .user import User  # noqa
from .work import Client, Project, Task  # noqa
from .utils import WorkUtils, UserUtils  # noqa
