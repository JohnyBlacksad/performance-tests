"""Сценарий нагрузочного тестирования: получение документов пользователя.

Модуль содержит сценарий для Locust, который тестирует получение документов:
- Тарифный документ
- Договорный документ

Сценарий использует предварительно созданные данные (seed) пользователя
с существующими счетами и документами.
"""

from locust import task, events
from locust.env import Environment
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser
from seeds.scenarios.existing_user_get_documents import ExistingUserGetDocumentsSeedScenario
from clients.http.gateway.locust import GatewayHTTPTaskSet

@events.init.add_listener
def init(environment: Environment, **kwargs):
    """Инициализировать сценарий и загрузить seed-данные пользователя.

    Создаёт экземпляр ExistingUserGetDocumentsSeedScenario, генерирует
    тестовые данные и сохраняет их в окружении Locust.

    Args:
        environment: Экземпляр окружения Locust.
        **kwargs: Дополнительные аргументы от Locust.
    """
    seed_user: ExistingUserGetDocumentsSeedScenario = ExistingUserGetDocumentsSeedScenario()
    seed_user.build()

    environment.seed = seed_user.load() # type: ignore


class GetDocumentsTaskSet(GatewayHTTPTaskSet):
    """Набор задач для тестирования получения документов пользователя.

    Выполняет запросы на получение счетов и документов пользователя
    через HTTP Gateway API.

    Attributes:
        seed_user: Данные предварительно созданного пользователя.
    """
    seed_user: SeedUserResult

    def on_start(self) -> None:
        """Инициализировать данные пользователя при старте задачи.

        Загружает следующего пользователя из seed-данных.
        """
        super().on_start()
        self.seed_user = self.user.environment.seed.get_next_user()

    @task(1)
    def get_accounts(self):
        """Получить список счетов пользователя.

        Выполняет HTTP запрос на получение всех счетов пользователя.
        """
        self.accounts_client.get_account(user_id=self.seed_user.user_id)

    @task(2)
    def get_tariff_document(self):
        """Получить тарифный документ сберегательного счёта.

        Выполняет HTTP запрос на получение тарифного документа
        для первого сберегательного счёта пользователя.
        """
        self.documents_client.get_tariff_document(account_id=self.seed_user.saving_accounts[0].account_id)

    @task(2)
    def get_contract_document(self):
        """Получить договорный документ дебетового счёта.

        Выполняет HTTP запрос на получение договорного документа
        для первого дебетового счёта пользователя.
        """
        self.documents_client.get_contract_document(account_id=self.seed_user.debit_card_accounts[0].account_id)



class GetDocumentsUser(LocustBaseUser):
    """Пользователь для сценария получения документов.

    Использует набор задач GetDocumentsTaskSet для тестирования
    endpoints получения документов.
    """
    tasks = [GetDocumentsTaskSet]