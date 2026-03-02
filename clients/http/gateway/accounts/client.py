from httpx import Response
from clients.http.base_client import BaseHTTPClient, QueryParams
from typing import TypedDict
from clients.http.gateway.cards.client import CardDict
from clients.http.gateway.gateway_client import build_gateway_http_client

class GetAccountsQueryDict(TypedDict):
    """Словарь параметров запроса для получения счетов."""

    userId: str

class OpenDepositAccountRequestDict(TypedDict):
    """Словарь запроса на открытие депозитного счёта."""

    userId: str

class OpenSavingAccountRequestDict(TypedDict):
    """Словарь запроса на открытие накопительного счёта."""

    userId: str

class OpenDebitCardAccountRequestDict(TypedDict):
    """Словарь запроса на открытие дебетового счёта."""

    userId: str

class OpenCreditCardAccountRequestDict(TypedDict):
    """Словарь запроса на открытие кредитного счёта."""

    userId: str

class AccountDict(TypedDict):
    id: str
    type: str
    cards: list[CardDict]
    status: str
    balance: float

class GetAccountResponseDict(TypedDict):
    accounts: list[AccountDict]

class OpenDepositAccountResponseDict(TypedDict):
    account: AccountDict

class OpenSavingAccountResponseDict(TypedDict):
    account: AccountDict

class OpenDebitCardAccountResponseDict(TypedDict):
    account: AccountDict

class OpenCreditCardAccountResponseDict(TypedDict):
    account: AccountDict

class AccountsGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для Accounts Gateway API."""

    def get_account_api(self, query: GetAccountsQueryDict) -> Response:
        """Получить счета пользователя.

        Args:
            query: Параметры запроса (userId).

        Returns:
            HTTP-ответ со списком счетов.
        """
        return self.get('accounts', params=QueryParams(**query))

    def get_account(self, user_id: str) -> GetAccountResponseDict:
        response = self.get_account_api(GetAccountsQueryDict(userId=user_id))
        return response.json()

    def open_deposit_account_api(self, request: OpenDepositAccountRequestDict) -> Response:
        """Открыть депозитный счёт.

        Args:
            request: Словарь с данными для открытия депозитного счёта.

        Returns:
            HTTP-ответ.
        """
        return self.post('accounts/open_deposit_account', json=request)

    def open_deposit_account(self, user_id: str) -> OpenDepositAccountResponseDict:
        request = OpenDepositAccountRequestDict(userId=user_id)
        response = self.open_deposit_account_api(request)
        return response.json()

    def open_saving_account_api(self, request: OpenSavingAccountRequestDict) -> Response:
        """Открыть накопительный счёт.

        Args:
            request: Словарь с данными для открытия накопительного счёта.

        Returns:
            HTTP-ответ.
        """
        return self.post('accounts/open-savings-account', json=request)

    def open_saving_account(self, user_id: str) -> OpenSavingAccountResponseDict:
        request = OpenSavingAccountRequestDict(userId=user_id)
        response = self.open_saving_account_api(request)
        return response.json()

    def open_debit_card_account_api(self, request: OpenDebitCardAccountRequestDict) -> Response:
        """Открыть дебетовый счёт.

        Args:
            request: Словарь с данными для открытия дебетового счёта.

        Returns:
            HTTP-ответ.
        """
        return self.post('accounts/open-debit-card-account', json=request)

    def open_debit_card_account(self, user_id: str) -> OpenDebitCardAccountResponseDict:
        request = OpenDebitCardAccountRequestDict(userId=user_id)
        response = self.open_debit_card_account_api(request)
        return response.json()

    def open_credit_card_account_api(self, request: OpenCreditCardAccountRequestDict) -> Response:
        """Открыть кредитный счёт.

        Args:
            request: Словарь с данными для открытия кредитного счёта.

        Returns:
            HTTP-ответ.
        """
        return self.post('accounts/open-credit-card-account', json=request)

    def open_credit_card_account(self, user_id: str) -> OpenCreditCardAccountResponseDict:
        request = OpenCreditCardAccountRequestDict(userId=user_id)
        response = self.open_credit_card_account_api(request)
        return response.json()


def build_accounts_gateway_http_client() -> AccountsGatewayHTTPClient:
    """Создать HTTP-клиент для Accounts Gateway API.

    Returns:
        Настроенный экземпляр AccountsGatewayHTTPClient.
    """
    return AccountsGatewayHTTPClient(client=build_gateway_http_client())