from typing import Any
from pydantic import BaseModel


class CeleryTask(BaseModel):
    worker: str
    task_id: str | None = None
    task_name: str | None = None
    args: Any = None
    kwargs: Any = None
    time_start: float | None = None


class CeleryTaskGroup(BaseModel):
    count: int
    tasks: list[CeleryTask]


class CeleryStatusResponse(BaseModel):
    active: CeleryTaskGroup
    pending: CeleryTaskGroup
    scheduled: CeleryTaskGroup