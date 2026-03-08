"""Клиент для работы с Operations Gateway API.

Модуль предоставляет класс OperationsGatewayHTTPClient для управления операциями:
- Получение списка операций и сводок
- Получение чеков и данных операций
- Создание различных типов операций (комиссии, пополнения, кэшбэки, переводы, покупки и т.д.)

Пример использования:
    >>> client = build_operations_gateway_http_client()
    >>> operations = client.get_operations_api({'accountId': 'a123'})
"""

from locust.env import Environment
from httpx import Response, QueryParams
from clients.http.base_client import BaseHTTPClient, HTTPClientExtensions
from clients.http.gateway.gateway_client import build_gateway_http_client, build_gateway_locust_http_client
from .schema import (
    GetOperationsQuerySchema,
    GetOperationResponseSchema,
    GetOperationsResponseSchema,
    GetOperationReceiptResponseSchema,
    GetOperationsSummaryQuerySchema,
    GetOperationsSummaryResponseSchema,
    MakeFeeOperationRequestSchema,
    MakeFeeOperationResponseSchema,
    MakeTopUpOperationRequestSchema,
    MakeTopUpOperationResponseSchema,
    MakeCashbackOperationRequestSchema,
    MakeCashbackOperationResponseSchema,
    MakePurchaseOperationRequestSchema,
    MakePurchaseOperationResponseSchema,
    MakeTransferOperationRequestSchema,
    MakeTransferOperationResponseSchema,
    MakeBillPaymentOperationRequestSchema,
    MakeBillPaymentOperationResponseSchema,
    MakeCashWithdrawalOperationRequestSchema,
    MakeCashWithdrawalOperationResponseSchema
)


class OperationsGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для Operations Gateway API.

    Предоставляет методы для получения и создания операций по счетам.

    Пример использования:
        >>> client = build_operations_gateway_http_client()
        >>> operations = client.get_operations_api({'accountId': 'a123'})
        >>> receipt = client.get_operation_receipt_api('op456')
    """

    def get_operations_api(self, params: GetOperationsQuerySchema) -> Response:
        """Получить список операций по счёту (API-метод).

        Отправляет GET-запрос для получения списка всех операций счёта.

        Args:
            params: Модель параметров запроса (GetOperationsQuerySchema).

        Returns:
            HTTP-ответ со списком операций.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> params = GetOperationsQuerySchema(account_id='a123')
            >>> response = client.get_operations_api(params)
        """
        return self.get('operations', params=QueryParams(**params.model_dump(by_alias=True)),
                        extensions=HTTPClientExtensions(route='operations'))

    def get_operations(self, account_id: str) -> GetOperationsResponseSchema:
        """Получить список операций по счёту (высокоуровневый метод).

        Создаёт и отправляет запрос на получение списка операций,
        возвращая их в виде модели GetOperationsResponseSchema.

        Args:
            account_id: Уникальный идентификатор счёта.

        Returns:
            Модель GetOperationsResponseSchema со списком операций.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operations = client.get_operations(account_id='a123')
            >>> print(operations.operations[0].amount)
        """
        params = GetOperationsQuerySchema(account_id=account_id) # type: ignore
        response = self.get_operations_api(params)
        return GetOperationsResponseSchema.model_validate_json(response.text)

    def get_operations_summary_api(self, params: GetOperationsSummaryQuerySchema) -> Response:
        """Получить сводку по операциям счёта (API-метод).

        Отправляет GET-запрос для получения агрегированной информации
        по операциям счёта.

        Args:
            params: Модель параметров запроса (GetOperationsSummaryQuerySchema).

        Returns:
            HTTP-ответ со сводкой по операциям.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> params = GetOperationsSummaryQuerySchema(account_id='a123')
            >>> response = client.get_operations_summary_api(params)
        """
        return self.get('operations/operations-summary',
                        params=QueryParams(**params.model_dump(by_alias=True)),
                        extensions=HTTPClientExtensions(route='operations/operations-summary'))

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseSchema:
        """Получить сводку по операциям счёта (высокоуровневый метод).

        Создаёт и отправляет запрос на получение сводной статистики,
        возвращая её в виде модели GetOperationsSummaryResponseSchema.

        Args:
            account_id: Уникальный идентификатор счёта.

        Returns:
            Модель GetOperationsSummaryResponseSchema со сводной статистикой.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> summary = client.get_operations_summary(account_id='a123')
            >>> print(summary.summary.spent_amount)
        """
        request = GetOperationsSummaryQuerySchema(account_id=account_id) # type: ignore
        response = self.get_operations_summary_api(request)
        return GetOperationsSummaryResponseSchema.model_validate_json(response.text)

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
        return self.get(f'operations/operation-receipt/{operation_id}',
                        extensions=HTTPClientExtensions(route='operations/operation-receipt/{operation_id}'))

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseSchema:
        """Получить чек по операции (высокоуровневый метод).

        Создаёт и отправляет запрос на получение чека,
        возвращая его в виде модели GetOperationReceiptResponseSchema.

        Args:
            operation_id: Уникальный идентификатор операции.

        Returns:
            Модель GetOperationReceiptResponseSchema с данными чека.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> receipt = client.get_operation_receipt(operation_id='op456')
            >>> print(receipt.receipt.url)
        """
        response = self.get_operation_receipt_api(operation_id)
        return GetOperationReceiptResponseSchema.model_validate_json(response.text)

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
        return self.get(f'operations/{operation_id}',
                        extensions=HTTPClientExtensions(route='operations/{operation_id}'))

    def get_operation(self, operation_id: str) -> GetOperationResponseSchema:
        """Получить данные операции по ID (высокоуровневый метод).

        Создаёт и отправляет запрос на получение данных операции,
        возвращая их в виде модели GetOperationResponseSchema.

        Args:
            operation_id: Уникальный идентификатор операции.

        Returns:
            Модель GetOperationResponseSchema с данными операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.get_operation(operation_id='op456')
            >>> print(operation.operation.amount)
        """
        response = self.get_operation_api(operation_id)
        return GetOperationResponseSchema.model_validate_json(response.text)

    def make_fee_operation_api(self, request: MakeFeeOperationRequestSchema) -> Response:
        """Создать операцию начисления комиссии (API-метод).

        Отправляет POST-запрос на создание операции комиссии.

        Args:
            request: Модель запроса на создание операции комиссии
                     (MakeFeeOperationRequestSchema).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = MakeFeeOperationRequestSchema(
            ...     status='COMPLETED',
            ...     amount=100,
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
            >>> response = client.make_fee_operation_api(request)
        """
        return self.post('operations/make-fee-operation', json=request.model_dump(by_alias=True))

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponseSchema:
        """Создать операцию начисления комиссии (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию комиссии с предзаданными параметрами.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Модель MakeFeeOperationResponseSchema с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_fee_operation(card_id='c1', account_id='a1')
            >>> print(operation.operation.id)
        """
        request = MakeFeeOperationRequestSchema.get_fake_data(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_fee_operation_api(request)
        return MakeFeeOperationResponseSchema.model_validate_json(response.text)

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestSchema) -> Response:
        """Создать операцию пополнения счёта (API-метод).

        Отправляет POST-запрос на создание операции пополнения.

        Args:
            request: Модель запроса на создание операции пополнения
                     (MakeTopUpOperationRequestSchema).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = MakeTopUpOperationRequestSchema(
            ...     status='COMPLETED',
            ...     amount=5000,
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
            >>> response = client.make_top_up_operation_api(request)
        """
        return self.post('operations/make-top-up-operation', json=request.model_dump(by_alias=True))

    def make_top_up_operation(self, card_id: str, account_id: str) -> MakeTopUpOperationResponseSchema:
        """Создать операцию пополнения счёта (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию пополнения с предзаданными параметрами.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Модель MakeTopUpOperationResponseSchema с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_top_up_operation(card_id='c1', account_id='a1')
            >>> print(operation.operation.amount)
        """
        request = MakeTopUpOperationRequestSchema.get_fake_data(card_id=card_id, account_id=account_id)
        response = self.make_top_up_operation_api(request)
        return MakeTopUpOperationResponseSchema.model_validate_json(response.text)

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestSchema) -> Response:
        """Создать операцию начисления кэшбэка (API-метод).

        Отправляет POST-запрос на создание операции кэшбэка.

        Args:
            request: Модель запроса на создание операции кэшбэка
                     (MakeCashbackOperationRequestSchema).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = MakeCashbackOperationRequestSchema(
            ...     status='COMPLETED',
            ...     amount=500,
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
            >>> response = client.make_cashback_operation_api(request)
        """
        return self.post('operations/make-cashback-operation', json=request.model_dump(by_alias=True))

    def make_cashback_operation(self, card_id: str, account_id: str) -> MakeCashbackOperationResponseSchema:
        """Создать операцию начисления кэшбэка (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию кэшбэка с предзаданными параметрами.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Модель MakeCashbackOperationResponseSchema с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_cashback_operation(card_id='c1', account_id='a1')
            >>> print(operation.operation.amount)
        """
        request = MakeCashbackOperationRequestSchema.get_fake_data(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_cashback_operation_api(request)
        return MakeCashbackOperationResponseSchema.model_validate_json(response.text)

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestSchema) -> Response:
        """Создать операцию перевода средств (API-метод).

        Отправляет POST-запрос на создание операции перевода.

        Args:
            request: Модель запроса на создание операции перевода
                     (MakeTransferOperationRequestSchema).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = MakeTransferOperationRequestSchema(
            ...     status='COMPLETED',
            ...     amount=10000,
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
            >>> response = client.make_transfer_operation_api(request)
        """
        return self.post('operations/make-transfer-operation', json=request.model_dump(by_alias=True))

    def make_transfer_operation(self, card_id: str, account_id: str) -> MakeTransferOperationResponseSchema:
        """Создать операцию перевода средств (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию перевода с предзаданными параметрами.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Модель MakeTransferOperationResponseSchema с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_transfer_operation(card_id='c1', account_id='a1')
            >>> print(operation.operation.amount)
        """
        request = MakeTransferOperationRequestSchema.get_fake_data(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_transfer_operation_api(request)
        return MakeTransferOperationResponseSchema.model_validate_json(response.text)

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestSchema) -> Response:
        """Создать операцию покупки (API-метод).

        Отправляет POST-запрос на создание операции покупки.

        Args:
            request: Модель запроса на создание операции покупки
                     (MakePurchaseOperationRequestSchema).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = MakePurchaseOperationRequestSchema(
            ...     status='COMPLETED',
            ...     amount=2500,
            ...     card_id='c1',
            ...     account_id='a1',
            ...     category='groceries'
            ... )
            >>> response = client.make_purchase_operation_api(request)
        """
        return self.post('operations/make-purchase-operation', json=request.model_dump(by_alias=True))

    def make_purchase_operation(self, card_id: str, account_id: str) -> MakePurchaseOperationResponseSchema:
        """Создать операцию покупки (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию покупки с предзаданными параметрами
        (категория: coffee).

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Модель MakePurchaseOperationResponseSchema с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_purchase_operation(card_id='c1', account_id='a1')
            >>> print(operation.operation.category)
        """
        request = MakePurchaseOperationRequestSchema.get_fake_data(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_purchase_operation_api(request)
        return MakePurchaseOperationResponseSchema.model_validate_json(response.text)

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestSchema) -> Response:
        """Создать операцию оплаты счёта (API-метод).

        Отправляет POST-запрос на создание операции оплаты счёта.

        Args:
            request: Модель запроса на создание операции оплаты счёта
                     (MakeBillPaymentOperationRequestSchema).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = MakeBillPaymentOperationRequestSchema(
            ...     status='COMPLETED',
            ...     amount=3000,
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
            >>> response = client.make_bill_payment_operation_api(request)
        """
        return self.post('operations/make-bill-payment-operation', json=request.model_dump(by_alias=True))

    def make_bill_payment_operation(self, card_id: str, account_id: str) -> MakeBillPaymentOperationResponseSchema:
        """Создать операцию оплаты счёта (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию оплаты счёта с предзаданными параметрами.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Модель MakeBillPaymentOperationResponseSchema с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_bill_payment_operation(card_id='c1', account_id='a1')
            >>> print(operation.operation.amount)
        """
        request = MakeBillPaymentOperationRequestSchema.get_fake_data(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_bill_payment_operation_api(request)
        return MakeBillPaymentOperationResponseSchema.model_validate_json(response.text)

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestSchema) -> Response:
        """Создать операцию снятия наличных (API-метод).

        Отправляет POST-запрос на создание операции снятия наличных.

        Args:
            request: Модель запроса на создание операции снятия наличных
                     (MakeCashWithdrawalOperationRequestSchema).

        Returns:
            HTTP-ответ с результатом операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> request = MakeCashWithdrawalOperationRequestSchema(
            ...     status='COMPLETED',
            ...     amount=5000,
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
            >>> response = client.make_cash_withdrawal_operation_api(request)
        """
        return self.post('operations/make-cash-withdrawal-operation', json=request.model_dump(by_alias=True))

    def make_cash_withdrawal_operation(self, card_id: str, account_id: str) -> MakeCashWithdrawalOperationResponseSchema:
        """Создать операцию снятия наличных (высокоуровневый метод).

        Создаёт и отправляет запрос на операцию снятия наличных с предзаданными параметрами.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Модель MakeCashWithdrawalOperationResponseSchema с данными созданной операции.

        Example:
            >>> client = build_operations_gateway_http_client()
            >>> operation = client.make_cash_withdrawal_operation(card_id='c1', account_id='a1')
            >>> print(operation.operation.amount)
        """
        request = MakeCashWithdrawalOperationRequestSchema.get_fake_data(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_cash_withdrawal_operation_api(request)
        return MakeCashWithdrawalOperationResponseSchema.model_validate_json(response.text)

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

def build_operations_locust_gateway_http_client(environment: Environment) -> OperationsGatewayHTTPClient:
    """Создать HTTP-клиент для Operations Gateway API с интеграцией Locust.

    Возвращает настроенный экземпляр OperationsGatewayHTTPClient для работы
    с API управления операциями через Locust (сбор метрик).

    Args:
        environment: Окружение Locust для настройки клиента.

    Returns:
        Настроенный экземпляр OperationsGatewayHTTPClient с Locust-интерцептором.

    Example:
        >>> client = build_operations_locust_gateway_http_client(environment)
        >>> response = client.get_operations_api({'accountId': 'a123'})
    """
    return OperationsGatewayHTTPClient(client=build_gateway_locust_http_client(environment))


