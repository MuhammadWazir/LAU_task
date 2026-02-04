from typing import Optional
from uuid import UUID
from src.domain.abstractions.repositories.abstract_task_repository import AbstractTaskRepository
from src.domain.entities.task_entity import TaskEntity
from src.domain.enums.task_enums import TaskStatus


class CompleteTaskUseCase:
    """Use case for marking a task as complete"""
    
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository
    
    def execute(self, task_id: UUID) -> Optional[TaskEntity]:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            return None
        
        if task.status == TaskStatus.DONE:
            return task
        
        # Update status to DONE
        task.status = TaskStatus.DONE
        return self.task_repository.update(task)
