"""Сценарий нагрузочного тестирования: покупочная операция пользователя.

Модуль содержит сценарий для Locust, который тестирует покупочные операции:
- Совершение покупочной операции по карте
- Получение счетов пользователя
- Получение операций и сводки

Сценарий использует предварительно созданные данные (seed) пользователя
с существующими кредитными счетами и картами.
"""

from locust import task, events
from locust.env import Environment
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser
from seeds.scenarios.existing_user_make_purchase_operation import ExistingUserMakePurchaseOperationSeedsScenario
from clients.http.gateway.locust import GatewayHTTPTaskSet

@events.init.add_listener
def init(environment: Environment, **kwargs):
    """Инициализировать сценарий и загрузить seed-данные пользователя.

    Создаёт экземпляр ExistingUserMakePurchaseOperationSeedsScenario, генерирует
    тестовые данные и сохраняет их в окружении Locust.

    Args:
        environment: Экземпляр окружения Locust.
        **kwargs: Дополнительные аргументы от Locust.
    """
    seeds_scenario = ExistingUserMakePurchaseOperationSeedsScenario()
    seeds_scenario.build()

    environment.seeds = seeds_scenario.load() # type: ignore

class ExistingUserMakePurchaseOperationTaskSet(GatewayHTTPTaskSet):
    """Набор задач для тестирования покупочных операций пользователя.

    Выполняет запросы на совершение операций и получение данных
    через HTTP Gateway API.

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

    @task(1)
    def make_purchase_operation(self):
        """Совершить покупочную операцию по кредитной карте.

        Выполняет HTTP запрос на совершение покупки по первой
        физической карте первого кредитного счёта пользователя.
        """
        self.operations_client.make_purchase_operation(
            card_id=self.seed_user.credit_card_accounts[0].physical_cards[0].card_id,
            account_id=self.seed_user.credit_card_accounts[0].account_id
        )

    @task(2)
    def get_accounts(self):
        """Получить список счетов пользователя.

        Выполняет HTTP запрос на получение всех счетов пользователя.
        """
        self.accounts_client.get_account(user_id=self.seed_user.user_id)

    @task(2)
    def get_operations(self):
        """Получить список операций по кредитному счёту.

        Выполняет HTTP запрос на получение операций для первого
        кредитного счёта пользователя.
        """
        self.operations_client.get_operations(account_id=self.seed_user.credit_card_accounts[0].account_id)

    @task(2)
    def get_operation_summary(self):
        """Получить сводку по операциям кредитного счёта.

        Выполняет HTTP запрос на получение сводки по операциям
        для первого кредитного счёта пользователя.
        """
        self.operations_client.get_operations_summary(account_id=self.seed_user.credit_card_accounts[0].account_id)


class ExistingUserMakePurchaseOperationUser(LocustBaseUser):
    """Пользователь для сценария покупочных операций.

    Использует набор задач ExistingUserMakePurchaseOperationTaskSet
    для тестирования endpoints операций.
    """
    tasks = [ExistingUserMakePurchaseOperationTaskSet]