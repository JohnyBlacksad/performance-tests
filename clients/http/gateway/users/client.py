"""Клиент для работы с User Gateway API.

Модуль предоставляет класс UserGatewayHTTPClient для управления пользователями:
- Создание новых пользователей
- Получение данных пользователей по ID

Пример использования:
    >>> client = build_users_gateway_http_client()
    >>> user = client.get_user(user_id='u123')
    >>> new_user = client.create_user()
"""

from uuid import uuid4
from clients.http.base_client import BaseHTTPClient
from httpx import Response
from typing import TypedDict
from clients.http.gateway.gateway_client import build_gateway_http_client
from .schema import (
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)


class UserGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для User Gateway API.

    Предоставляет методы для создания и получения данных пользователей.

    Пример использования:
        >>> client = build_users_gateway_http_client()
        >>> user = client.get_user(user_id='u123')
        >>> new_user = client.create_user()
    """

    def get_user_api(self, user_id: str) -> Response:
        """Получить пользователя по ID (API-метод).

        Отправляет GET-запрос для получения данных пользователя.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            HTTP-ответ с данными пользователя.

        Example:
            >>> client = build_users_gateway_http_client()
            >>> response = client.get_user_api('u123')
        """
        return self.get(f'users/{user_id}')

    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """Создать нового пользователя (API-метод).

        Отправляет POST-запрос на создание нового пользователя.

        Args:
            request: Словарь с данными для создания пользователя
                     (email, lastName, firstName, middleName, phoneNumber).

        Returns:
            HTTP-ответ с результатом создания.

        Example:
            >>> client = build_users_gateway_http_client()
            >>> request = {'email': 'test@example.com', 'lastName': 'Ivanov',
            ...            'firstName': 'Ivan', 'middleName': 'Ivanovich',
            ...            'phoneNumber': '+79991234567'}
            >>> response = client.create_user_api(request)
        """
        return self.post('users', json=request.model_dump(by_alias=True))

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        """Получить пользователя по ID (высокоуровневый метод).

        Создаёт и отправляет запрос на получение данных пользователя,
        возвращая их в виде словаря.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            Словарь с данными пользователя.

        Example:
            >>> client = build_users_gateway_http_client()
            >>> user_data = client.get_user(user_id='u123')
            >>> print(user_data['user']['email'])
        """
        response = self.get_user_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)

    def create_user(self) -> CreateUserResponseSchema:
        """Создать нового пользователя с автоматически сгенерированными данными.

        Создаёт пользователя со случайным email и тестовыми данными.
        Использует UUID для генерации уникального email.

        Returns:
            Словарь с данными созданного пользователя.

        Example:
            >>> client = build_users_gateway_http_client()
            >>> new_user = client.create_user()
            >>> print(new_user['user']['id'])
        """
        response = self.create_user_api(
            CreateUserRequestSchema(
                email=f'{str(uuid4())[:6]}@example.com',
                last_name='string', # type: ignore
                middle_name='string', # type: ignore
                first_name='string', # type: ignore
                phone_number='string' # type: ignore
            )
        )

        return CreateUserResponseSchema.model_validate_json(response.text)


def build_users_gateway_http_client() -> UserGatewayHTTPClient:
    """Создать HTTP-клиент для User Gateway API.

    Возвращает настроенный экземпляр UserGatewayHTTPClient для работы
    с API управления пользователями.

    Returns:
        Настроенный экземпляр UserGatewayHTTPClient.

    Example:
        >>> client = build_users_gateway_http_client()
        >>> user = client.get_user(user_id='u123')
    """
    return UserGatewayHTTPClient(client=build_gateway_http_client())
