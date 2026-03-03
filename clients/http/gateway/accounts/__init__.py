"""Клиенты для Accounts Gateway API.

Экспортирует класс AccountsGatewayHTTPClient и функцию-фабрику
для работы с API управления счетами.
"""

from clients.http.gateway.accounts.client import (
    AccountsGatewayHTTPClient,
    build_accounts_gateway_http_client,
)

__all__ = ['AccountsGatewayHTTPClient', 'build_accounts_gateway_http_client']
