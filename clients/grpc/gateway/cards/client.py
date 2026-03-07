"""gRPC клиент для Cards Gateway сервиса.

Модуль предоставляет класс CardsGatewayGRPCClient для управления картами:
- Выпуск виртуальных карт
- Выпуск физических карт

Пример использования:
    >>> client = build_cards_gateway_grpc_client()
    >>> card = client.issue_virtual_card(user_id='u123', account_id='a456')
"""

from grpc import Channel
from locust.env import Environment
from clients.grpc.client import GRPCClient, build_gateway_grpc_client, build_gateway_locust_grpc_client
from contracts.services.gateway.cards.cards_gateway_service_pb2_grpc import CardsGatewayServiceStub
from contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import IssuePhysicalCardRequest, IssuePhysicalCardResponse
from contracts.services.gateway.cards.rpc_issue_virtual_card_pb2 import IssueVirtualCardRequest, IssueVirtualCardResponse

class CardsGatewayGRPCClient(GRPCClient):
    """gRPC клиент для Cards Gateway сервиса.

    Предоставляет методы для выпуска виртуальных и физических карт.

    Example:
        >>> client = build_cards_gateway_grpc_client()
        >>> card = client.issue_virtual_card(user_id='u123', account_id='a456')
    """
    def __init__(self, channel: Channel) -> None:
        """Инициализировать клиент для работы с картами.

        Args:
            channel: gRPC канал для подключения.
        """
        super().__init__(channel)
        self.stub = CardsGatewayServiceStub(channel)

    def issue_physical_card_api(self, request: IssuePhysicalCardRequest) -> IssuePhysicalCardResponse:
        """Выпустить физическую карту (низкоуровневый метод).

        Args:
            request: Запрос на выпуск физической карты.

        Returns:
            Ответ с данными выпущенной карты.
        """
        return self.stub.IssuePhysicalCard(request)

    def issue_virtual_card_api(self, request: IssueVirtualCardRequest) -> IssueVirtualCardResponse:
        """Выпустить виртуальную карту (низкоуровневый метод).

        Args:
            request: Запрос на выпуск виртуальной карты.

        Returns:
            Ответ с данными выпущенной карты.
        """
        return self.stub.IssueVirtualCard(request)

    def issue_physical_card(self, user_id: str, account_id: str) -> IssuePhysicalCardResponse:
        """Выпустить физическую карту.

        Args:
            user_id: Идентификатор пользователя.
            account_id: Идентификатор счёта.

        Returns:
            Ответ с данными выпущенной карты.
        """
        request = IssuePhysicalCardRequest(
            user_id=user_id,
            account_id=account_id
        )
        return self.issue_physical_card_api(request)

    def issue_virtual_card(self, user_id: str, account_id: str) -> IssueVirtualCardResponse:
        """Выпустить виртуальную карту.

        Args:
            user_id: Идентификатор пользователя.
            account_id: Идентификатор счёта.

        Returns:
            Ответ с данными выпущенной карты.
        """
        request = IssueVirtualCardRequest(
            user_id=user_id,
            account_id=account_id
        )
        return self.issue_virtual_card_api(request)

def build_cards_gateway_client() -> CardsGatewayGRPCClient:
    """Создать gRPC клиент для Cards Gateway.

    Returns:
        Настроенный экземпляр CardsGatewayGRPCClient.
    """
    return CardsGatewayGRPCClient(channel=build_gateway_grpc_client())

def build_cards_gateway_locust_grpc_client(environment: Environment) -> CardsGatewayGRPCClient:
    """Создать gRPC клиент с интеграцией Locust для Cards Gateway.

    Args:
        environment: Экземпляр окружения Locust.

    Returns:
        Настроенный экземпляр CardsGatewayGRPCClient с интерцептором.
    """
    return CardsGatewayGRPCClient(channel=build_gateway_locust_grpc_client(environment))