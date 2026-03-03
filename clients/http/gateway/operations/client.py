"""Клиент для работы с Operations Gateway API.

Модуль предоставляет класс OperationsGatewayHTTPClient для управления операциями:
- Получение списка операций и сводок
- Получение чеков и данных операций
- Создание различных типов операций (комиссии, пополнения, кэшбэки, переводы, покупки и т.д.)

Пример использования:
    >>> client = build_operations_gateway_http_client()
    >>> operations = client.get_operations_api({'accountId': 'a123'})
"""

from httpx import Response, QueryParams
from typing import TypedDict
from clients.http.base_client import BaseHTTPClient
from clients.http.gateway.gateway_client import build_gateway_http_client

class OperationDict(TypedDict):
    """Словарь, представляющий данные операции.

    Attributes:
        id: Уникальный идентификатор операции.
        type: Тип операции (fee, top_up, cashback, transfer, purchase и т.д.).
        status: Статус операции (completed, pending, failed и т.д.).
        amount: Сумма операции в копейках/центах.
        cardId: Идентификатор карты, связанной с операцией.
        category: Категория операции (для покупок).
        createdAt: Дата и время создания операции в формате ISO 8601.
        accountId: Идентификатор счёта, связанного с операцией.
    """
    id: str
    type: str
    status: str
    amount: float
    cardId: str
    category: str
    createdAt: str
    accountId: str


class GetOperationsResponseDict(TypedDict):
    """Словарь ответа на получение списка операций.

    Attributes:
        operations: Список операций.
    """
    operations: list[OperationDict]


class GetOperationResponseDict(TypedDict):
    """Словарь ответа на получение данных операции.

    Attributes:
        operation: Данные операции.
    """
    operation: OperationDict


class SummaryDict(TypedDict):
    """Словарь, представляющий сводную статистику по операциям.

    Attributes:
        spentAmount: Общая сумма потраченных средств.
        receivedAmount: Общая сумма полученных средств.
        cashbackAmount: Общая сумма начисленного кэшбэка.
    """
    spentAmount: float
    receivedAmount: float
    cashbackAmount: float


class GetOperationsSummaryResponseDict(TypedDict):
    """Словарь ответа на получение сводки по операциям.

    Attributes:
        summary: Сводная статистика по операциям.
    """
    summary: SummaryDict


class ReceiptDict(TypedDict):
    """Словарь, представляющий данные чека операции.

    Attributes:
        url: URL для доступа к чеку.
        document: Содержимое чека в формате base64 или текст.
    """
    url: str
    document: str


class GetOperationReceiptResponseDict(TypedDict):
    """Словарь ответа на получение чека операции.

    Attributes:
        receipt: Данные чека.
    """
    receipt: ReceiptDict


class MakeFeeOperationResponseDict(TypedDict):
    """Словарь ответа на создание операции начисления комиссии.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationDict


class MakeTopUpOperationResponseDict(TypedDict):
    """Словарь ответа на создание операции пополнения.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationDict


class MakeCashbackOperationResponseDict(TypedDict):
    """Словарь ответа на создание операции начисления кэшбэка.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationDict


class MakeTransferOperationResponseDict(TypedDict):
    """Словарь ответа на создание операции перевода.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationDict


class MakePurchaseOperationResponseDict(TypedDict):
    """Словарь ответа на создание операции покупки.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationDict


class MakeBillPaymentOperationResponseDict(TypedDict):
    """Словарь ответа на создание операции оплаты счёта.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationDict


