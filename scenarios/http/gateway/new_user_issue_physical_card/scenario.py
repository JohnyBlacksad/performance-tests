"""Сценарий нагрузочного тестирования: выпуск физической карты новым пользователем.

Модуль содержит сценарий для Locust, который тестирует последовательность:
- Создание нового пользователя
- Открытие дебетового счёта
- Выпуск физической карты

Сценарий использует последовательное выполнение задач (SequentialTaskSet).
"""

from locust import task
from tools.locust.user import LocustBaseUser
from clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema
from clients.http.gateway.accounts.schema import OpenDebitCardAccountResponseSchema

class IssuePhysicalCardSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    """Последовательный набор задач для выпуска физической карты.

    Выполняет задачи строго по порядку: создание пользователя → открытие счёта → выпуск карты.
    Каждая задача использует результат предыдущей.

    Attributes:
        create_user_response: Ответ на запрос создания пользователя.
        open_account_response: Ответ на запрос открытия счёта.
    """
    create_user_response: CreateUserResponseSchema | None = None
    open_account_response: OpenDebitCardAccountResponseSchema | None

    @task
    def create_user(self):
        """Создать нового пользователя.

        Выполняет HTTP запрос на создание пользователя и сохраняет
        ответ для последующих задач.
        """
        self.create_user_response = self.user_client.create_user()

    @task
    def open_debit_account(self):
        """Открыть дебетовый счёт для созданного пользователя.

        Выполняет HTTP запрос на открытие дебетового счёта.
        Пропускает задачу, если пользователь не был создан.
        """
        if not self.create_user_response:
            return

        self.open_account_response = self.accounts_client.open_debit_card_account(
            self.create_user_response.user.id)

    @task
    def create_physical_card(self):
        """Выпустить физическую карту на открытый счёт.

        Выполняет HTTP запрос на выпуск физической карты.
        Пропускает задачу, если счёт или пользователь не были созданы.
        """
        if not self.open_account_response:
            return

        if not self.create_user_response:
            return

        self.cards_client.issue_physical_card(
            user_id=self.create_user_response.user.id,
            account_id=self.open_account_response.account.id
        )



class IssuePhysicalCardScenarioUser(LocustBaseUser):
    """Пользователь для сценария выпуска физической карты.

    Использует последовательный набор задач IssuePhysicalCardSequentialTaskSet
    для тестирования полного пути выпуска физической карты.
    """
    tasks = [IssuePhysicalCardSequentialTaskSet]