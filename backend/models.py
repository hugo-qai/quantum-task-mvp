from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from database import Base
import datetime
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    ai_preferences = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    raw_nlp_input = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority_score = Column(Integer, default=0)
    status = Column(String, default="TODO") # TODO, IN_PROGRESS, DONE
    smart_tags = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="tasks")
