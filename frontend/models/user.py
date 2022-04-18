from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password_hash = db.Column(db.String(150))

    project = db.relationship(
        "Project",
        back_populates="creator",
    )
    task = db.relationship(
        "Task",
        back_populates="worker",
    )

    # For use in Janet not on website
    @staticmethod
    def current_user():
        return User.query.filter_by(is_active=True).first()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
