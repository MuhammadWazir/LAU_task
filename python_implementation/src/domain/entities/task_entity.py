from typing import Optional
from pydantic import BaseModel
from src.domain.enums.task_enums import TaskStatus
from uuid import UUID

class TaskEntity(BaseModel):
    task_id: Optional[UUID] = None
    title: Optional[str] = None
    status: Optional[TaskStatus] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None