"""gRPC клиент для Accounts Gateway сервиса.

Модуль предоставляет класс AccountsGatewayGRPCClient для управления счетами:
- Получение счетов пользователя
- Открытие различных типов счетов (депозитные, накопительные, дебетовые, кредитные)

Пример использования:
    >>> client = build_accounts_gateway_grpc_client()
    >>> accounts = client.get_accounts(user_id='u123')
    >>> new_account = client.open_deposit_account(user_id='u123')
"""

from grpc import Channel
from locust.env import Environment
from clients.grpc.client import GRPCClient, build_gateway_grpc_client, build_gateway_locust_grpc_client
from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub
from contracts.services.gateway.accounts.rpc_get_accounts_pb2 import GetAccountsRequest, GetAccountsResponse
from contracts.services.gateway.accounts.rpc_open_credit_card_account_pb2 import OpenCreditCardAccountRequest, OpenCreditCardAccountResponse
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountRequest, OpenDebitCardAccountResponse
from contracts.services.gateway.accounts.rpc_open_deposit_account_pb2 import OpenDepositAccountRequest, OpenDepositAccountResponse
from contracts.services.gateway.accounts.rpc_open_savings_account_pb2 import OpenSavingsAccountRequest, OpenSavingsAccountResponse
from tools.fakers import faker_ru

class AccountsGatewayGRPCClient(GRPCClient):
    """gRPC клиент для Accounts Gateway сервиса.

    Предоставляет методы для получения и открытия счетов различных типов.

    Example:
        >>> client = build_accounts_gateway_grpc_client()
        >>> accounts = client.get_accounts(user_id='u123')
    """
    def __init__(self, channel: Channel) -> None:
        """Инициализировать клиент для работы со счетами.

        Args:
            channel: gRPC канал для подключения.
        """
        super().__init__(channel)
        self.stub = AccountsGatewayServiceStub(channel)

    def get_accounts_api(self, request: GetAccountsRequest) -> GetAccountsResponse:
        """Получить счета пользователя (низкоуровневый метод).

        Args:
            request: Запрос с идентификатором пользователя.

        Returns:
            Ответ со списком счетов.
        """
        return self.stub.GetAccounts(request)

    def open_credit_card_account_api(self, request: OpenCreditCardAccountRequest) -> OpenCreditCardAccountResponse:
        """Открыть кредитный счёт (низкоуровневый метод).

        Args:
            request: Запрос на открытие кредитного счёта.

        Returns:
            Ответ с данными открытого счёта.
        """
        return self.stub.OpenCreditCardAccount(request)

    def open_debit_card_account_api(self, request: OpenDebitCardAccountRequest) -> OpenDebitCardAccountResponse:
        """Открыть дебетовый счёт (низкоуровневый метод).

        Args:
            request: Запрос на открытие дебетового счёта.

        Returns:
            Ответ с данными открытого счёта.
        """
        return self.stub.OpenDebitCardAccount(request)

    def open_deposit_account_api(self, request: OpenDepositAccountRequest) -> OpenDepositAccountResponse:
        """Открыть депозитный счёт (низкоуровневый метод).

        Args:
            request: Запрос на открытие депозитного счёта.

        Returns:
            Ответ с данными открытого счёта.
        """
        return self.stub.OpenDepositAccount(request)

    def open_saving_account_api(self, request: OpenSavingsAccountRequest) -> OpenSavingsAccountResponse:
        """Открыть накопительный счёт (низкоуровневый метод).

        Args:
            request: Запрос на открытие накопительного счёта.

        Returns:
            Ответ с данными открытого счёта.
        """
        return self.stub.OpenSavingsAccount(request)

    def get_accounts(self, user_id: str) -> GetAccountsResponse:
        """Получить счета пользователя.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Ответ со списком счетов.
        """
        request = GetAccountsRequest(user_id=user_id)
        return self.get_accounts_api(request)

    def open_credit_card_account(self, user_id: str) -> OpenCreditCardAccountResponse:
        """Открыть кредитный счёт.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Ответ с данными открытого счёта.
        """
        request = OpenCreditCardAccountRequest(user_id=user_id)
        return self.open_credit_card_account_api(request)

    def open_debit_card_account(self, user_id: str) -> OpenDebitCardAccountResponse:
        """Открыть дебетовый счёт.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Ответ с данными открытого счёта.
        """
        request = OpenDebitCardAccountRequest(user_id=user_id)
        return self.open_debit_card_account_api(request)

    def open_deposit_account(self, user_id: str) -> OpenDepositAccountResponse:
        """Открыть депозитный счёт.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Ответ с данными открытого счёта.
        """
        request = OpenDepositAccountRequest(user_id=user_id)
        return self.open_deposit_account_api(request)

    def open_saving_account(self, user_id: str) -> OpenSavingsAccountResponse:
        """Открыть накопительный счёт.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Ответ с данными открытого счёта.
        """
        request = OpenSavingsAccountRequest(user_id=user_id)
        return self.open_saving_account_api(request)

def build_accounts_gateway_client() -> AccountsGatewayGRPCClient:
    """Создать gRPC клиент для Accounts Gateway.

    Returns:
        Настроенный экземпляр AccountsGatewayGRPCClient.
    """
    return AccountsGatewayGRPCClient(channel=build_gateway_grpc_client())

def build_accounts_gateway_locust_grpc_client(environment: Environment) -> AccountsGatewayGRPCClient:
    """Создать gRPC клиент с интеграцией Locust для Accounts Gateway.

    Args:
        environment: Экземпляр окружения Locust.

    Returns:
        Настроенный экземпляр AccountsGatewayGRPCClient с интерцептором.
    """
    return AccountsGatewayGRPCClient(channel=build_gateway_locust_grpc_client(environment))