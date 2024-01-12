from pydantic import BaseModel, Field

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