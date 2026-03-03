"""Pydantic-модели для валидации данных пользователя.

Модели описывают структуру JSON-данных для операций с пользователями:
- Создание пользователя
- Получение данных пользователя
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CreateUserRequestSchema(BaseModel):
    """Модель запроса на создание пользователя.

    Attributes:
        email: Электронная почта пользователя.
        last_name: Фамилия пользователя.
        first_name: Имя пользователя.
        middle_name: Отчество пользователя.
        phone_number: Номер телефона пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr = Field(description="Электронная почта пользователя")
    last_name: str = Field(alias='lastName', description="Фамилия пользователя")
    first_name: str = Field(alias='firstName', description="Имя пользователя")
    middle_name: str = Field(alias='middleName', description="Отчество пользователя")
    phone_number: str = Field(alias='phoneNumber', description="Номер телефона пользователя")


class UserSchema(BaseModel):
    """Модель пользователя.

    Attributes:
        id: Уникальный идентификатор пользователя.
        email: Электронная почта пользователя.
        last_name: Фамилия пользователя.
        first_name: Имя пользователя.
        middle_name: Отчество пользователя.
        phone_number: Номер телефона пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="Уникальный идентификатор пользователя")
    email: EmailStr = Field(description="Электронная почта пользователя")
    last_name: str = Field(alias='lastName', description="Фамилия пользователя")
    first_name: str = Field(alias='firstName', description="Имя пользователя")
    middle_name: str = Field(alias='middleName', description="Отчество пользователя")
    phone_number: str = Field(alias='phoneNumber', description="Номер телефона пользователя")


class GetUserResponseSchema(BaseModel):
    """Модель ответа на получение данных пользователя.

    Attributes:
        user: Данные пользователя.
    """
    user: UserSchema


class CreateUserResponseSchema(BaseModel):
    """Модель ответа на создание пользователя.

    Attributes:
        user: Данные созданного пользователя.
    """
    user: UserSchema
