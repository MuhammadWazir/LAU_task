from typing import Optional
from src.domain.abstractions.repositories.abstract_task_repository import AbstractTaskRepository
from src.domain.entities.task_entity import TaskEntity
from src.domain.enums.task_enums import TaskStatus
from src.config.constants import limit_cap, limit_default, offset_default


class ListTasksUseCase:
    """Use case for listing tasks with optional filtering"""
    
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository
    
    def execute(
        self, 
        status: Optional[TaskStatus] = None,
        limit: int = limit_default,
        offset: int = offset_default
    ) -> tuple[list[TaskEntity], int]:
        # Validate and cap limit
        if limit > limit_cap:
            limit = limit_cap
        if limit < 1:
            limit = limit_default
        
        # Validate offset
        if offset < 0:
            offset = offset_default
        
        # Get tasks (repository will handle filtering if needed)
        tasks = self.task_repository.get_all(skip=offset, limit=limit, status=status)
        
        # Get total count for the filter
        total = self.task_repository.count(status=status)
        
        return tasks, total
