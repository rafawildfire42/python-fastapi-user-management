from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr = Field(
        title="Email do usuário",
        default="",
        description="Email do usuário.",
    )


class UserCreate(UserBase):
    password: str = Field(
        title="Senha",
        description="A senha do usuário deve conter pelo menos 6 caracteres.",
        min_length=6,
    )


class User(UserBase):
    id: int = Field(
        title="ID do usuário",
        default=0,
        description="O ID de um usuário é único e recebe um valor sequencial em uma unidade a cada usuário criado.",
    )
    is_active: bool = Field(
        title="Usuário ativo?",
        default=False,
        description="Este parâmetro decide se o usuário quer manter ou não sua conta ativa/visível na plataforma.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{"email": "rafa123@mail.com", "id": 3, "is_active": True}]
        }
    }
