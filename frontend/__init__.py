from flask import flash, redirect, url_for
from flask_login import LoginManager

from frontend.models import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauth_handler():
    flash("You must be logged in to view this page", "error")
    return redirect(url_for("public.login"))
