"""Клиент для подключения к Gateway API.

Модуль предоставляет функцию для создания базового HTTP-клиента,
который используется всеми специализированными клиентами Gateway.
"""

from httpx import Client
from locust.env import Environment
from clients.http.event_hooks.locust_event_hook import (
    locust_request_event_hook,
    locust_response_event_hook
)


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

def build_gateway_locust_http_client(environment: Environment) -> Client:
    """Создать HTTP-клиент с интеграцией Locust для сбора метрик.

    Создаёт клиент с event hooks для перехвата запросов и ответов,
    отправляя метрики производительности в Locust.

    Args:
        environment: Экземпляр окружения Locust.

    Returns:
        Настроенный экземпляр httpx.Client с event hooks.

    Example:
        >>> client = build_gateway_locust_http_client(env)
        >>> response = client.get('/users')
    """
    return Client(base_url='http://localhost:8003/api/v1/', timeout=100,
                  event_hooks={
                      'request': [locust_request_event_hook],
                      'response': [locust_response_event_hook(environment)]
                  })
