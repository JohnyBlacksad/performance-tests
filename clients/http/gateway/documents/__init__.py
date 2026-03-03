"""Клиенты для Documents Gateway API.

Экспортирует класс DocumentsGatewayHTTPClient и функцию-фабрику
для работы с API управления документами.
"""

from clients.http.gateway.documents.client import (
    DocumentsGatewayHTTPClient,
    build_documents_gateway_http_client,
)

__all__ = ['DocumentsGatewayHTTPClient', 'build_documents_gateway_http_client']
