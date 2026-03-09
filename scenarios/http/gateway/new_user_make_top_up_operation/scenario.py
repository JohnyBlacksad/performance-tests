"""Сценарий нагрузочного тестирования: операция пополнения новым пользователем.

Модуль содержит сценарий для Locust, который тестирует последовательность:
- Создание нового пользователя
- Открытие дебетового счёта
- Операция пополнения счёта
- Получение операций и сводки

Сценарий использует последовательное выполнение задач (SequentialTaskSet).
"""

from locust import task
from tools.locust.user import LocustBaseUser
from clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema
from clients.http.gateway.accounts.schema import OpenDebitCardAccountResponseSchema
from clients.http.gateway.operations.schema import MakeTopUpOperationResponseSchema

class MakeTopUpOperationSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    """Последовательный набор задач для тестирования операции пополнения.

    Выполняет задачи строго по порядку: создание пользователя → открытие счёта →
    пополнение → получение операций. Каждая задача использует результат предыдущей.

    Attributes:
        create_user_response: Ответ на запрос создания пользователя.
        open_account_response: Ответ на запрос открытия счёта.
        operation_response: Ответ на запрос операции пополнения.
    """
    create_user_response: CreateUserResponseSchema | None = None
    open_account_response: OpenDebitCardAccountResponseSchema | None = None
    operation_response: MakeTopUpOperationResponseSchema | None = None

    @task
    def create_user(self):
        """Создать нового пользователя.

        Выполняет HTTP запрос на создание пользователя и сохраняет
        ответ для последующих задач.
        """
        self.create_user_response = self.user_client.create_user()

    @task
    def open_debit_card_account(self):
        """Открыть дебетовый счёт для созданного пользователя.

        Выполняет HTTP запрос на открытие дебетового счёта.
        Пропускает задачу, если пользователь не был создан.
        """
        if not self.create_user_response:
            return

        self.open_account_response = self.accounts_client.open_debit_card_account(self.create_user_response.user.id)

    @task
    def make_top_up_operation(self):
        """Совершить операцию пополнения счёта.

        Выполняет HTTP запрос на пополнение счёта через первую карту.
        Пропускает задачу, если счёт не был открыт.
        """
        if not self.open_account_response:
            return

        self.operation_response = self.operations_client.make_top_up_operation(
            card_id=self.open_account_response.account.cards[0].id,
            account_id=self.open_account_response.account.id)

    @task
    def get_operations(self):
        """Получить список операций по счёту.

        Выполняет HTTP запрос на получение операций для открытого счёта.
        Пропускает задачу, если счёт не был открыт.
        """
        if not self.open_account_response:
            return

        self.operations_client.get_operations(account_id=self.open_account_response.account.id)


    @task
    def get_operations_summary(self):
        """Получить сводку по операциям счёта.

        Выполняет HTTP запрос на получение сводки по операциям.
        Пропускает задачу, если счёт не был открыт.
        """
        if not self.open_account_response:
            return

        self.operations_client.get_operations_summary(self.open_account_response.account.id)

    @task
    def get_operation(self):
        """Получить детальную информацию об операции пополнения.

        Выполняет HTTP запрос на получение конкретной операции.
        Пропускает задачу, если операция не была совершена.
        """
        if not self.operation_response:
            return

        self.operations_client.get_operation(self.operation_response.operation.id)


class MakeTopUpOperationUser(LocustBaseUser):
    """Пользователь для сценария операции пополнения.

    Использует последовательный набор задач MakeTopUpOperationSequentialTaskSet
    для тестирования полного пути операции пополнения.
    """
    tasks = [MakeTopUpOperationSequentialTaskSet]