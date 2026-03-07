"""TaskSet для HTTP сценариев тестирования Gateway.

Модуль предоставляет классы TaskSet для Locust, которые инициализируют
HTTP клиенты для всех сервисов Gateway (users, cards, accounts, documents, operations).

Поддерживаемые режимы:
- GatewayHTTPTaskSet — параллельное выполнение задач
- GatewayHTTPSequentialTaskSet — последовательное выполнение задач
"""

from locust import TaskSet, SequentialTaskSet
from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient, build_accounts_locust_gateway_http_client
from clients.http.gateway.cards.client import CardsGatewayHTTPClient, build_cards_locust_gateway_http_client
from clients.http.gateway.documents.client import DocumentsGatewayHTTPClient, build_documents_locust_gateway_http_client
from clients.http.gateway.operations.client import OperationsGatewayHTTPClient, build_operations_locust_gateway_http_client
from clients.http.gateway.users.client import UserGatewayHTTPClient, build_users_locust_gateway_http_client

class GatewayHTTPTaskSet(TaskSet):
    """Набор задач для HTTP тестирования Gateway (параллельный режим).

    Инициализирует HTTP клиенты для всех сервисов Gateway и предоставляет
    их для использования в задачах Locust.

    Attributes:
        user_client: Клиент для сервиса пользователей.
        cards_client: Клиент для сервиса карт.
        accounts_client: Клиент для сервиса счетов.
        documents_client: Клиент для сервиса документов.
        operations_client: Клиент для сервиса операций.
    """
    user_client: UserGatewayHTTPClient
    cards_client: CardsGatewayHTTPClient
    accounts_client: AccountsGatewayHTTPClient
    documents_client: DocumentsGatewayHTTPClient
    operations_client: OperationsGatewayHTTPClient

    def on_start(self) -> None:
        """Инициализировать HTTP клиенты при старте TaskSet.

        Создаёт клиенты с Locust event hooks для сбора метрик.
        """
        self.user_client = build_users_locust_gateway_http_client(self.user.environment)
        self.cards_client = build_cards_locust_gateway_http_client(self.user.environment)
        self.accounts_client = build_accounts_locust_gateway_http_client(self.user.environment)
        self.documents_client = build_documents_locust_gateway_http_client(self.user.environment)
        self.operations_client = build_operations_locust_gateway_http_client(self.user.environment)


class GatewayHTTPSequentialTaskSet(SequentialTaskSet):
    """Набор задач для HTTP тестирования Gateway (последовательный режим).

    Инициализирует HTTP клиенты для всех сервисов Gateway и выполняет
    задачи в строгом порядке.

    Attributes:
        user_client: Клиент для сервиса пользователей.
        cards_client: Клиент для сервиса карт.
        accounts_client: Клиент для сервиса счетов.
        documents_client: Клиент для сервиса документов.
        operations_client: Клиент для сервиса операций.
    """
    user_client: UserGatewayHTTPClient
    cards_client: CardsGatewayHTTPClient
    accounts_client: AccountsGatewayHTTPClient
    documents_client: DocumentsGatewayHTTPClient
    operations_client: OperationsGatewayHTTPClient

    def on_start(self) -> None:
        """Инициализировать HTTP клиенты при старте TaskSet.

        Создаёт клиенты с Locust event hooks для сбора метрик.
        """
        self.user_client = build_users_locust_gateway_http_client(self.user.environment)
        self.cards_client = build_cards_locust_gateway_http_client(self.user.environment)
        self.accounts_client = build_accounts_locust_gateway_http_client(self.user.environment)
        self.documents_client = build_documents_locust_gateway_http_client(self.user.environment)
        self.operations_client = build_operations_locust_gateway_http_client(self.user.environment)
