"""Клиент для работы с Cards Gateway API.

Модуль предоставляет класс CardsGatewayHTTPClient для управления картами:
- Выпуск виртуальных карт
- Выпуск физических карт

Пример использования:
    >>> client = build_cards_gateway_http_client()
    >>> response = client.issue_virtual_card(user_id='u123', account_id='a456')
"""

from httpx import Response
from locust.env import Environment
from clients.http.base_client import BaseHTTPClient
from clients.http.gateway.gateway_client import build_gateway_http_client, build_gateway_locust_http_client
from .schema import (
    IssueVirtualCardRequestSchema,
    IssueVirtualCardResponseSchema,
    IssuePhysicalCardRequestSchema,
    IssuePhysicalCardResponseSchema
)


class CardsGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для Cards Gateway API.

    Предоставляет методы для выпуска виртуальных и физических карт.

    Пример использования:
        >>> client = build_cards_gateway_http_client()
        >>> card_data = client.issue_virtual_card(user_id='u123', account_id='a456')
    """

    def issue_virtual_card_api(self, request: IssueVirtualCardRequestSchema) -> Response:
        """Выпустить виртуальную карту (API-метод).

        Отправляет POST-запрос на выпуск виртуальной карты.

        Args:
            request: Модель запроса на выпуск виртуальной карты
                     (IssueVirtualCardRequestSchema).

        Returns:
            HTTP-ответ от сервера.

        Example:
            >>> client = build_cards_gateway_http_client()
            >>> request = IssueVirtualCardRequestSchema(
            ...     user_id='u123',
            ...     account_id='a456'
            ... )
            >>> response = client.issue_virtual_card_api(request)
        """
        return self.post('cards/issue-virtual-card', json=request.model_dump(by_alias=True))

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestSchema) -> Response:
        """Выпустить физическую карту (API-метод).

        Отправляет POST-запрос на выпуск физической карты.

        Args:
            request: Модель запроса на выпуск физической карты
                     (IssuePhysicalCardRequestSchema).

        Returns:
            HTTP-ответ от сервера.

        Example:
            >>> client = build_cards_gateway_http_client()
            >>> request = IssuePhysicalCardRequestSchema(
            ...     user_id='u123',
            ...     account_id='a456'
            ... )
            >>> response = client.issue_physical_card_api(request)
        """
        return self.post('cards/issue-physical-card', json=request.model_dump(by_alias=True))

    def issue_virtual_card(self, user_id: str, account_id: str) -> IssueVirtualCardResponseSchema:
        """Выпустить виртуальную карту (высокоуровневый метод).

        Создаёт и отправляет запрос на выпуск виртуальной карты,
        возвращая данные карты в виде модели IssueVirtualCardResponseSchema.

        Args:
            user_id: Уникальный идентификатор пользователя.
            account_id: Уникальный идентификатор счёта.

        Returns:
            Модель IssueVirtualCardResponseSchema с данными выпущенной карты.

        Example:
            >>> client = build_cards_gateway_http_client()
            >>> card = client.issue_virtual_card(user_id='u123', account_id='a456')
            >>> print(card.card.card_number)
        """
        request = IssueVirtualCardRequestSchema(
            user_id=user_id, # type: ignore
            account_id=account_id # type: ignore
        )

        response = self.issue_virtual_card_api(request)
        return IssueVirtualCardResponseSchema.model_validate_json(response.text)

    def issue_physical_card(self, user_id: str, account_id: str) -> IssuePhysicalCardResponseSchema:
        """Выпустить физическую карту (высокоуровневый метод).

        Создаёт и отправляет запрос на выпуск физической карты,
        возвращая данные карты в виде модели IssuePhysicalCardResponseSchema.

        Args:
            user_id: Уникальный идентификатор пользователя.
            account_id: Уникальный идентификатор счёта.

        Returns:
            Модель IssuePhysicalCardResponseSchema с данными выпущенной карты.

        Example:
            >>> client = build_cards_gateway_http_client()
            >>> card = client.issue_physical_card(user_id='u123', account_id='a456')
            >>> print(card.card.card_number)
        """
        request = IssuePhysicalCardRequestSchema(
            user_id=user_id, # type: ignore
            account_id=account_id # type: ignore
        )

        response = self.issue_physical_card_api(request)
        return IssuePhysicalCardResponseSchema.model_validate_json(response.text)


def build_cards_gateway_http_client() -> CardsGatewayHTTPClient:
    """Создать HTTP-клиент для Cards Gateway API.

    Возвращает настроенный экземпляр CardsGatewayHTTPClient для работы
    с API управления картами.

    Returns:
        Настроенный экземпляр CardsGatewayHTTPClient.

    Example:
        >>> client = build_cards_gateway_http_client()
        >>> card = client.issue_virtual_card(user_id='u123', account_id='a456')
    """
    return CardsGatewayHTTPClient(client=build_gateway_http_client())

def build_cards_locust_gateway_http_client(environment: Environment) -> CardsGatewayHTTPClient:
    """Создать HTTP-клиент для Cards Gateway API с интеграцией Locust.

    Возвращает настроенный экземпляр CardsGatewayHTTPClient для работы
    с API управления картами через Locust (сбор метрик).

    Args:
        environment: Окружение Locust для настройки клиента.

    Returns:
        Настроенный экземпляр CardsGatewayHTTPClient с Locust-интерцептором.

    Example:
        >>> client = build_cards_locust_gateway_http_client(environment)
        >>> card = client.issue_virtual_card(user_id='u123', account_id='a456')
    """
    return CardsGatewayHTTPClient(client=build_gateway_locust_http_client(environment))


