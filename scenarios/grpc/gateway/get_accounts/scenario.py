"""gRPC-сценарий для тестирования получения счетов пользователя.

Модуль содержит Locust-сценарий для последовательного выполнения:
- Создание пользователя
- Открытие кредитного и дебетового счетов
- Получение списка счетов

Пример использования:
    # Запуск через locust:
    # locust -f scenarios/grpc/gateway/get_accounts/scenario.py
"""

from locust import task
from tools.locust.user import LocustBaseUser
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse
from clients.grpc.gateway.locust import GatewayGRPCSequentialTaskSet


class GetAccountsSequentialTaskSet(GatewayGRPCSequentialTaskSet):
    """Последовательный набор задач для тестирования получения счетов.

    Выполняет сценарий:
    1. create_user — создание нового пользователя
    2. open_accounts — открытие кредитного и дебетового счетов
    3. get_accounts — получение списка счетов пользователя

    Attributes:
        create_user_response: Результат создания пользователя.

    Пример использования:
        >>> class MyUser(LocustBaseUser):
        ...     tasks = [GetAccountsSequentialTaskSet]
    """
    create_user_response: CreateUserResponse | None = None

    @task
    def create_user(self) -> None:
        """Создать нового пользователя.

        Отправляет gRPC-запрос на создание пользователя и сохраняет
        результат в create_user_response для последующих задач.

        Example:
            >>> taskset.create_user()
        """
        self.create_user_response = self.user_client.create_user()

    @task
    def open_accounts(self) -> None:
        """Открыть кредитный и дебетовый счета для пользователя.

        Если пользователь не был создан (create_user_response is None),
        задача завершается без выполнения.

        Example:
            >>> taskset.open_accounts()
        """
        if not self.create_user_response:
            return

        self.accounts_client.open_credit_card_account(self.create_user_response.user.id)
        self.accounts_client.open_debit_card_account(self.create_user_response.user.id)

    @task
    def get_accounts(self) -> None:
        """Получить список счетов пользователя.

        Если пользователь не был создан (create_user_response is None),
        задача завершается без выполнения.

        Example:
            >>> taskset.get_accounts()
        """
        if not self.create_user_response:
            return

        self.accounts_client.get_accounts(self.create_user_response.user.id)


class GetAccountsUser(LocustBaseUser):
    """Locust-пользователь для сценария получения счетов.

    Использует последовательный набор задач GetAccountsSequentialTaskSet
    для тестирования gRPC API получения счетов.

    Attributes:
        tasks: Список наборов задач для выполнения.

    Пример использования:
        # Запуск через locust:
        # locust -f scenarios/grpc/gateway/get_accounts/scenario.py
    """
    tasks = [GetAccountsSequentialTaskSet]
