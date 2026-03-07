"""Сценарий нагрузочного тестирования: получение документов.

Модуль содержит сценарий для Locust, который тестирует последовательность:
1. Создание пользователя
2. Открытие накопительного счёта
3. Получение тарифного и договорного документов

Пример запуска:
    locust -f scenarios/http/gateway/get_documents/scenario.py --host=http://localhost:8003
"""

from clients.http.gateway.accounts.schema import OpenSavingAccountResponseSchema
from clients.http.gateway.users.schema import CreateUserResponseSchema
from clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from locust import User, between, task


class GetDocumentsSequentsTaskSet(GatewayHTTPSequentialTaskSet):
    """Последовательный набор задач для тестирования получения документов.

    Выполняет цепочку действий:
    1. Создаёт пользователя
    2. Открывает накопительный счёт
    3. Получает тарифный и договорный документы

    Attributes:
        create_user_response: Данные созданного пользователя.
        open_saving_account_response: Данные открытого счёта.
    """
    create_user_response: CreateUserResponseSchema | None = None
    open_saving_account_response: OpenSavingAccountResponseSchema | None = None

    @task
    def create_user(self):
        """Создать нового пользователя."""
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

        self.documents_client.get_tariff_document(self.open_saving_account_response.account.id)
        self.documents_client.get_contract_document(self.open_saving_account_response.account.id)

class GetDocumentUser(User):
    """Пользователь для сценария тестирования получения документов.

    Attributes:
        host: Хост для подключения (localhost).
        tasks: Набор задач для выполнения.
        wait_time: Время ожидания между задачами (1-3 секунды).
    """
    host = 'localhost'
    tasks = [GetDocumentsSequentsTaskSet]
    wait_time = between(1, 3)