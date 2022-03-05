from . import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, nullable=False, default=False)

    project = db.relationship(
        "Project",
        back_populates="creator",
    )
    task = db.relationship(
        "Task",
        back_populates="worker",
    )

    @staticmethod
    def current_user():
        return User.query.filter_by(is_active=True).first()
