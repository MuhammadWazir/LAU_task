from src.domain.abstractions.repositories.abstract_task_repository import AbstractTaskRepository
from src.domain.entities.task_entity import TaskEntity
from src.domain.enums.task_enums import TaskStatus
from src.application.dtos.task_dtos import CreateTaskRequest


class CreateTaskUseCase:
    """Use case for creating a new task"""
    
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository
    
    def execute(self, request: CreateTaskRequest) -> TaskEntity:
        task_entity = TaskEntity(
            title=request.title,
            status=TaskStatus.OPEN
        )
        return self.task_repository.create(task_entity)
