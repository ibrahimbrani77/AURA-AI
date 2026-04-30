from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.database import Base

class User(Base):
    __tablename__ = "users"
    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String)
    email          = Column(String, unique=True, index=True)
    password_hash  = Column(String)
    preferences    = Column(Text, default="")
    face_embedding = Column(Text, nullable=True)
    created_at     = Column(DateTime, default=datetime.utcnow)
    tasks          = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String)
    description = Column(Text)
    status      = Column(String, default="pending")
    user_id     = Column(Integer, ForeignKey("users.id"))
    owner       = relationship("User", back_populates="tasks")

class Note(Base):
    __tablename__ = "notes"
    id      = Column(Integer, primary_key=True, index=True)
    title   = Column(String, nullable=True)
    content = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

class Reminder(Base):
    __tablename__ = "reminders"
    id       = Column(Integer, primary_key=True, index=True)
    title    = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=True)
    done     = Column(Integer, default=0)
    user_id  = Column(Integer, ForeignKey("users.id"))

class Personalization(Base):
    __tablename__ = "personalization"
    id      = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key     = Column(String, nullable=False)
    value   = Column(String, nullable=False)

