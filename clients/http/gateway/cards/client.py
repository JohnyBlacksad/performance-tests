from httpx import Response
from base_client import BaseHTTPClient
from typing import TypedDict

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
        return self.post('cards/issue_virtual_card', json=request)

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestDict) -> Response:
        """Выпустить физическую карту.

        Args:
            request: Словарь с данными для выпуска физической карты.

        Returns:
            HTTP-ответ.
        """
        return self.post('cards/issue_physical_card', json=request)