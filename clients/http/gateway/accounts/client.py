"""Клиент для работы с Accounts Gateway API.

Модуль предоставляет класс AccountsGatewayHTTPClient для управления счетами:
- Получение счетов пользователя
- Открытие различных типов счетов (депозитные, накопительные, дебетовые, кредитные)

Пример использования:
    >>> client = build_accounts_gateway_http_client()
    >>> accounts = client.get_account(user_id='u123')
    >>> new_account = client.open_deposit_account(user_id='u123')
"""

from httpx import Response, QueryParams
from locust.env import Environment
from clients.http.base_client import BaseHTTPClient, HTTPClientExtensions
from clients.http.gateway.gateway_client import build_gateway_http_client, build_gateway_locust_http_client
from .schema import (
    GetAccountsQuerySchema,
    GetAccountResponseSchema,
    OpenSavingAccountRequestSchema,
    OpenSavingAccountResponseSchema,
    OpenDepositAccountRequestSchema,
    OpenDepositAccountResponseSchema,
    OpenDebitCardAccountRequestSchema,
    OpenDebitCardAccountResponseSchema,
    OpenCreditCardAccountRequestSchema,
    OpenCreditCardAccountResponseSchema
)

class AccountsGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для Accounts Gateway API.

    Предоставляет методы для получения и открытия счетов различных типов.

    Пример использования:
        >>> client = build_accounts_gateway_http_client()
        >>> accounts = client.get_account(user_id='u123')
        >>> new_account = client.open_deposit_account(user_id='u123')
    """

    def get_account_api(self, query: GetAccountsQuerySchema) -> Response:
        """Получить счета пользователя (API-метод).

        Отправляет GET-запрос для получения списка всех счетов пользователя.

        Args:
            query: Модель параметров запроса (GetAccountsQuerySchema).

        Returns:
            HTTP-ответ со списком счетов.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> query = GetAccountsQuerySchema(user_id='u123')
            >>> response = client.get_account_api(query)
        """
        return self.get('accounts', params=QueryParams(**query.model_dump(by_alias=True)),
                        extensions=HTTPClientExtensions(route='accounts'))

    def get_account(self, user_id: str) -> GetAccountResponseSchema:
        """Получить счета пользователя (высокоуровневый метод).

        Создаёт и отправляет запрос на получение счетов пользователя,
        возвращая их в виде модели GetAccountResponseSchema.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            Модель GetAccountResponseSchema со списком счетов.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> accounts = client.get_account(user_id='u123')
            >>> print(accounts.accounts[0].balance)
        """
        response = self.get_account_api(GetAccountsQuerySchema(user_id=user_id)) # type: ignore
        return GetAccountResponseSchema.model_validate_json(response.text)

    def open_deposit_account_api(self, request: OpenDepositAccountRequestSchema) -> Response:
        """Открыть депозитный счёт (API-метод).

        Отправляет POST-запрос на открытие депозитного счёта.

        Args:
            request: Модель запроса на открытие депозитного счёта
                     (OpenDepositAccountRequestSchema).

        Returns:
            HTTP-ответ с результатом открытия счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> request = OpenDepositAccountRequestSchema(user_id='u123')
            >>> response = client.open_deposit_account_api(request)
        """
        return self.post('accounts/open-deposit-account', json=request.model_dump(by_alias=True))

    def open_deposit_account(self, user_id: str) -> OpenDepositAccountResponseSchema:
        """Открыть депозитный счёт (высокоуровневый метод).

        Создаёт и отправляет запрос на открытие депозитного счёта,
        возвращая данные счёта в виде модели OpenDepositAccountResponseSchema.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            Модель OpenDepositAccountResponseSchema с данными открытого счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> account = client.open_deposit_account(user_id='u123')
            >>> print(account.account.id)
        """
        request = OpenDepositAccountRequestSchema(user_id=user_id) # type: ignore
        response = self.open_deposit_account_api(request)
        return OpenDepositAccountResponseSchema.model_validate_json(response.text)

    def open_saving_account_api(self, request: OpenSavingAccountRequestSchema) -> Response:
        """Открыть накопительный счёт (API-метод).

        Отправляет POST-запрос на открытие накопительного счёта.

        Args:
            request: Модель запроса на открытие накопительного счёта
                     (OpenSavingAccountRequestSchema).

        Returns:
            HTTP-ответ с результатом открытия счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> request = OpenSavingAccountRequestSchema(user_id='u123')
            >>> response = client.open_saving_account_api(request)
        """
        return self.post('accounts/open-savings-account', json=request.model_dump(by_alias=True))

    def open_saving_account(self, user_id: str) -> OpenSavingAccountResponseSchema:
        """Открыть накопительный счёт (высокоуровневый метод).

        Создаёт и отправляет запрос на открытие накопительного счёта,
        возвращая данные счёта в виде модели OpenSavingAccountResponseSchema.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            Модель OpenSavingAccountResponseSchema с данными открытого счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> account = client.open_saving_account(user_id='u123')
            >>> print(account.account.balance)
        """
        request = OpenSavingAccountRequestSchema(user_id=user_id) # type: ignore
        response = self.open_saving_account_api(request)
        return OpenSavingAccountResponseSchema.model_validate_json(response.text)

    def open_debit_card_account_api(self, request: OpenDebitCardAccountRequestSchema) -> Response:
        """Открыть дебетовый счёт (API-метод).

        Отправляет POST-запрос на открытие дебетового счёта.

        Args:
            request: Модель запроса на открытие дебетового счёта
                     (OpenDebitCardAccountRequestSchema).

        Returns:
            HTTP-ответ с результатом открытия счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> request = OpenDebitCardAccountRequestSchema(user_id='u123')
            >>> response = client.open_debit_card_account_api(request)
        """
        return self.post('accounts/open-debit-card-account', json=request.model_dump(by_alias=True))

    def open_debit_card_account(self, user_id: str) -> OpenDebitCardAccountResponseSchema:
        """Открыть дебетовый счёт (высокоуровневый метод).

        Создаёт и отправляет запрос на открытие дебетового счёта,
        возвращая данные счёта в виде модели OpenDebitCardAccountResponseSchema.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            Модель OpenDebitCardAccountResponseSchema с данными открытого счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> account = client.open_debit_card_account(user_id='u123')
            >>> print(account.account.type)
        """
        request = OpenDebitCardAccountRequestSchema(user_id=user_id) # type: ignore
        response = self.open_debit_card_account_api(request)
        return OpenDebitCardAccountResponseSchema.model_validate_json(response.text)

    def open_credit_card_account_api(self, request: OpenCreditCardAccountRequestSchema) -> Response:
        """Открыть кредитный счёт (API-метод).

        Отправляет POST-запрос на открытие кредитного счёта.

        Args:
            request: Модель запроса на открытие кредитного счёта
                     (OpenCreditCardAccountRequestSchema).

        Returns:
            HTTP-ответ с результатом открытия счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> request = OpenCreditCardAccountRequestSchema(user_id='u123')
            >>> response = client.open_credit_card_account_api(request)
        """
        return self.post('accounts/open-credit-card-account', json=request.model_dump(by_alias=True))

    def open_credit_card_account(self, user_id: str) -> OpenCreditCardAccountResponseSchema:
        """Открыть кредитный счёт (высокоуровневый метод).

        Создаёт и отправляет запрос на открытие кредитного счёта,
        возвращая данные счёта в виде модели OpenCreditCardAccountResponseSchema.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            Модель OpenCreditCardAccountResponseSchema с данными открытого счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> account = client.open_credit_card_account(user_id='u123')
            >>> print(account.account.balance)
        """
        request = OpenCreditCardAccountRequestSchema(user_id=user_id) # type: ignore
        response = self.open_credit_card_account_api(request)
        return OpenCreditCardAccountResponseSchema.model_validate_json(response.text)


def build_accounts_gateway_http_client() -> AccountsGatewayHTTPClient:
    """Создать HTTP-клиент для Accounts Gateway API.

    Возвращает настроенный экземпляр AccountsGatewayHTTPClient для работы
    с API управления счетами.

    Returns:
        Настроенный экземпляр AccountsGatewayHTTPClient.

    Example:
        >>> client = build_accounts_gateway_http_client()
        >>> accounts = client.get_account(user_id='u123')
    """
    return AccountsGatewayHTTPClient(client=build_gateway_http_client())

def build_accounts_locust_gateway_http_client(environment: Environment) -> AccountsGatewayHTTPClient:
    """Создать HTTP-клиент для Accounts Gateway API с интеграцией Locust.

    Возвращает настроенный экземпляр AccountsGatewayHTTPClient для работы
    с API управления счетами через Locust (сбор метрик).

    Args:
        environment: Окружение Locust для настройки клиента.

    Returns:
        Настроенный экземпляр AccountsGatewayHTTPClient с Locust-интерцептором.

    Example:
        >>> client = build_accounts_locust_gateway_http_client(environment)
        >>> accounts = client.get_account(user_id='u123')
    """
    return AccountsGatewayHTTPClient(client=build_gateway_locust_http_client(environment))
