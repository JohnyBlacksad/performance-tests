"""Клиенты для Cards Gateway API.

Экспортирует класс CardsGatewayHTTPClient и функцию-фабрику
для работы с API управления картами.
"""

from clients.http.gateway.cards.client import (
    CardsGatewayHTTPClient,
    build_cards_gateway_http_client,
)

__all__ = ['CardsGatewayHTTPClient', 'build_cards_gateway_http_client']
