from httpx import Response
from base_client import BaseHTTPClient, QueryParams
from typing import TypedDict

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

    def open_deposit_account_api(self, request: OpenDepositAccountRequestDict) -> Response:
        """Открыть депозитный счёт.

        Args:
            request: Словарь с данными для открытия депозитного счёта.

        Returns:
            HTTP-ответ.
        """
        return self.post('accounts/open_deposit_account', json=request)

    def open_saveng_account_api(self, request: OpenSavingAccountRequestDict) -> Response:
        """Открыть накопительный счёт.

        Args:
            request: Словарь с данными для открытия накопительного счёта.

        Returns:
            HTTP-ответ.
        """
        return self.post('accounts/open-savings-account', json=request)

    def open_debit_card_account_api(self, request: OpenDebitCardAccountRequestDict) -> Response:
        """Открыть дебетовый счёт.

        Args:
            request: Словарь с данными для открытия дебетового счёта.

        Returns:
            HTTP-ответ.
        """
        return self.post('accounts/open-debit-card-account', json=request)

    def open_credit_card_account_api(self, request: OpenCreditCardAccountRequestDict) -> Response:
        """Открыть кредитный счёт.

        Args:
            request: Словарь с данными для открытия кредитного счёта.

        Returns:
            HTTP-ответ.
        """
        return self.post('accounts/open-credit-card-account', json=request)

