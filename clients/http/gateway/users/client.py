from uuid import uuid4
from clients.http.base_client import BaseHTTPClient
from httpx import Response
from typing import TypedDict
from clients.http.gateway.gateway_client import build_gateway_http_client

class CreateUserRequestDict(TypedDict):
    """Словарь, представляющий запрос на создание пользователя."""

    email: str
    lastName: str
    firstName: str
    middleName: str
    phoneNumber: str

class UserDict(TypedDict):
    id: str
    email: str
    lastName: str
    firstName: str
    middleName: str
    phoneNumber: str

class GetUserResponseDict(TypedDict):
    user: UserDict

class CreateUserResponseDict(TypedDict):
    user: UserDict

class UserGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для User Gateway API."""

    def get_user_api(self, user_id: str) -> Response:
        """Получить пользователя по ID.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            HTTP-ответ с данными пользователя.
        """
        return self.get(f'users/{user_id}')

    def create_user_api(self, request: CreateUserRequestDict) -> Response:
        """Создать нового пользователя.

        Args:
            request: Словарь с данными для создания пользователя.

        Returns:
            HTTP-ответ.
        """
        return self.post('users', json=request)

    def get_user(self, user_id: str) -> GetUserResponseDict:
        response = self.get_user_api(user_id)
        return response.json()

    def create_user(self) -> CreateUserResponseDict:

        response = self.create_user_api(
            CreateUserRequestDict(
                email= f'{str(uuid4())[:6]}@example.com',
                lastName='string',
                middleName='string',
                firstName='string',
                phoneNumber='string'
            )
        )

        return response.json()

def build_users_gateway_http_client() -> UserGatewayHTTPClient:
    """Создать HTTP-клиент для User Gateway API.

    Returns:
        Настроенный экземпляр UserGatewayHTTPClient.
    """
    return UserGatewayHTTPClient(client=build_gateway_http_client())