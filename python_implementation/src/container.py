from dependency_injector import containers, providers
from src.infrastructure.database.config import SessionLocal
from src.infrastructure.database.repositories.tasks_repository import TaskRepository
from src.application.use_cases.tasks.create_task_use_case import CreateTaskUseCase
from src.application.use_cases.tasks.get_task_by_id_use_case import GetTaskByIdUseCase
from src.application.use_cases.tasks.list_tasks_use_case import ListTasksUseCase
from src.application.use_cases.tasks.complete_task_use_case import CompleteTaskUseCase
from src.application.use_cases.tasks.delete_task_use_case import DeleteTaskUseCase

from src.infrastructure.cache.redis_cache import RedisCache
from src.config.config import get_settings

class Container(containers.DeclarativeContainer):
    
    settings = providers.Singleton(get_settings)
    
    db = providers.Factory(SessionLocal)
    
    cache = providers.Singleton(
        RedisCache,
        host=settings().REDIS_HOST,
        port=settings().REDIS_PORT
    )
    
    task_repository = providers.Factory(
        TaskRepository,
        db=db
    )
    
    # Use Cases
    create_task_use_case = providers.Factory(
        CreateTaskUseCase,
        task_repository=task_repository
    )
    
    get_task_by_id_use_case = providers.Factory(
        GetTaskByIdUseCase,
        task_repository=task_repository
    )
    
    list_tasks_use_case = providers.Factory(
        ListTasksUseCase,
        task_repository=task_repository
    )
    
    complete_task_use_case = providers.Factory(
        CompleteTaskUseCase,
        task_repository=task_repository
    )
    
    delete_task_use_case = providers.Factory(
        DeleteTaskUseCase,
        task_repository=task_repository
    )