class MakeCashWithdrawalOperationResponseDict(TypedDict):
    """Словарь ответа на создание операции снятия наличных.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationDict

class GetOperationsQueryDict(TypedDict):
    """Словарь параметров запроса для получения операций.

    Attributes:
        accountId: Уникальный идентификатор счёта.
    """
    accountId: str


class GetOperationsSummaryQueryDict(TypedDict):
    """Словарь параметров запроса для получения сводки по операциям.

    Attributes:
        accountId: Уникальный идентификатор счёта.
    """
    accountId: str


class MakeFeeOperationRequestDict(TypedDict):
    """Словарь запроса на операцию начисления комиссии.

    Attributes:
        status: Статус операции.
        amount: Сумма комиссии в копейках/центах.
        cardId: Идентификатор карты.
        accountId: Идентификатор счёта.
    """
    status: str
    amount: int
    cardId: str
    accountId: str


class MakeTopUpOperationRequestDict(TypedDict):
    """Словарь запроса на операцию пополнения.

    Attributes:
        status: Статус операции.
        amount: Сумма пополнения в копейках/центах.
        cardId: Идентификатор карты.
        accountId: Идентификатор счёта.
    """
    status: str
    amount: int
    cardId: str
    accountId: str


class MakeCashbackOperationRequestDict(TypedDict):
    """Словарь запроса на операцию начисления кэшбэка.

    Attributes:
        status: Статус операции.
        amount: Сумма кэшбэка в копейках/центах.
        cardId: Идентификатор карты.
        accountId: Идентификатор счёта.
    """
    status: str
    amount: int
    cardId: str
    accountId: str


class MakeTransferOperationRequestDict(TypedDict):
    """Словарь запроса на операцию перевода.

    Attributes:
        status: Статус операции.
        amount: Сумма перевода в копейках/центах.
        cardId: Идентификатор карты.
        accountId: Идентификатор счёта.
    """
    status: str
    amount: int
    cardId: str
    accountId: str


class MakePurchaseOperationRequestDict(TypedDict):
    """Словарь запроса на операцию покупки.

    Attributes:
        status: Статус операции.
        amount: Сумма покупки в копейках/центах.
        cardId: Идентификатор карты.
        accountId: Идентификатор счёта.
        category: Категория покупки.
    """
    status: str
    amount: int
    cardId: str
    accountId: str
    category: str


class MakeBillPaymentOperationRequestDict(TypedDict):
    """Словарь запроса на операцию оплаты счёта.

    Attributes:
        status: Статус операции.
        amount: Сумма оплаты в копейках/центах.
        cardId: Идентификатор карты.
        accountId: Идентификатор счёта.
    """
    status: str
    amount: int
    cardId: str
    accountId: str


class MakeCashWithdrawalOperationRequestDict(TypedDict):
    """Словарь запроса на операцию снятия наличных.

    Attributes:
        status: Статус операции.
        amount: Сумма снятия в копейках/центах.
        cardId: Идентификатор карты.
        accountId: Идентификатор счёта.
    """
    status: str
    amount: int
    cardId: str
    accountId: str


class OperationsGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для Operations Gateway API.

    Предоставляет методы для получения и создания операций по счетам.

    Пример использования:
        >>> client = build_operations_gateway_http_client()
        >>> operations = client.get_operations_api({'accountId': 'a123'})
        >>> receipt = client.get_operation_receipt_api('op456')
    """

    def get_operations_api(self, params: GetOperationsQueryDict) -> Response:
        """Получить список операций по счёту (API-метод).

        Отправляет GET-запрос для получения списка всех операций счёта.

        Args:
            params: Параметры запроса (accountId).

        Returns:
            HTTP-ответ со списком операций.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> response = client.get_operations_api({'accountId': 'a123'})
        """
        return self.get('operations', params=QueryParams(**params))

    def get_operations(self, account_id: str) -> GetOperationsResponseDict:
        """Получить список операций по счёту (высокоуровневый метод).

        Создаёт и отправляет запрос на получение списка операций,
        возвращая их в виде словаря.

        Args:
            account_id: Уникальный идентификатор счёта.

        Returns:
            Словарь со списком операций.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operations = client.get_operations(account_id='a123')
            >>> print(operations['operations'][0]['amount'])
        """
        params = GetOperationsQueryDict(accountId=account_id)
        response = self.get_operations_api(params)
        return response.json()

    def get_operations_summary_api(self, params: GetOperationsSummaryQueryDict) -> Response:
        """Получить сводку по операциям счёта (API-метод).

        Отправляет GET-запрос для получения агрегированной информации
        по операциям счёта.

        Args:
            params: Параметры запроса (accountId).

        Returns:
            HTTP-ответ со сводкой по операциям.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> response = client.get_operations_summary_api({'accountId': 'a123'})
        """
        return self.get('operations/operations-summary', params=QueryParams(**params))

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseDict:
        """Получить сводку по операциям счёта (высокоуровневый метод).

        Создаёт и отправляет запрос на получение сводной статистики,
        возвращая её в виде словаря.

        Args:
            account_id: Уникальный идентификатор счёта.

        Returns:
            Словарь со сводной статистикой по операциям.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> summary = client.get_operations_summary(account_id='a123')
            >>> print(summary['summary']['spentAmount'])
        """
        request = GetOperationsSummaryQueryDict(accountId=account_id)
        response = self.get_operations_summary_api(request)
        return response.json()

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """Получить чек по операции (API-метод).

        Отправляет GET-запрос для получения чека конкретной операции.

        Args:
            operation_id: Уникальный идентификатор операции.

        Returns:
            HTTP-ответ с чеком операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> response = client.get_operation_receipt_api('op456')
        """
        return self.get(f'operations/operation-receipt/{operation_id}')

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseDict:
        """Получить чек по операции (высокоуровневый метод).

        Создаёт и отправляет запрос на получение чека,
        возвращая его в виде словаря.

        Args:
            operation_id: Уникальный идентификатор операции.

        Returns:
            Словарь с данными чека.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> receipt = client.get_operation_receipt(operation_id='op456')
            >>> print(receipt['receipt']['url'])
        """
        response = self.get_operation_receipt_api(operation_id)
        return response.json()

    def get_operation_api(self, operation_id: str) -> Response:
        """Получить данные операции по ID (API-метод).

        Отправляет GET-запрос для получения детальной информации об операции.

        Args:
            operation_id: Уникальный идентификатор операции.

        Returns:
            HTTP-ответ с данными операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> response = client.get_operation_api('op456')
        """
        return self.get(f'operations/{operation_id}')

    def get_operation(self, operation_id: str) -> GetOperationResponseDict:
        """Получить данные операции по ID (высокоуровневый метод).

        Создаёт и отправляет запрос на получение данных операции,
        возвращая их в виде словаря.

        Args:
            operation_id: Уникальный идентификатор операции.

        Returns:
            Словарь с данными операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.get_operation(operation_id='op456')
            >>> print(operation['operation']['amount'])
        """
        response = self.get_operation_api(operation_id)
        return response.json()

    def make_fee_operation_api(self, request: MakeFeeOperationRequestDict) -> Response:
        """Создать операцию начисления комиссии (API-метод).

        Отправляет POST-запрос на создание операции комиссии.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = {'status': 'completed', 'amount': 100, 'cardId': 'c1', 'accountId': 'a1'}
            >>> response = client.make_fee_operation_api(request)
        """
        return self.post('operations/make-fee-operation', json=request)

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponseDict:
        """Создать операцию начисления комиссии (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию комиссии с предзаданными параметрами.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Словарь с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_fee_operation(card_id='c1', account_id='a1')
            >>> print(operation['operation']['id'])
        """
        request = MakeFeeOperationRequestDict(
            status='COMPLETED',
            amount=550,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_fee_operation_api(request)
        return response.json()

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestDict) -> Response:
        """Создать операцию пополнения счёта (API-метод).

        Отправляет POST-запрос на создание операции пополнения.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = {'status': 'completed', 'amount': 5000, 'cardId': 'c1', 'accountId': 'a1'}
            >>> response = client.make_top_up_operation_api(request)
        """
        return self.post('operations/make-top-up-operation', json=request)

    def make_top_up_operation(self, card_id: str, account_id: str) -> MakeTopUpOperationResponseDict:
        """Создать операцию пополнения счёта (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию пополнения с предзаданными параметрами.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Словарь с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_top_up_operation(card_id='c1', account_id='a1')
            >>> print(operation['operation']['amount'])
        """
        request = MakeTopUpOperationRequestDict(
            status='COMPLETED',
            amount=50,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_top_up_operation_api(request)
        return response.json()

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestDict) -> Response:
        """Создать операцию начисления кэшбэка (API-метод).

        Отправляет POST-запрос на создание операции кэшбэка.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = {'status': 'completed', 'amount': 500, 'cardId': 'c1', 'accountId': 'a1'}
            >>> response = client.make_cashback_operation_api(request)
        """
        return self.post('operations/make-cashback-operation', json=request)

    def make_cashback_operation(self, card_id: str, account_id: str) -> MakeCashbackOperationResponseDict:
        """Создать операцию начисления кэшбэка (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию кэшбэка с предзаданными параметрами.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Словарь с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_cashback_operation(card_id='c1', account_id='a1')
            >>> print(operation['operation']['amount'])
        """
        request = MakeCashbackOperationRequestDict(
            status='COMPLETED',
            amount=50,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_cashback_operation_api(request)
        return response.json()

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestDict) -> Response:
        """Создать операцию перевода средств (API-метод).

        Отправляет POST-запрос на создание операции перевода.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = {'status': 'completed', 'amount': 10000, 'cardId': 'c1', 'accountId': 'a1'}
            >>> response = client.make_transfer_operation_api(request)
        """
        return self.post('operations/make-transfer-operation', json=request)

    def make_transfer_operation(self, card_id: str, account_id: str) -> MakeTransferOperationResponseDict:
        """Создать операцию перевода средств (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию перевода с предзаданными параметрами.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Словарь с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_transfer_operation(card_id='c1', account_id='a1')
            >>> print(operation['operation']['amount'])
        """
        request = MakeTransferOperationRequestDict(
            status='COMPLETED',
            amount=50,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_transfer_operation_api(request)
        return response.json()

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestDict) -> Response:
        """Создать операцию покупки (API-метод).

        Отправляет POST-запрос на создание операции покупки.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId, category).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = {'status': 'completed', 'amount': 2500, 'cardId': 'c1', 'accountId': 'a1', 'category': 'groceries'}
            >>> response = client.make_purchase_operation_api(request)
        """
        return self.post('operations/make-purchase-operation', json=request)

    def make_purchase_operation(self, card_id: str, account_id: str) -> MakePurchaseOperationResponseDict:
        """Создать операцию покупки (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию покупки с предзаданными параметрами
        (категория: coffee).

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Словарь с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_purchase_operation(card_id='c1', account_id='a1')
            >>> print(operation['operation']['category'])
        """
        request = MakePurchaseOperationRequestDict(
            status='COMPLETED',
            amount=50,
            cardId=card_id,
            accountId=account_id,
            category='coffee'
        )
        response = self.make_purchase_operation_api(request)
        return response.json()

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestDict) -> Response:
        """Создать операцию оплаты счёта (API-метод).

        Отправляет POST-запрос на создание операции оплаты счёта.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = {'status': 'completed', 'amount': 3000, 'cardId': 'c1', 'accountId': 'a1'}
            >>> response = client.make_bill_payment_operation_api(request)
        """
        return self.post('operations/make-bill-payment-operation', json=request)

    def make_bill_payment_operation(self, card_id: str, account_id: str) -> MakeBillPaymentOperationResponseDict:
        """Создать операцию оплаты счёта (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию оплаты счёта с предзаданными параметрами.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Словарь с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_bill_payment_operation(card_id='c1', account_id='a1')
            >>> print(operation['operation']['amount'])
        """
        request = MakeBillPaymentOperationRequestDict(
            status='COMPLETED',
            amount=50,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_bill_payment_operation_api(request)
        return response.json()

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestDict) -> Response:
        """Создать операцию снятия наличных (API-метод).

        Отправляет POST-запрос на создание операции снятия наличных.

        Args:
            request: Словарь с данными операции (status, amount, cardId, accountId).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = {'status': 'completed', 'amount': 5000, 'cardId': 'c1', 'accountId': 'a1'}
            >>> response = client.make_cash_withdrawal_operation_api(request)
        """
        return self.post('operations/make-cash-withdrawal-operation', json=request)

    def make_cash_withdrawal_operation(self, card_id: str, account_id: str) -> MakeCashWithdrawalOperationResponseDict:
        """Создать операцию снятия наличных (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию снятия наличных с предзаданными параметрами.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Словарь с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_cash_withdrawal_operation(card_id='c1', account_id='a1')
            >>> print(operation['operation']['amount'])
        """
        request = MakeCashWithdrawalOperationRequestDict(
            status='COMPLETED',
            amount=50,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_cash_withdrawal_operation_api(request)
        return response.json()

def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """Создать HTTP-клиент для Operations Gateway API.

    Возвращает настроенный экземпляр OperationsGatewayHTTPClient для работы
    с API управления операциями.

    Returns:
        Настроенный экземпляр OperationsGatewayHTTPClient.

    Example:
        >>> client = build_operations_gateway_http_client()
        >>> response = client.get_operations_api({'accountId': 'a123'})
    """
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())
