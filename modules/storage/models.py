from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(10), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=False)

    jobs = relationship("Job")
    client = relationship("Client")

    def save(self, db):
        db.add(self)
        db.commit()


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    jobs = relationship("Job")
    projects = relationship("Project")

    def save(self, db):
        db.add(self)
        db.commit()


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    is_active = Column(Boolean, default=False)

    jobs = relationship("Job")

    def save(self, db):
        db.add(self)
        db.commit()


class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    start_time = Column(String, nullable=True)
    end_time = Column(String, nullable=True)
    hours = Column(Float(4, 1), default=0.0)
    is_active = Column(Boolean, default=False)

    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)

    def save(self, db):
        db.add(self)
        db.commit()
