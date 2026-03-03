"""Клиенты для Operations Gateway API.

Экспортирует класс OperationsGatewayHTTPClient и функцию-фабрику
для работы с API управления операциями.
"""

from clients.http.gateway.operations.client import (
    OperationsGatewayHTTPClient,
    build_operations_gateway_http_client,
)

__all__ = ['OperationsGatewayHTTPClient', 'build_operations_gateway_http_client']
