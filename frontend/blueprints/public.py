from flask import Blueprint, render_template

from .utils import APITools

bp = Blueprint("public", __name__)
api_tools = APITools()


@bp.route("/")
def home():
    reading = api_tools.current_reading()

    context = {
        "reading": reading,
        "page": "home",
    }

    return render_template("home.html", **context)


@bp.route("/about/")
def about():
    context = {"page": "about"}

    return render_template("about.html", **context)
