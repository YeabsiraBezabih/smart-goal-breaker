"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class GoalCreate(BaseModel):
    """Schema for creating a new goal."""
    goal_text: str = Field(..., min_length=1, max_length=500, description="The user's goal")


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: int
    task_text: str
    order: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class GoalResponse(BaseModel):
    """Schema for goal response with tasks."""
    id: int
    goal_text: str
    complexity_score: int
    created_at: datetime
    tasks: List[TaskResponse]
    
    class Config:
        from_attributes = True
