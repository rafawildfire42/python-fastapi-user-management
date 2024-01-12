from enum import Enum
from pydantic import BaseModel, Field


class Action(Enum):
    create = "create"
    delete = "delete"
    view = "view"
    update = "update"


class PermissionBase(BaseModel):
    route_id: int = Field(
        title="ID da Rota", description="Rota (endpoint) relacionado à permissão.",
        default=0
    )
    action: Action = Field(
        title="Ação",
        description="Permissão que se relaciona uma rota e diz o que é permitido fazer nela com esta permissão.",
        default=""
    )


class Permission(PermissionBase):
    id: int = Field(
        title="ID",
        description="Identificador de uma instância de permissão",
        default=0
    )
