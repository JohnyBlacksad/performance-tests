from __future__ import annotations
from httpx import Response
from clients.http.base_client import BaseHTTPClient
from typing import TypedDict
from clients.http.gateway.gateway_client import build_gateway_http_client

class CardDict(TypedDict):
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
    card: CardDict

class IssuePhysicalCardResponseDict(TypedDict):
    card: CardDict

class IssueVirtualCardRequestDict(TypedDict):
    """Словарь запроса на выпуск виртуальной карты."""

    userId: str
    accountId: str

class IssuePhysicalCardRequestDict(TypedDict):
    """Словарь запроса на выпуск физической карты."""

    userId: str
    accountId: str

class CardsGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для Cards Gateway API."""

    def issue_virtual_card_api(self, request: IssueVirtualCardRequestDict) -> Response:
        """Выпустить виртуальную карту.

        Args:
            request: Словарь с данными для выпуска виртуальной карты.

        Returns:
            HTTP-ответ.
        """
        return self.post('cards/issue-virtual-card', json=request)

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestDict) -> Response:
        """Выпустить физическую карту.

        Args:
            request: Словарь с данными для выпуска физической карты.

        Returns:
            HTTP-ответ.
        """
        return self.post('cards/issue-physical-card', json=request)

    def issue_virtual_card(self, user_id: str, account_id: str) -> IssueVirtualCardResponseDict:

        request = IssueVirtualCardRequestDict(
            userId=user_id,
            accountId=account_id
        )

        response = self.issue_virtual_card_api(request)
        return response.json()

    def issue_physical_card(self, user_id: str, account_id: str) -> IssuePhysicalCardResponseDict:

        request = IssuePhysicalCardRequestDict(
            userId=user_id,
            accountId=account_id
        )

        response = self.issue_physical_card_api(request)
        return response.json()

def build_cards_gateway_http_client() -> CardsGatewayHTTPClient:
    """Создать HTTP-клиент для Cards Gateway API.

    Returns:
        Настроенный экземпляр CardsGatewayHTTPClient.
    """
    return CardsGatewayHTTPClient(client=build_gateway_http_client())