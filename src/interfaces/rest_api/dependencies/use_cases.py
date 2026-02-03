from typing import Annotated, TypeAlias

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from src.application.use_cases import CreateTaskUseCase, GetTaskUseCase
from src.infrastructure.di_config import ApplicationContainer


@inject
def get_create_task_use_case(
    create_task_use_case: CreateTaskUseCase = Depends(
        Provide[ApplicationContainer.create_task_use_case]
    ),
) -> CreateTaskUseCase:
    return create_task_use_case


@inject
def get_get_task_use_case(
    get_task_use_case: GetTaskUseCase = Depends(
        Provide[ApplicationContainer.get_task_use_case]
    ),
) -> GetTaskUseCase:
    return get_task_use_case


CreateTaskUseCaseDep: TypeAlias = Annotated[
    CreateTaskUseCase,
    Depends(get_create_task_use_case),
]


GetTaskUseCaseDep: TypeAlias = Annotated[
    GetTaskUseCase,
    Depends(get_get_task_use_case),
]
