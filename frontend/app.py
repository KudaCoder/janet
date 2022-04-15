from frontend.models import migrate, db
from frontend import blueprints
from .config import Config
from .assets import assets

from flask import Flask


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(blueprints.public.bp)
app.register_blueprint(blueprints.habitat.bp)

assets.init_app(app)


@app.template_filter()
def pretty_dt(value):
    day = value.day
    return value.strftime("{D} %B, %Y @ %H:%M").replace(
        "{D}", str(day) + ordinal_suffix(day)
    )


def ordinal_suffix(number):
    if number % 10 == 1 and number != 11:
        return "st"
    elif number % 10 == 2 and number != 12:
        return "nd"
    elif number % 10 == 3 and number != 13:
        return "rd"
    else:
        return "th"
