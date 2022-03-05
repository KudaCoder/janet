from . import db


class Client(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=False)

    project = db.relationship(
        "Project",
        back_populates="client",
    )

    @staticmethod
    def find(**kwargs):
        if kwargs.get("name"):
            return Client.query.filter_by(name=kwargs.get("name")).first()

        if kwargs.get("is_active"):
            return Client.query.filter_by(is_active=True).first()


class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=False)

    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    client = db.relationship("Client", back_populates="project")

    task = db.relationship("Task", back_populates="project")

    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    creator = db.relationship("User", back_populates="project")

    @staticmethod
    def find(**kwargs):
        if kwargs.get("name"):
            return Project.query.filter_by(kwargs.get("name")).first()

        if kwargs.get("is_active"):
            return Project.query.filter_by(is_active=True).first()


class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=False)

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    project = db.relationship(
        "Project",
        back_populates="task",
    )

    worker_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    worker = db.relationship("User", back_populates="task")

    @staticmethod
    def find(**kwargs):
        if kwargs.get("title"):
            return Task.query.filter_by(kwargs.get("title")).first()

        if kwargs.get("is_active"):
            return Task.query.filter_by(is_active=True).first()

    @property
    def total_hours(self):
        if not self.start_time or not self.end_time:
            return 0.0

        return float((self.end_time - self.start_time).total_seconds() / 3600, 2)
