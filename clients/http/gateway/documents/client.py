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
from typing import TypedDict
from clients.http.base_client import BaseHTTPClient
from clients.http.gateway.gateway_client import build_gateway_http_client

class TariffDict(TypedDict):
    """Словарь, представляющий данные тарифного документа.

    Attributes:
        url: URL для доступа к тарифному документу.
        document: Содержимое документа в формате base64 или текст.
    """
    url: str
    document: str


class GetTariffDocumentResponseDict(TypedDict):
    """Словарь ответа на получение тарифного документа.

    Attributes:
        tariff: Данные тарифного документа.
    """
    tariff: TariffDict


class ContractDict(TypedDict):
    """Словарь, представляющий данные договора.

    Attributes:
        url: URL для доступа к договору.
        document: Содержимое договора в формате base64 или текст.
    """
    url: str
    document: str


class GetContractDocumentResponseDict(TypedDict):
    """Словарь ответа на получение договора.

    Attributes:
        contract: Данные договора.
    """
    contract: ContractDict

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
        return self.get(f'documents/tariff-document/{account_id}')

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseDict:
        """Получить тарифный документ по счёту (высокоуровневый метод).

        Создаёт и отправляет запрос на получение тарифного документа,
        возвращая его в виде словаря.

        Args:
            account_id: Уникальный идентификатор счёта.

        Returns:
            Словарь с данными тарифного документа.

        Example:
            >>> client = build_documents_gateway_http_client()
            >>> tariff = client.get_tariff_document(account_id='a123')
            >>> print(tariff['tariff']['url'])
        """
        response = self.get_tariff_document_api(account_id)
        return response.json()

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
        return self.get(f'documents/contract-document/{account_id}')

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseDict:
        """Получить договор по счёту (высокоуровневый метод).

        Создаёт и отправляет запрос на получение договора,
        возвращая его в виде словаря.

        Args:
            account_id: Уникальный идентификатор счёта.

        Returns:
            Словарь с данными договора.

        Example:
            >>> client = build_documents_gateway_http_client()
            >>> contract = client.get_contract_document(account_id='a123')
            >>> print(contract['contract']['url'])
        """
        response = self.get_contract_document_api(account_id)
        return response.json()


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
