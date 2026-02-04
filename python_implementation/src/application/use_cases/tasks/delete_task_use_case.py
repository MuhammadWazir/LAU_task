from uuid import UUID
from src.domain.abstractions.repositories.abstract_task_repository import AbstractTaskRepository


class DeleteTaskUseCase:
    """Use case for deleting a task"""
    
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository
    
    def execute(self, task_id: UUID) -> bool:
        return self.task_repository.delete(task_id)
