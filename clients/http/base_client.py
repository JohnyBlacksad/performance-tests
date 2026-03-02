from httpx import Client, URL, QueryParams, Response
from typing import Any


class BaseHTTPClient:
    """Базовый HTTP-клиент для выполнения API-запросов."""

    def __init__(self, client: Client):
        """Инициализировать базовый HTTP-клиент.

        Args:
            client: Экземпляр httpx Client.
        """
        self.client = client

    def get(self, url: URL|str, params: QueryParams|dict|None = None) -> Response:
        """Отправить GET-запрос.

        Args:
            url: URL для отправки запроса.
            params: Опциональные параметры запроса.

        Returns:
            HTTP-ответ.
        """
        return self.client.get(url, params=params)

    def post(self, url: URL|str, json: Any = None) -> Response:
        """Отправить POST-запрос.

        Args:
            url: URL для отправки запроса.
            json: Опциональная JSON-нагрузка.

        Returns:
            HTTP-ответ.
        """
        return self.client.post(url, json=json)