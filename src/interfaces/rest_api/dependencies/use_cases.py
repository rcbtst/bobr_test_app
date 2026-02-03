from typing import Annotated, TypeAlias

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from src.application.use_cases import CreateTaskUseCase
from src.infrastructure.di_config import ApplicationContainer


@inject
def get_create_task_use_case(
    create_task_use_case: CreateTaskUseCase = Depends(
        Provide[ApplicationContainer.create_task_use_case]
    ),
) -> CreateTaskUseCase:
    return create_task_use_case


CreateTaskUseCaseDep: TypeAlias = Annotated[
    CreateTaskUseCase,
    Depends(get_create_task_use_case),
]
