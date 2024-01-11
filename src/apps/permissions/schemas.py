from pydantic import BaseModel, Field
from enum import Enum


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


class PermissionGroup(BaseModel):
    name: str = Field(
        title="Nome do grupo de permissão",
        description="Grupo de permissão onde um usuário poderá participar e cada usuário poderá participar de vários grupos.",
        default=""
    )


class PermissionGroupBase(PermissionGroup):
    id: int = Field(
        title="ID",
        description="Esse valor deverá ser referenciado por uma permissão, assim haverá uma relação entre permissão e grupo de permissões.",
    )


class PermissionAndGroupRelation(BaseModel):
    permission_id: int = 0
    permission_group_id: int = 0


class UserAndGroupRelation(BaseModel):
    user_id: int = 0
    permission_group_id: int = 0
