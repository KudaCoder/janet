from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from . import Base
from .models import User, Client, Project, Job

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
USERNAME = os.environ.get("USERNAME")


class Database:
    def __init__(self):
        self.Base = Base
        self.engine = create_engine("sqlite:///conf/janet.db", echo=False)
        self.Base.metadata.create_all(bind=self.engine)
        self.db = None

    def open_session(self):
        """
        TODO - Add functionality for multiple users
               Voice recognition??
        """
        SessionLocal = sessionmaker(bind=self.engine)
        self.db = SessionLocal()

        self.user = self.db.query(User).filter_by(username=USERNAME).first()
        if self.user is None:
            new_user = User()
            new_user.username = USERNAME
            new_user.save(self.db)
            self.user = self.db.query(User).filter_by(username=USERNAME).first()
            self.user.is_active = True
            self.user.save(self.db)

        return self.db, self.user

    def return_active(self):
        client = None
        project = None
        job = None

        client = self.db.query(Client).filter_by(is_active=True).first()
        project = self.db.query(Project).filter_by(is_active=True).first()
        job = self.db.query(Job).filter_by(is_active=True).first()

        return client, project, job

    def close_session(self):
        self.db.close()
