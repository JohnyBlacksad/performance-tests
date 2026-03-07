"""gRPC клиент для Documents Gateway сервиса.

Модуль предоставляет класс DocumentsGatewayGRPCClients для работы с документами:
- Получение тарифных документов по счёту
- Получение договоров по счёту

Пример использования:
    >>> client = build_documents_gateway_grpc_client()
    >>> tariff = client.get_tariff_document(account_id='a123')
"""

from grpc import Channel
from locust.env import Environment
from clients.grpc.client import GRPCClient, build_gateway_grpc_client, build_gateway_locust_grpc_client
from contracts.services.gateway.documents.documents_gateway_service_pb2_grpc import DocumentsGatewayServiceStub
from contracts.services.gateway.documents.rpc_get_contract_document_pb2 import GetContractDocumentRequest, GetContractDocumentResponse
from contracts.services.gateway.documents.rpc_get_tariff_document_pb2 import GetTariffDocumentRequest, GetTariffDocumentResponse

class DocumentsGatewayGRPCClients(GRPCClient):
    """gRPC клиент для Documents Gateway сервиса.

    Предоставляет методы для получения тарифных документов и договоров.

    Example:
        >>> client = build_documents_gateway_grpc_client()
        >>> tariff = client.get_tariff_document(account_id='a123')
    """
    def __init__(self, channel: Channel) -> None:
        """Инициализировать клиент для работы с документами.

        Args:
            channel: gRPC канал для подключения.
        """
        super().__init__(channel)
        self.stub = DocumentsGatewayServiceStub(channel)

    def get_contract_document_api(self, request: GetContractDocumentRequest) -> GetContractDocumentResponse:
        """Получить договор по счёту (низкоуровневый метод).

        Args:
            request: Запрос на получение договора.

        Returns:
            Ответ с данными договора.
        """
        return self.stub.GetContractDocument(request)

    def get_tariff_document_api(self, request: GetTariffDocumentRequest) -> GetTariffDocumentResponse:
        """Получить тарифный документ по счёту (низкоуровневый метод).

        Args:
            request: Запрос на получение тарифного документа.

        Returns:
            Ответ с данными тарифа.
        """
        return self.stub.GetTariffDocument(request)

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponse:
        """Получить договор по счёту.

        Args:
            account_id: Идентификатор счёта.

        Returns:
            Ответ с данными договора.
        """
        request = GetContractDocumentRequest(account_id=account_id)
        return self.get_contract_document_api(request)

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponse:
        """Получить тарифный документ по счёту.

        Args:
            account_id: Идентификатор счёта.

        Returns:
            Ответ с данными тарифа.
        """
        request = GetTariffDocumentRequest(account_id=account_id)
        return self.get_tariff_document_api(request)

def build_documents_gateway_grpc_client() -> DocumentsGatewayGRPCClients:
    """Создать gRPC клиент для Documents Gateway.

    Returns:
        Настроенный экземпляр DocumentsGatewayGRPCClients.
    """
    return DocumentsGatewayGRPCClients(channel=build_gateway_grpc_client())

def build_documents_gateway_locust_grpc_client(environment: Environment) -> DocumentsGatewayGRPCClients:
    """Создать gRPC клиент с интеграцией Locust для Documents Gateway.

    Args:
        environment: Экземпляр окружения Locust.

    Returns:
        Настроенный экземпляр DocumentsGatewayGRPCClients с интерцептором.
    """
    return DocumentsGatewayGRPCClients(channel=build_gateway_locust_grpc_client(environment))