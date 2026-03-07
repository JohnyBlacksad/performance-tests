"""TaskSet для gRPC сценариев тестирования Gateway.

Модуль предоставляет классы TaskSet для Locust, которые инициализируют
gRPC клиенты для всех сервисов Gateway (users, cards, accounts, documents, operations).

Поддерживаемые режимы:
- GatewayGRPCTaskSet — параллельное выполнение задач
- GatewayGRPCSequentialTaskSet — последовательное выполнение задач
"""

from locust import TaskSet, SequentialTaskSet
from clients.grpc.gateway.accounts.client import AccountsGatewayGRPCClient, build_accounts_gateway_locust_grpc_client
from clients.grpc.gateway.cards.client import CardsGatewayGRPCClient, build_cards_gateway_locust_grpc_client
from clients.grpc.gateway.documents.client import DocumentsGatewayGRPCClients, build_documents_gateway_locust_grpc_client
from clients.grpc.gateway.operations.client import OperationsGatewayGRPCClient, build_operations_gateway_locust_grpc_client
from clients.grpc.gateway.users.client import UserGatewayGRPCClient, build_users_gateway_locust_grpc_client

class GatewayGRPCTaskSet(TaskSet):
    """Набор задач для gRPC тестирования Gateway (параллельный режим).

    Инициализирует gRPC клиенты для всех сервисов Gateway и предоставляет
    их для использования в задачах Locust.

    Attributes:
        user_client: Клиент для сервиса пользователей.
        cards_client: Клиент для сервиса карт.
        accounts_client: Клиент для сервиса счетов.
        documents_client: Клиент для сервиса документов.
        operations_client: Клиент для сервиса операций.
    """
    user_client: UserGatewayGRPCClient
    cards_client: CardsGatewayGRPCClient
    accounts_client: AccountsGatewayGRPCClient
    documents_client: DocumentsGatewayGRPCClients
    operations_client: OperationsGatewayGRPCClient

    def on_start(self) -> None:
        """Инициализировать gRPC клиенты при старте TaskSet.

        Создаёт клиенты с Locust-интерцептором для сбора метрик.
        """
        self.user_client = build_users_gateway_locust_grpc_client(self.user.environment)
        self.cards_client = build_cards_gateway_locust_grpc_client(self.user.environment)
        self.accounts_client = build_accounts_gateway_locust_grpc_client(self.user.environment)
        self.documents_client = build_documents_gateway_locust_grpc_client(self.user.environment)
        self.operations_client = build_operations_gateway_locust_grpc_client(self.user.environment)


class GatewayGRPCSequentialTaskSet(SequentialTaskSet):
    """Набор задач для gRPC тестирования Gateway (последовательный режим).

    Инициализирует gRPC клиенты для всех сервисов Gateway и выполняет
    задачи в строгом порядке.

    Attributes:
        user_client: Клиент для сервиса пользователей.
        cards_client: Клиент для сервиса карт.
        accounts_client: Клиент для сервиса счетов.
        documents_client: Клиент для сервиса документов.
        operations_client: Клиент для сервиса операций.
    """
    user_client: UserGatewayGRPCClient
    cards_client: CardsGatewayGRPCClient
    accounts_client: AccountsGatewayGRPCClient
    documents_client: DocumentsGatewayGRPCClients
    operations_client: OperationsGatewayGRPCClient

    def on_start(self) -> None:
        """Инициализировать gRPC клиенты при старте TaskSet.

        Создаёт клиенты с Locust-интерцептором для сбора метрик.
        """
        self.user_client = build_users_gateway_locust_grpc_client(self.user.environment)
        self.cards_client = build_cards_gateway_locust_grpc_client(self.user.environment)
        self.accounts_client = build_accounts_gateway_locust_grpc_client(self.user.environment)
        self.documents_client = build_documents_gateway_locust_grpc_client(self.user.environment)
        self.operations_client = build_operations_gateway_locust_grpc_client(self.user.environment)
