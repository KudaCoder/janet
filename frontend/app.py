from frontend import blueprints, models
from frontend import assets, jinja
from .config import Config
from . import login_manager

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    models.init_app(app)
    assets.init_app(app)
    jinja.init_app(app)

    login_manager.init_app(app)

    app.register_blueprint(blueprints.public.bp)
    app.register_blueprint(blueprints.habitat.bp)

    return app
