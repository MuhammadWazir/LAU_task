from sqlalchemy.orm import Session
from typing import Optional, List

from src.domain.abstractions.repositories.abstract_task_repository import AbstractTaskRepository
from src.domain.entities.task_entity import TaskEntity
from src.domain.enums.task_enums import TaskStatus
from src.infrastructure.database.models.task import Task
from src.config.constants import limit_default, offset_default

class TaskRepository(AbstractTaskRepository):
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: TaskEntity) -> TaskEntity:
        db_task = Task(
            title=task.title
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_by_id(self, task_id: str) -> Optional[TaskEntity]:
        task = self.db.query(Task).filter(Task.task_id == task_id).first()
        return task

    def get_all(
        self, 
        skip: int = offset_default, 
        limit: int = limit_default,
        status: Optional[TaskStatus] = None
    ) -> List[TaskEntity]:
        query = self.db.query(Task)
        
        # Apply status filter if provided
        if status is not None:
            query = query.filter(Task.status == status)
        
        return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
    
    def count(self, status: Optional[TaskStatus] = None) -> int:
        """Count tasks with optional status filter"""
        query = self.db.query(Task)
        
        if status is not None:
            query = query.filter(Task.status == status)
        
        return query.count()

    def update(self, task: TaskEntity) -> Optional[TaskEntity]:
        db_task = self.get_by_id(task.task_id)
        if not db_task:
            return None
        db_task.status = task.status
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete(self, task_id: str) -> bool:
        db_task = self.get_by_id(task_id)
        if not db_task:
            return False
        self.db.delete(db_task)
        self.db.commit()
        return True