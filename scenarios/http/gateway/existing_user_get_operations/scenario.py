"""Сценарий нагрузочного тестирования: получение операций пользователя.

Модуль содержит сценарий для Locust, который тестирует получение операций:
- Список операций по счёту
- Сводка по операциям

Сценарий использует предварительно созданные данные (seed) пользователя
с существующими кредитными счетами.
"""

from locust import task, events
from locust.env import Environment
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser
from seeds.scenarios.existing_user_get_operations import ExistingUserGetOperationsSeedsScenario
from clients.http.gateway.locust import GatewayHTTPTaskSet

@events.init.add_listener
def init(environment: Environment, **kwargs):
    """Инициализировать сценарий и загрузить seed-данные пользователя.

    Создаёт экземпляр ExistingUserGetOperationsSeedsScenario, генерирует
    тестовые данные и сохраняет их в окружении Locust.

    Args:
        environment: Экземпляр окружения Locust.
        **kwargs: Дополнительные аргументы от Locust.
    """
    seed_user: ExistingUserGetOperationsSeedsScenario = ExistingUserGetOperationsSeedsScenario()
    seed_user.build()

    environment.seed = seed_user.load() # type: ignore

class GetOperationsTaskSet(GatewayHTTPTaskSet):
    """Набор задач для тестирования получения операций пользователя.

    Выполняет запросы на получение счетов и операций пользователя
    через HTTP Gateway API.

    Attributes:
        seed_users: Данные предварительно созданного пользователя.
    """
    seed_users: SeedUserResult

    def on_start(self) -> None:
        """Инициализировать данные пользователя при старте задачи.

        Загружает случайного пользователя из seed-данных.
        """
        super().on_start()
        self.seed_users = self.user.environment.seed.get_random_user()

    @task(1)
    def get_accounts(self):
        """Получить список счетов пользователя.

        Выполняет HTTP запрос на получение всех счетов пользователя.
        """
        self.accounts_client.get_account(user_id=self.seed_users.user_id)

    @task(2)
    def get_operations(self):
        """Получить список операций по кредитному счёту.

        Выполняет HTTP запрос на получение операций для первого
        кредитного счёта пользователя.
        """
        self.operations_client.get_operations(account_id=self.seed_users.credit_card_accounts[0].account_id)

    @task(3)
    def get_operation_summary(self):
        """Получить сводку по операциям кредитного счёта.

        Выполняет HTTP запрос на получение сводки по операциям
        для первого кредитного счёта пользователя.
        """
        self.operations_client.get_operations_summary(account_id=self.seed_users.credit_card_accounts[0].account_id)


class GetOperationsUser(LocustBaseUser):
    """Пользователь для сценария получения операций.

    Использует набор задач GetOperationsTaskSet для тестирования
    endpoints получения операций.
    """
    tasks = [GetOperationsTaskSet]