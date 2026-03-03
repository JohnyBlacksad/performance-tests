"""Клиент для подключения к Gateway API.

Модуль предоставляет функцию для создания базового HTTP-клиента,
который используется всеми специализированными клиентами Gateway.
"""

from httpx import Client


def build_gateway_http_client() -> Client:
    """Создать и настроить базовый HTTP-клиент для Gateway API.

    Возвращает экземпляр httpx.Client с предустановленными параметрами:
    - base_url: http://localhost:8003/api/v1/
    - timeout: 100 секунд

    Returns:
        Настроенный экземпляр httpx.Client для работы с Gateway API.

    Example:
        >>> client = build_gateway_http_client()
        >>> response = client.get('/users')
    """
    return Client(base_url='http://localhost:8003/api/v1/', timeout=100)
