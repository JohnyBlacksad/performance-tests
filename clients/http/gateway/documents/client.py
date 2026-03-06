"""Клиент для работы с Documents Gateway API.

Модуль предоставляет класс DocumentsGatewayHTTPClient для работы с документами:
- Получение тарифных документов по счёту
- Получение договоров по счёту

Пример использования:
    >>> client = build_documents_gateway_http_client()
    >>> tariff = client.get_tariff_document_api(account_id='a123')
    >>> contract = client.get_contract_document_api(account_id='a123')
"""

from httpx import Response
from locust.env import Environment
from clients.http.base_client import BaseHTTPClient, HTTPClientExtensions
from clients.http.gateway.gateway_client import build_gateway_http_client, build_gateway_locust_http_client
from .schema import (
    GetTariffDocumentResponseSchema,
    GetContractDocumentResponseSchema
)

class DocumentsGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для Documents Gateway API.

    Предоставляет методы для получения тарифных документов и договоров.

    Пример использования:
        >>> client = build_documents_gateway_http_client()
        >>> tariff = client.get_tariff_document_api(account_id='a123')
    """

    def get_tariff_document_api(self, account_id: str) -> Response:
        """Получить тарифный документ по счёту (API-метод).

        Отправляет GET-запрос для получения тарифного документа,
        связанного с указанным счётом.

        Args:
            account_id: Уникальный идентификатор счёта.

        Returns:
            HTTP-ответ с тарифным документом.

        Example:
            >>> client = build_documents_gateway_http_client()
            >>> response = client.get_tariff_document_api('a123')
        """
        return self.get(f'documents/tariff-document/{account_id}',
                        extensions=HTTPClientExtensions(route='documents/tariff-document/{account_id}'))

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseSchema:
        """Получить тарифный документ по счёту (высокоуровневый метод).

        Создаёт и отправляет запрос на получение тарифного документа,
        возвращая его в виде модели GetTariffDocumentResponseSchema.

        Args:
            account_id: Уникальный идентификатор счёта.

        Returns:
            Модель GetTariffDocumentResponseSchema с данными тарифного документа.

        Example:
            >>> client = build_documents_gateway_http_client()
            >>> tariff = client.get_tariff_document(account_id='a123')
            >>> print(tariff.tariff.url)
        """
        response = self.get_tariff_document_api(account_id)
        return GetTariffDocumentResponseSchema.model_validate_json(response.text)

    def get_contract_document_api(self, account_id: str) -> Response:
        """Получить договор по счёту (API-метод).

        Отправляет GET-запрос для получения договора,
        связанного с указанным счётом.

        Args:
            account_id: Уникальный идентификатор счёта.

        Returns:
            HTTP-ответ с договором.

        Example:
            >>> client = build_documents_gateway_http_client()
            >>> response = client.get_contract_document_api('a123')
        """
        return self.get(f'documents/contract-document/{account_id}',
                        extensions=HTTPClientExtensions(route='documents/contract-document/{account_id}'))

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseSchema:
        """Получить договор по счёту (высокоуровневый метод).

        Создаёт и отправляет запрос на получение договора,
        возвращая его в виде модели GetContractDocumentResponseSchema.

        Args:
            account_id: Уникальный идентификатор счёта.

        Returns:
            Модель GetContractDocumentResponseSchema с данными договора.

        Example:
            >>> client = build_documents_gateway_http_client()
            >>> contract = client.get_contract_document(account_id='a123')
            >>> print(contract.contract.url)
        """
        response = self.get_contract_document_api(account_id)
        return GetContractDocumentResponseSchema.model_validate_json(response.text)


def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """Создать HTTP-клиент для Documents Gateway API.

    Возвращает настроенный экземпляр DocumentsGatewayHTTPClient для работы
    с API управления документами.

    Returns:
        Настроенный экземпляр DocumentsGatewayHTTPClient.

    Example:
        >>> client = build_documents_gateway_http_client()
        >>> response = client.get_tariff_document_api(account_id='a123')
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())

def build_documents_locust_gateway_http_client(environment: Environment) -> DocumentsGatewayHTTPClient:
    return DocumentsGatewayHTTPClient(client=build_gateway_locust_http_client(environment))

