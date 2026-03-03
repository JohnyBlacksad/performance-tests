"""Базовый HTTP-клиент для выполнения API-запросов.

Модуль предоставляет класс BaseHTTPClient — обёртку над httpx.Client,
которая упрощает отправку HTTP-запросов в performance-тестах.
"""

from httpx import Client, URL, QueryParams, Response
from typing import Any


class BaseHTTPClient:
    """Базовый HTTP-клиент для выполнения API-запросов.

    Класс предоставляет удобный интерфейс для отправки GET и POST запросов
    через обёртку над httpx.Client.

    Attributes:
        client: Экземпляр httpx.Client для выполнения запросов.

    Пример использования:
        >>> from httpx import Client
        >>> client = Client(base_url='http://api.example.com')
        >>> http = BaseHTTPClient(client)
        >>> response = http.get('/users', params={'limit': 10})
        >>> response = http.post('/users', json={'name': 'John'})
    """

    def __init__(self, client: Client):
        """Инициализировать базовый HTTP-клиент.

        Args:
            client: Экземпляр httpx.Client для выполнения запросов.
        """
        self.client = client

    def get(self, url: URL | str, params: QueryParams | dict | None = None) -> Response:
        """Отправить GET-запрос к указанному URL.

        Args:
            url: URL для отправки запроса (строка или объект URL).
            params: Опциональные параметры запроса (словарь или QueryParams).

        Returns:
            Объект Response с данными HTTP-ответа.

        Raises:
            httpx.HTTPError: При возникновении ошибок HTTP.
        """
        return self.client.get(url, params=params)

    def post(self, url: URL | str, json: Any = None) -> Response:
        """Отправить POST-запрос к указанному URL.

        Args:
            url: URL для отправки запроса (строка или объект URL).
            json: Опциональные данные в формате JSON для отправки в теле запроса.

        Returns:
            Объект Response с данными HTTP-ответа.

        Raises:
            httpx.HTTPError: При возникновении ошибок HTTP.
        """
        return self.client.post(url, json=json)