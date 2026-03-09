"""Сценарий нагрузочного тестирования: выпуск виртуальной карты.

Модуль содержит сценарий для Locust, который тестирует выпуск виртуальной карты:
- Получение счетов пользователя
- Выпуск виртуальной карты на дебетовый счёт

Сценарий использует предварительно созданные данные (seed) пользователя
с существующими дебетовыми счетами.
"""

from locust import task, events
from locust.env import Environment
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser
from seeds.scenarios.existing_user_issue_virtual_card import ExistingUserIssueVirtualCardSeedsScenario
from clients.grpc.gateway.locust import GatewayGRPCTaskSet

@events.init.add_listener
def init(environment: Environment, **kwargs):
    """Инициализировать сценарий и загрузить seed-данные пользователя.

    Создаёт экземпляр ExistingUserIssueVirtualCardSeedsScenario, генерирует
    тестовые данные и сохраняет их в окружении Locust.

    Args:
        environment: Экземпляр окружения Locust.
        **kwargs: Дополнительные аргументы от Locust.
    """
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    seeds_scenario.build()

    environment.seeds = seeds_scenario.load() # type: ignore

class IssueVirtualCardTaskSet(GatewayGRPCTaskSet):
    """Набор задач для тестирования выпуска виртуальной карты.

    Выполняет запросы на получение счетов и выпуск виртуальной карты
    через gRPC Gateway API.

    Attributes:
        seed_user: Данные предварительно созданного пользователя.
    """
    seed_user: SeedUserResult

    def on_start(self) -> None:
        """Инициализировать данные пользователя при старте задачи.

        Загружает случайного пользователя из seed-данных.
        """
        super().on_start()
        self.seed_user = self.user.environment.seeds.get_random_user()

    @task(2)
    def get_account(self):
        """Получить список счетов пользователя.

        Выполняет gRPC запрос на получение всех счетов пользователя.
        """
        self.accounts_client.get_accounts(user_id=self.seed_user.user_id)

    @task(1)
    def issue_virtual_card(self):
        """Выпустить виртуальную карту на дебетовый счёт.

        Выполняет gRPC запрос на выпуск виртуальной карты
        для первого дебетового счёта пользователя.
        """
        self.cards_client.issue_virtual_card(
            user_id=self.seed_user.user_id,
            account_id=self.seed_user.debit_card_accounts[0].account_id
        )



class IssueVirtualCardUser(LocustBaseUser):
    """Пользователь для сценария выпуска виртуальной карты.

    Использует набор задач IssueVirtualCardTaskSet для тестирования
    endpoints выпуска виртуальной карты.
    """
    tasks = [IssueVirtualCardTaskSet]