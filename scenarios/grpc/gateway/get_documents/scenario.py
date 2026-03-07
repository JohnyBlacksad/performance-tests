"""gRPC сценарий нагрузочного тестирования: получение документов.

Модуль содержит сценарий для Locust, который тестирует последовательность:
1. Создание пользователя (gRPC)
2. Открытие накопительного счёта (gRPC)
3. Получение тарифного и договорного документов (gRPC)

Пример запуска:
    locust -f scenarios/grpc/gateway/get_documents/scenario.py
"""

from locust import User, between, task

from clients.grpc.gateway.locust import GatewayGRPCSequentialTaskSet
from contracts.services.gateway.accounts.rpc_open_savings_account_pb2 import OpenSavingsAccountResponse
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse


class GetDocumentsSequentialTaskSet(GatewayGRPCSequentialTaskSet):
    """Последовательный набор задач для gRPC тестирования получения документов.

    Выполняет цепочку действий:
    1. Создаёт пользователя через gRPC
    2. Открывает накопительный счёт через gRPC
    3. Получает тарифный и договорный документы через gRPC

    Attributes:
        create_user_response: Данные созданного пользователя.
        open_saving_account_response: Данные открытого счёта.
    """

    create_user_response: CreateUserResponse | None = None
    open_saving_account_response: OpenSavingsAccountResponse | None = None

    @task
    def create_user(self):
        """Создать нового пользователя через gRPC."""
        self.create_user_response = self.user_client.create_user()

    @task
    def open_saving_account(self):
        """Открыть накопительный счёт для созданного пользователя."""
        if not self.create_user_response:
            return

        self.open_saving_account_response = self.accounts_client.open_saving_account(self.create_user_response.user.id)

    @task
    def get_documents(self):
        """Получить тарифный и договорный документы для счёта."""
        if not self.open_saving_account_response:
            return

        self.documents_client.get_contract_document(self.open_saving_account_response.account.id)
        self.documents_client.get_tariff_document(self.open_saving_account_response.account.id)


class GetDocumentUser(User):
    """Пользователь для gRPC сценария тестирования получения документов.

    Attributes:
        host: Хост для подключения (localhost).
        tasks: Набор задач для выполнения.
        wait_time: Время ожидания между задачами (1-3 секунды).
    """
    host = 'localhost'
    tasks = [GetDocumentsSequentialTaskSet]
    wait_time = between(1, 3)