from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from frontend.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


def init_app(app):
    db.init_app(db)
    migrate.init_app(app, db)


from .user import User
from .work import Client, Project, Task
from .utils import WorkUtils, UserUtils
