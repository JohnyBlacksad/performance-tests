"""Модуль клиентов для выполнения запросов к различным API.

Этот пакет предоставляет набор HTTP-клиентов для взаимодействия
с внешними сервисами и API в рамках performance-тестирования.

Пример использования:
    >>> from clients.http import BaseHTTPClient, build_gateway_http_client
    >>> client = build_gateway_http_client()
    >>> http = BaseHTTPClient(client)
    >>> response = http.get('/endpoint')
"""
