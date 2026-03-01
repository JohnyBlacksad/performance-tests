from base_client import BaseHTTPClient
from httpx import Response
from typing import TypedDict

class CreateUserRequestDict(TypedDict):
    """Словарь, представляющий запрос на создание пользователя."""

    email: str
    lastName: str
    firstName: str
    middleName: str
    phoneNumber: str

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
        return self.post('users/', json=request)