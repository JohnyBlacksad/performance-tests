"""Клиент для работы с Cards Gateway API.

Модуль предоставляет класс CardsGatewayHTTPClient для управления картами:
- Выпуск виртуальных карт
- Выпуск физических карт

Пример использования:
    >>> client = build_cards_gateway_http_client()
    >>> response = client.issue_virtual_card(user_id='u123', account_id='a456')
"""

from __future__ import annotations
from httpx import Response
from clients.http.base_client import BaseHTTPClient
from typing import TypedDict
from clients.http.gateway.gateway_client import build_gateway_http_client


class CardDict(TypedDict):
    """Словарь, представляющий данные карты.

    Attributes:
        id: Уникальный идентификатор карты.
        pin: PIN-код карты.
        cvv: CVV-код карты.
        type: Тип карты.
        status: Статус карты.
        accountId: Идентификатор счёта, к которому привязана карта.
        cardNumber: Номер карты.
        cardHolder: Имя держателя карты.
        expiryDate: Срок действия карты.
        paymentSystem: Платёжная система карты.
    """
    id: str
    pin: str
    cvv: str
    type: str
    status: str
    accountId: str
    cardNumber: str
    cardHolder: str
    expiryDate: str
    paymentSystem: str


class IssueVirtualCardResponseDict(TypedDict):
    """Словарь ответа на выпуск виртуальной карты.

    Attributes:
        card: Данные выпущенной карты.
    """
    card: CardDict


class IssuePhysicalCardResponseDict(TypedDict):
    """Словарь ответа на выпуск физической карты.

    Attributes:
        card: Данные выпущенной карты.
    """
    card: CardDict


class IssueVirtualCardRequestDict(TypedDict):
    """Словарь запроса на выпуск виртуальной карты.

    Attributes:
        userId: Уникальный идентификатор пользователя.
        accountId: Уникальный идентификатор счёта.
    """
    userId: str
    accountId: str


class IssuePhysicalCardRequestDict(TypedDict):
    """Словарь запроса на выпуск физической карты.

    Attributes:
        userId: Уникальный идентификатор пользователя.
        accountId: Уникальный идентификатор счёта.
    """
    userId: str
    accountId: str


class CardsGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для Cards Gateway API.

    Предоставляет методы для выпуска виртуальных и физических карт.

    Пример использования:
        >>> client = build_cards_gateway_http_client()
        >>> card_data = client.issue_virtual_card(user_id='u123', account_id='a456')
    """

    def issue_virtual_card_api(self, request: IssueVirtualCardRequestDict) -> Response:
        """Выпустить виртуальную карту (API-метод).

        Отправляет POST-запрос на выпуск виртуальной карты.

        Args:
            request: Словарь с данными для выпуска виртуальной карты
                     (userId, accountId).

        Returns:
            HTTP-ответ от сервера.

        Example:
            >>> client = build_cards_gateway_http_client()
            >>> request = {'userId': 'u123', 'accountId': 'a456'}
            >>> response = client.issue_virtual_card_api(request)
        """
        return self.post('cards/issue-virtual-card', json=request)

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestDict) -> Response:
        """Выпустить физическую карту (API-метод).

        Отправляет POST-запрос на выпуск физической карты.

        Args:
            request: Словарь с данными для выпуска физической карты
                     (userId, accountId).

        Returns:
            HTTP-ответ от сервера.

        Example:
            >>> client = build_cards_gateway_http_client()
            >>> request = {'userId': 'u123', 'accountId': 'a456'}
            >>> response = client.issue_physical_card_api(request)
        """
        return self.post('cards/issue-physical-card', json=request)

    def issue_virtual_card(self, user_id: str, account_id: str) -> IssueVirtualCardResponseDict:
        """Выпустить виртуальную карту (высокоуровневый метод).

        Создаёт и отправляет запрос на выпуск виртуальной карты,
        возвращая данные карты в виде словаря.

        Args:
            user_id: Уникальный идентификатор пользователя.
            account_id: Уникальный идентификатор счёта.

        Returns:
            Словарь с данными выпущенной карты.

        Example:
            >>> client = build_cards_gateway_http_client()
            >>> card = client.issue_virtual_card(user_id='u123', account_id='a456')
            >>> print(card['card']['cardNumber'])
        """
        request = IssueVirtualCardRequestDict(
            userId=user_id,
            accountId=account_id
        )

        response = self.issue_virtual_card_api(request)
        return response.json()

    def issue_physical_card(self, user_id: str, account_id: str) -> IssuePhysicalCardResponseDict:
        """Выпустить физическую карту (высокоуровневый метод).

        Создаёт и отправляет запрос на выпуск физической карты,
        возвращая данные карты в виде словаря.

        Args:
            user_id: Уникальный идентификатор пользователя.
            account_id: Уникальный идентификатор счёта.

        Returns:
            Словарь с данными выпущенной карты.

        Example:
            >>> client = build_cards_gateway_http_client()
            >>> card = client.issue_physical_card(user_id='u123', account_id='a456')
            >>> print(card['card']['cardNumber'])
        """
        request = IssuePhysicalCardRequestDict(
            userId=user_id,
            accountId=account_id
        )

        response = self.issue_physical_card_api(request)
        return response.json()


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
