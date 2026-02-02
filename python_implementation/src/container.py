from dependency_injector import containers, providers
from src.infrastructure.database.config import SessionLocal
from src.infrastructure.database.repositories.tasks_repository import TaskRepository

class Container(containers.DeclarativeContainer):
    
    db = providers.Factory(SessionLocal)
    
    task_repository = providers.Singleton(
        TaskRepository,
        db=db
    )
    