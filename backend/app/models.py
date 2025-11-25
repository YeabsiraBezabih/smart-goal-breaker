"""Database models for goals and tasks."""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Goal(Base):
    """Goal model representing a user's goal."""
    
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)  # Session-based user ID
    goal_text = Column(Text, nullable=False)
    complexity_score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to tasks
    tasks = relationship("Task", back_populates="goal", cascade="all, delete-orphan")


class Task(Base):
    """Task model representing actionable steps for a goal."""
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    task_text = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)  # 1-5 for the 5 steps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to goal
    goal = relationship("Goal", back_populates="tasks")
