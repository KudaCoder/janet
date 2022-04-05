from flask import Blueprint, render_template

bp = Blueprint("public", __name__)


@bp.route("/")
def home():
    context = {"page": "home"}
    return render_template("home.html", **context)


@bp.route("/about/")
def about():
    context = {"page": "about"}
    return render_template("about.html", **context)
