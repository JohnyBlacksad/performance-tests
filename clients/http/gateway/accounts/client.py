"""Клиент для работы с Accounts Gateway API.

Модуль предоставляет класс AccountsGatewayHTTPClient для управления счетами:
- Получение счетов пользователя
- Открытие различных типов счетов (депозитные, накопительные, дебетовые, кредитные)

Пример использования:
    >>> client = build_accounts_gateway_http_client()
    >>> accounts = client.get_account(user_id='u123')
    >>> new_account = client.open_deposit_account(user_id='u123')
"""

from httpx import Response
from clients.http.base_client import BaseHTTPClient, QueryParams
from typing import TypedDict
from clients.http.gateway.cards.client import CardDict
from clients.http.gateway.gateway_client import build_gateway_http_client


class GetAccountsQueryDict(TypedDict):
    """Словарь параметров запроса для получения счетов.

    Attributes:
        userId: Уникальный идентификатор пользователя.
    """
    userId: str


class OpenDepositAccountRequestDict(TypedDict):
    """Словарь запроса на открытие депозитного счёта.

    Attributes:
        userId: Уникальный идентификатор пользователя.
    """
    userId: str


class OpenSavingAccountRequestDict(TypedDict):
    """Словарь запроса на открытие накопительного счёта.

    Attributes:
        userId: Уникальный идентификатор пользователя.
    """
    userId: str


class OpenDebitCardAccountRequestDict(TypedDict):
    """Словарь запроса на открытие дебетового счёта.

    Attributes:
        userId: Уникальный идентификатор пользователя.
    """
    userId: str


class OpenCreditCardAccountRequestDict(TypedDict):
    """Словарь запроса на открытие кредитного счёта.

    Attributes:
        userId: Уникальный идентификатор пользователя.
    """
    userId: str


class AccountDict(TypedDict):
    """Словарь, представляющий данные счёта.

    Attributes:
        id: Уникальный идентификатор счёта.
        type: Тип счёта.
        cards: Список карт, привязанных к счёту.
        status: Статус счёта.
        balance: Баланс счёта.
    """
    id: str
    type: str
    cards: list[CardDict]
    status: str
    balance: float


class GetAccountResponseDict(TypedDict):
    """Словарь ответа на получение счетов пользователя.

    Attributes:
        accounts: Список счетов пользователя.
    """
    accounts: list[AccountDict]


class OpenDepositAccountResponseDict(TypedDict):
    """Словарь ответа на открытие депозитного счёта.

    Attributes:
        account: Данные открытого счёта.
    """
    account: AccountDict


class OpenSavingAccountResponseDict(TypedDict):
    """Словарь ответа на открытие накопительного счёта.

    Attributes:
        account: Данные открытого счёта.
    """
    account: AccountDict


class OpenDebitCardAccountResponseDict(TypedDict):
    """Словарь ответа на открытие дебетового счёта.

    Attributes:
        account: Данные открытого счёта.
    """
    account: AccountDict


class OpenCreditCardAccountResponseDict(TypedDict):
    """Словарь ответа на открытие кредитного счёта.

    Attributes:
        account: Данные открытого счёта.
    """
    account: AccountDict


class AccountsGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для Accounts Gateway API.

    Предоставляет методы для получения и открытия счетов различных типов.

    Пример использования:
        >>> client = build_accounts_gateway_http_client()
        >>> accounts = client.get_account(user_id='u123')
        >>> new_account = client.open_deposit_account(user_id='u123')
    """

    def get_account_api(self, query: GetAccountsQueryDict) -> Response:
        """Получить счета пользователя (API-метод).

        Отправляет GET-запрос для получения списка всех счетов пользователя.

        Args:
            query: Параметры запроса (userId).

        Returns:
            HTTP-ответ со списком счетов.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> response = client.get_account_api({'userId': 'u123'})
        """
        return self.get('accounts', params=QueryParams(**query))

    def get_account(self, user_id: str) -> GetAccountResponseDict:
        """Получить счета пользователя (высокоуровневый метод).

        Создаёт и отправляет запрос на получение счетов пользователя,
        возвращая их в виде словаря.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            Словарь со списком счетов пользователя.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> accounts = client.get_account(user_id='u123')
            >>> print(accounts['accounts'][0]['balance'])
        """
        response = self.get_account_api(GetAccountsQueryDict(userId=user_id))
        return response.json()

    def open_deposit_account_api(self, request: OpenDepositAccountRequestDict) -> Response:
        """Открыть депозитный счёт (API-метод).

        Отправляет POST-запрос на открытие депозитного счёта.

        Args:
            request: Словарь с данными для открытия депозитного счёта (userId).

        Returns:
            HTTP-ответ с результатом открытия счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> response = client.open_deposit_account_api({'userId': 'u123'})
        """
        return self.post('accounts/open_deposit_account', json=request)

    def open_deposit_account(self, user_id: str) -> OpenDepositAccountResponseDict:
        """Открыть депозитный счёт (высокоуровневый метод).

        Создаёт и отправляет запрос на открытие депозитного счёта,
        возвращая данные счёта в виде словаря.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            Словарь с данными открытого счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> account = client.open_deposit_account(user_id='u123')
            >>> print(account['account']['id'])
        """
        request = OpenDepositAccountRequestDict(userId=user_id)
        response = self.open_deposit_account_api(request)
        return response.json()

    def open_saving_account_api(self, request: OpenSavingAccountRequestDict) -> Response:
        """Открыть накопительный счёт (API-метод).

        Отправляет POST-запрос на открытие накопительного счёта.

        Args:
            request: Словарь с данными для открытия накопительного счёта (userId).

        Returns:
            HTTP-ответ с результатом открытия счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> response = client.open_saving_account_api({'userId': 'u123'})
        """
        return self.post('accounts/open-savings-account', json=request)

    def open_saving_account(self, user_id: str) -> OpenSavingAccountResponseDict:
        """Открыть накопительный счёт (высокоуровневый метод).

        Создаёт и отправляет запрос на открытие накопительного счёта,
        возвращая данные счёта в виде словаря.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            Словарь с данными открытого счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> account = client.open_saving_account(user_id='u123')
            >>> print(account['account']['balance'])
        """
        request = OpenSavingAccountRequestDict(userId=user_id)
        response = self.open_saving_account_api(request)
        return response.json()

    def open_debit_card_account_api(self, request: OpenDebitCardAccountRequestDict) -> Response:
        """Открыть дебетовый счёт (API-метод).

        Отправляет POST-запрос на открытие дебетового счёта.

        Args:
            request: Словарь с данными для открытия дебетового счёта (userId).

        Returns:
            HTTP-ответ с результатом открытия счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> response = client.open_debit_card_account_api({'userId': 'u123'})
        """
        return self.post('accounts/open-debit-card-account', json=request)

    def open_debit_card_account(self, user_id: str) -> OpenDebitCardAccountResponseDict:
        """Открыть дебетовый счёт (высокоуровневый метод).

        Создаёт и отправляет запрос на открытие дебетового счёта,
        возвращая данные счёта в виде словаря.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            Словарь с данными открытого счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> account = client.open_debit_card_account(user_id='u123')
            >>> print(account['account']['type'])
        """
        request = OpenDebitCardAccountRequestDict(userId=user_id)
        response = self.open_debit_card_account_api(request)
        return response.json()

    def open_credit_card_account_api(self, request: OpenCreditCardAccountRequestDict) -> Response:
        """Открыть кредитный счёт (API-метод).

        Отправляет POST-запрос на открытие кредитного счёта.

        Args:
            request: Словарь с данными для открытия кредитного счёта (userId).

        Returns:
            HTTP-ответ с результатом открытия счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> response = client.open_credit_card_account_api({'userId': 'u123'})
        """
        return self.post('accounts/open-credit-card-account', json=request)

    def open_credit_card_account(self, user_id: str) -> OpenCreditCardAccountResponseDict:
        """Открыть кредитный счёт (высокоуровневый метод).

        Создаёт и отправляет запрос на открытие кредитного счёта,
        возвращая данные счёта в виде словаря.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            Словарь с данными открытого счёта.

        Example:
            >>> client = build_accounts_gateway_http_client()
            >>> account = client.open_credit_card_account(user_id='u123')
            >>> print(account['account']['balance'])
        """
        request = OpenCreditCardAccountRequestDict(userId=user_id)
        response = self.open_credit_card_account_api(request)
        return response.json()


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
