from httpx import Response, QueryParams
from typing import TypedDict
from clients.http.base_client import BaseHTTPClient
from clients.http.gateway.gateway_client import build_gateway_http_client


class GetOperationsQueryDict(TypedDict):
    """Словарь параметров запроса для получения операций."""

    accountId: str

class GetOperationsSummaryQueryDict(TypedDict):
    """Словарь параметров запроса для получения сводки по операциям."""

    accountId: str

class MakeFeeOperationRequestDict(TypedDict):
    """Словарь запроса на операцию начисления комиссии."""

    status: str
    amount: int
    cardId: str
    accountId: str

class MakeTopUpOperationRequestDict(TypedDict):
    """Словарь запроса на операцию пополнения."""

    status: str
    amount: int
    cardId: str
    accountId: str

class MakeCashbackOperationRequestDict(TypedDict):
    """Словарь запроса на операцию начисления кэшбэка."""

    status: str
    amount: int
    cardId: str
    accountId: str

class MakeTransferOperationRequestDict(TypedDict):
    """Словарь запроса на операцию перевода."""

    status: str
    amount: int
    cardId: str
    accountId: str

class MakePurchaseOperationRequestDict(TypedDict):
    """Словарь запроса на операцию покупки."""

    status: str
    amount: int
    cardId: str
    accountId: str
    category: str

class MakeBillPaymentOperationRequestDict(TypedDict):
    """Словарь запроса на операцию оплаты счёта."""

    status: str
    amount: int
    cardId: str
    accountId: str

class MakeCashWithdrawalOperationRequestDict(TypedDict):
    """Словарь запроса на операцию снятия наличных."""

    status: str
    amount: int
    cardId: str
    accountId: str

class OperationsGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для Operations Gateway API."""

    def get_operations_api(self, params: GetOperationsQueryDict) -> Response:
        """Получить список операций по счёту.

        Args:
            params: Параметры запроса (accountId).

        Returns:
            HTTP-ответ со списком операций.
        """
        return self.get('operations', params=QueryParams(**params))

    def get_operations_summary_api(self, params: GetOperationsSummaryQueryDict) -> Response:
        """Получить сводку по операциям счёта.

        Args:
            params: Параметры запроса (accountId).

        Returns:
            HTTP-ответ со сводкой по операциям.
        """
        return self.get('operations/operations-summary', params=QueryParams(**params))

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """Получить чек по операции.

        Args:
            operation_id: Уникальный идентификатор операции.

        Returns:
            HTTP-ответ с чеком операции.
        """
        return self.get(f'operations/operation-receipt/{operation_id}')

    def get_operation_api(self, operation_id: str) -> Response:
        """Получить данные операции по ID.

        Args:
            operation_id: Уникальный идентификатор операции.

        Returns:
            HTTP-ответ с данными операции.
        """
        return self.get(f'operations/{operation_id}')

    def make_fee_operation_api(self, request: MakeFeeOperationRequestDict) -> Response:
        """Создать операцию начисления комиссии.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.
        """
        return self.post('operations/make_fee_operation', json=request)

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestDict) -> Response:
        """Создать операцию пополнения счёта.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.
        """
        return self.post('operations/make_top_up_operation', json=request)

    def make_cahsback_operation_api(self, request: MakeCashbackOperationRequestDict) -> Response:
        """Создать операцию начисления кэшбэка.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.
        """
        return self.post('operations/make_cashback_operation', json=request)

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestDict) -> Response:
        """Создать операцию перевода средств.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.
        """
        return self.post('operations/make_transfer_operation', json=request)

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestDict) -> Response:
        """Создать операцию покупки.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.
        """
        return self.post('operations/make_purchase_operation', json=request)

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestDict) -> Response:
        """Создать операцию оплаты счёта.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.
        """
        return self.post('operations/make_bill_payment_operation', json=request)

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestDict) -> Response:
        """Создать операцию снятия наличных.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.
        """
        return self.post('operations/make_cash_withdrawal_operation', json=request)

def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """Создать HTTP-клиент для Operations Gateway API.

    Returns:
        Настроенный экземпляр OperationsGatewayHTTPClient.
    """
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())