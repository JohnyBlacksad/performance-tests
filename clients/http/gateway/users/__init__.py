"""Клиенты для Users Gateway API.

Экспортирует класс UserGatewayHTTPClient и функцию-фабрику
для работы с API управления пользователями.
"""

from clients.http.gateway.users.client import (
    UserGatewayHTTPClient,
    build_users_gateway_http_client,
)

__all__ = ['UserGatewayHTTPClient', 'build_users_gateway_http_client']
