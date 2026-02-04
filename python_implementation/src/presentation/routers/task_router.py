from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import Optional
from uuid import UUID
from dependency_injector.wiring import inject, Provide

from src.application.dtos.task_dtos import CreateTaskRequest, TaskResponse, TaskListResponse
from src.application.use_cases.tasks.create_task_use_case import CreateTaskUseCase
from src.application.use_cases.tasks.get_task_by_id_use_case import GetTaskByIdUseCase
from src.application.use_cases.tasks.list_tasks_use_case import ListTasksUseCase
from src.application.use_cases.tasks.complete_task_use_case import CompleteTaskUseCase
from src.application.use_cases.tasks.delete_task_use_case import DeleteTaskUseCase
from src.domain.enums.task_enums import TaskStatus
from src.container import Container
from src.config.constants import limit_cap, limit_default, offset_default
from src.domain.abstractions.cache.abstract_redis_cache import AbstractRedisCache

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Creates a new task with status OPEN"
)
@inject
def create_task(
    request: CreateTaskRequest,
    use_case: CreateTaskUseCase = Depends(Provide[Container.create_task_use_case]),
    cache: AbstractRedisCache = Depends(Provide[Container.cache])
) -> TaskResponse:
    try:
        task = use_case.execute(request)
        cache.invalidate_pattern("tasks:*")
        return TaskResponse.model_validate(task)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create task: {str(e)}"
        )


@router.get(
    "",
    response_model=TaskListResponse,
    summary="List tasks",
    description="List tasks with optional filtering and pagination"
)
@inject
def list_tasks(
    status_filter: Optional[TaskStatus] = Query(None, alias="status", description="Filter by task status"),
    limit: int = Query(limit_default, ge=1, le=limit_cap, description="Number of tasks to return (max 200)"),
    offset: int = Query(offset_default, ge=0, description="Number of tasks to skip"),
    use_case: ListTasksUseCase = Depends(Provide[Container.list_tasks_use_case]),
    cache: AbstractRedisCache = Depends(Provide[Container.cache])
) -> TaskListResponse:
    try:
        cache_key = f"tasks:list:status={status_filter}:limit={limit}:offset={offset}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return TaskListResponse.model_validate(cached_data)

        tasks, total = use_case.execute(
            status=status_filter,
            limit=limit,
            offset=offset
        )
        
        response = TaskListResponse(
            tasks=[TaskResponse.model_validate(task) for task in tasks],
            total=total,
            limit=limit,
            offset=offset
        )
        
        cache.set(cache_key, response.model_dump(mode='json'), ttl=10)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to list tasks: {str(e)}"
        )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
    description="Retrieve a specific task by its ID"
)
@inject
def get_task(
    task_id: UUID,
    use_case: GetTaskByIdUseCase = Depends(Provide[Container.get_task_by_id_use_case])
) -> TaskResponse:
    task = use_case.execute(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    return TaskResponse.model_validate(task)


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
    summary="Mark task as complete",
    description="Mark a task as DONE (idempotent)"
)
@inject
def complete_task(
    task_id: UUID,
    use_case: CompleteTaskUseCase = Depends(Provide[Container.complete_task_use_case]),
    cache: AbstractRedisCache = Depends(Provide[Container.cache])
) -> TaskResponse:
    task = use_case.execute(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    cache.invalidate_pattern("tasks:*")
    return TaskResponse.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete a task by ID"
)
@inject
def delete_task(
    task_id: UUID,
    use_case: DeleteTaskUseCase = Depends(Provide[Container.delete_task_use_case]),
    cache: AbstractRedisCache = Depends(Provide[Container.cache])
) -> None:
    success = use_case.execute(task_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    cache.invalidate_pattern("tasks:*")
