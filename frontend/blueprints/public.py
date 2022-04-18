from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user

from frontend.forms import LoginForm, RegisterForm
from frontend.models import db, User

bp = Blueprint("public", __name__)


@bp.route("/")
def home():
    context = {"page": "home"}
    return render_template("home.html", **context)


@bp.route("/about")
def about():
    context = {"page": "about"}
    return render_template("about.html", **context)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("public.home"))

    return render_template("login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("public.login"))

    return render_template("register.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("public.home"))
