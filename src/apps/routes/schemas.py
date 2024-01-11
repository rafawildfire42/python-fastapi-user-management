from pydantic import BaseModel, Field


class RouteBase(BaseModel):
    """
    Esquema com propósito de descrever saídas e entradas de rotas.
    A rota só poderá ser acessada se ela for cadastrada no banco.
    """
    path: str = Field(title="Caminho", default="",
                      description="Caminho da rota.")
    needs_permission: bool = Field(
        title="Precisa de permissão?",
        description="Caso este valor seja falso significa que qualquer usuário poderá utilizar qualquer método nesta rota, evitando que a aplicação realize um processo mais custoso de verificação de permissionamento.",
        default=False
    )


class Route(RouteBase):
    id: int = Field(
        title="ID", description="Identificador da instância de Route.")
