from typing import Optional
from uuid import UUID
from src.domain.abstractions.repositories.abstract_task_repository import AbstractTaskRepository
from src.domain.entities.task_entity import TaskEntity


class GetTaskByIdUseCase:
    """Use case for retrieving a task by ID"""
    
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository
    
    def execute(self, task_id: UUID) -> Optional[TaskEntity]:
        return self.task_repository.get_by_id(task_id)
