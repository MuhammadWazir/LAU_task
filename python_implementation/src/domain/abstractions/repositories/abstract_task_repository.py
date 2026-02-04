from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from src.domain.entities.task_entity import TaskEntity
from src.domain.enums.task_enums import TaskStatus
from src.config.constants import limit_default, offset_default

class AbstractTaskRepository(ABC):
    @abstractmethod
    def create(self, task: TaskEntity) -> TaskEntity:
        pass
    
    @abstractmethod
    def get_by_id(self, task_id: UUID) -> Optional[TaskEntity]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = offset_default, limit: int = limit_default, status: Optional[TaskStatus] = None) -> List[TaskEntity]:
        pass
    
    @abstractmethod
    def count(self, status: Optional[TaskStatus] = None) -> int:
        pass
    
    @abstractmethod
    def update(self, task: TaskEntity) -> Optional[TaskEntity]:
        pass
    
    @abstractmethod
    def delete(self, task_id: UUID) -> bool:
        pass