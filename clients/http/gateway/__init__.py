"""Клиенты для Gateway API.

Модуль предоставляет функции для создания настроенных HTTP-клиентов,
предназначенных для работы с Gateway сервисом.
"""

from httpx import Client


def build_gateway_http_client() -> Client:
    """Создать и настроить HTTP-клиент для Gateway API.

    Возвращает экземпляр httpx.Client с предустановленными параметрами:
    - base_url: http://localhost:8003/api/v1/
    - timeout: 100 секунд

    Returns:
        Настроенный экземпляр httpx.Client для работы с Gateway API.

    Пример использования:
        >>> client = build_gateway_http_client()
        >>> http = BaseHTTPClient(client)
        >>> response = http.get('/users')
    """
    return Client(base_url='http://localhost:8003/api/v1/', timeout=100)
