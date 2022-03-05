from flask import Flask

from .config import Config
from frontend.models import migrate, db
from frontend import blueprints


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(blueprints.public.bp)
app.register_blueprint(blueprints.habitat.bp)
