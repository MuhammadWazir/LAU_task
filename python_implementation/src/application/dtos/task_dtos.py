from pydantic import BaseModel, Field, field_validator, field_serializer, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID   
from src.domain.enums.task_enums import TaskStatus


class CreateTaskRequest(BaseModel):
    """Request DTO for creating a new task"""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()


class TaskResponse(BaseModel):
    """Response DTO for task data"""
    model_config = ConfigDict(from_attributes=True)
    
    task_id: UUID
    title: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    """Response DTO for list of tasks"""
    tasks: list[TaskResponse]
    total: int
    limit: int
    offset: int
