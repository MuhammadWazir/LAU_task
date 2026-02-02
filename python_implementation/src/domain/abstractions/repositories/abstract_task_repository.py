from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.task import TaskEntity

class AbstractTaskRepository(ABC):
    @abstractmethod
    def create(self, task: TaskEntity) -> TaskEntity:
        pass
    
    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[TaskEntity]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10) -> List[TaskEntity]:
        pass
    
    @abstractmethod
    def update(self, task: TaskEntity) -> Optional[TaskEntity]:
        pass
    
    @abstractmethod
    def delete(self, task_id: str) -> bool:
        pass