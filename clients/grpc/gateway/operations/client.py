"""gRPC клиент для Operations Gateway сервиса.

Модуль предоставляет класс OperationsGatewayGRPCClient для управления операциями:
- Получение списка операций и сводок
- Получение чеков и данных операций
- Создание различных типов операций (комиссии, пополнения, кэшбэки, переводы, покупки и т.д.)

Пример использования:
    >>> client = build_operations_gateway_grpc_client()
    >>> operations = client.get_operations(account_id='a123')
"""

from grpc import Channel
from locust.env import Environment
from tools.fakers import faker_ru
from clients.grpc.client import GRPCClient, build_gateway_grpc_client, build_gateway_locust_grpc_client
from contracts.services.gateway.operations.operations_gateway_service_pb2_grpc import OperationsGatewayServiceStub
from contracts.services.gateway.operations.rpc_get_operation_pb2 import GetOperationRequest, GetOperationResponse
from contracts.services.gateway.operations.rpc_get_operations_pb2 import GetOperationsRequest, GetOperationsResponse
from contracts.services.gateway.operations.rpc_get_operations_summary_pb2 import GetOperationsSummaryRequest, GetOperationsSummaryResponse
from contracts.services.gateway.operations.rpc_get_operation_receipt_pb2 import GetOperationReceiptRequest, GetOperationReceiptResponse
from contracts.services.gateway.operations.rpc_make_fee_operation_pb2 import MakeFeeOperationRequest, MakeFeeOperationResponse
from contracts.services.gateway.operations.rpc_make_top_up_operation_pb2 import MakeTopUpOperationRequest, MakeTopUpOperationResponse
from contracts.services.gateway.operations.rpc_make_cashback_operation_pb2 import MakeCashbackOperationRequest, MakeCashbackOperationResponse
from contracts.services.gateway.operations.rpc_make_transfer_operation_pb2 import MakeTransferOperationRequest, MakeTransferOperationResponse
from contracts.services.gateway.operations.rpc_make_purchase_operation_pb2 import MakePurchaseOperationRequest, MakePurchaseOperationResponse
from contracts.services.gateway.operations.rpc_make_bill_payment_operation_pb2 import MakeBillPaymentOperationRequest, MakeBillPaymentOperationResponse
from contracts.services.gateway.operations.rpc_make_cash_withdrawal_operation_pb2 import MakeCashWithdrawalOperationRequest, MakeCashWithdrawalOperationResponse
from contracts.services.operations.operation_pb2 import OperationStatus

class OperationsGatewayGRPCClient(GRPCClient):
    """gRPC клиент для Operations Gateway сервиса.

    Предоставляет методы для получения и создания операций по счетам.

    Example:
        >>> client = build_operations_gateway_grpc_client()
        >>> operations = client.get_operations(account_id='a123')
    """
    def __init__(self, channel: Channel) -> None:
        """Инициализировать клиент для работы с операциями.

        Args:
            channel: gRPC канал для подключения.
        """
        super().__init__(channel)
        self.stub = OperationsGatewayServiceStub(channel)

    def get_operation_api(self, request: GetOperationRequest) -> GetOperationResponse:
        """Получить операцию по ID (низкоуровневый метод).

        Args:
            request: Запрос на получение операции.

        Returns:
            Ответ с данными операции.
        """
        return self.stub.GetOperation(request)

    def get_operation(self, user_id: str) -> GetOperationResponse:
        """Получить операцию по ID.

        Args:
            user_id: Идентификатор операции.

        Returns:
            Ответ с данными операции.
        """
        request = GetOperationRequest(id=user_id)
        return self.get_operation_api(request)

    def get_operations_api(self, request: GetOperationsRequest) -> GetOperationsResponse:
        """Получить список операций (низкоуровневый метод).

        Args:
            request: Запрос на получение списка операций.

        Returns:
            Ответ со списком операций.
        """
        return self.stub.GetOperations(request)

    def get_operations(self, account_id: str) -> GetOperationsResponse:
        """Получить список операций по счёту.

        Args:
            account_id: Идентификатор счёта.

        Returns:
            Ответ со списком операций.
        """
        request = GetOperationsRequest(account_id=account_id)
        return self.get_operations_api(request)

    def get_operations_summary_api(self, request: GetOperationsSummaryRequest) -> GetOperationsSummaryResponse:
        """Получить сводку по операциям (низкоуровневый метод).

        Args:
            request: Запрос на получение сводки.

        Returns:
            Ответ со сводной статистикой.
        """
        return self.stub.GetOperationsSummary(request)

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponse:
        """Получить сводку по операциям счёта.

        Args:
            account_id: Идентификатор счёта.

        Returns:
            Ответ со сводной статистикой.
        """
        request = GetOperationsSummaryRequest(account_id=account_id)
        return self.stub.GetOperationsSummary(request)

    def get_operation_receipt_api(self, request: GetOperationReceiptRequest) -> GetOperationReceiptResponse:
        """Получить чек по операции (низкоуровневый метод).

        Args:
            request: Запрос на получение чека.

        Returns:
            Ответ с данными чека.
        """
        return self.stub.GetOperationReceipt(request)

    def get_opration_receipt(self, operation_id: str) -> GetOperationReceiptResponse:
        """Получить чек по операции.

        Args:
            operation_id: Идентификатор операции.

        Returns:
            Ответ с данными чека.
        """
        request = GetOperationReceiptRequest(operation_id=operation_id)
        return self.stub.GetOperationReceipt(request)

    def make_fee_operation_api(self, request: MakeFeeOperationRequest) -> MakeFeeOperationResponse:
        """Создать операцию комиссии (низкоуровневый метод).

        Args:
            request: Запрос на создание операции комиссии.

        Returns:
            Ответ с данными созданной операции.
        """
        return self.stub.MakeFeeOperation(request)

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponse:
        """Создать операцию начисления комиссии.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Ответ с данными созданной операции.
        """
        request = MakeFeeOperationRequest(
            status=faker_ru.proto_enum(OperationStatus), # type: ignore
            amount=faker_ru.amount(),
            card_id=card_id,
            account_id=account_id
        )
        return self.make_fee_operation_api(request)

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequest) -> MakeTopUpOperationResponse:
        """Создать операцию пополнения (низкоуровневый метод).

        Args:
            request: Запрос на создание операции пополнения.

        Returns:
            Ответ с данными созданной операции.
        """
        return self.stub.MakeTopUpOperation(request)

    def make_top_up_operation(self, card_id: str, account_id: str) -> MakeTopUpOperationResponse:
        """Создать операцию пополнения счёта.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Ответ с данными созданной операции.
        """
        request = MakeTopUpOperationRequest(
            status=faker_ru.proto_enum(OperationStatus), # type: ignore
            amount=faker_ru.amount(),
            card_id=card_id,
            account_id=account_id
        )
        return self.make_top_up_operation_api(request)

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequest) -> MakeCashbackOperationResponse:
        """Создать операцию кэшбэка (низкоуровневый метод).

        Args:
            request: Запрос на создание операции кэшбэка.

        Returns:
            Ответ с данными созданной операции.
        """
        return self.stub.MakeCashbackOperation(request)

    def make_cashback_operation(self, card_id: str, account_id: str) -> MakeCashbackOperationResponse:
        """Создать операцию начисления кэшбэка.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Ответ с данными созданной операции.
        """
        request = MakeCashbackOperationRequest(
            status=faker_ru.proto_enum(OperationStatus), # type: ignore
            amount=faker_ru.amount(),
            card_id=card_id,
            account_id=account_id
        )
        return self.make_cashback_operation_api(request)

    def make_transfer_operation_api(self, request: MakeTransferOperationRequest) -> MakeTransferOperationResponse:
        """Создать операцию перевода (низкоуровневый метод).

        Args:
            request: Запрос на создание операции перевода.

        Returns:
            Ответ с данными созданной операции.
        """
        return self.stub.MakeTransferOperation(request)

    def make_transfer_operation(self, card_id: str, account_id: str) -> MakeTransferOperationResponse:
        """Создать операцию перевода средств.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Ответ с данными созданной операции.
        """
        request = MakeTransferOperationRequest(
            status=faker_ru.proto_enum(OperationStatus), # type: ignore
            amount=faker_ru.amount(),
            card_id=card_id,
            account_id=account_id
        )
        return self.make_transfer_operation_api(request)

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequest) -> MakePurchaseOperationResponse:
        """Создать операцию покупки (низкоуровневый метод).

        Args:
            request: Запрос на создание операции покупки.

        Returns:
            Ответ с данными созданной операции.
        """
        return self.stub.MakePurchaseOperation(request)

    def make_purchase_operation(self, card_id: str, account_id: str) -> MakePurchaseOperationResponse:
        """Создать операцию покупки.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Ответ с данными созданной операции.
        """
        request = MakePurchaseOperationRequest(
            status=faker_ru.proto_enum(OperationStatus), # type: ignore
            amount=faker_ru.amount(),
            card_id=card_id,
            category=faker_ru.category(),
            account_id=account_id
        )
        return self.make_purchase_operation_api(request)

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequest) -> MakeBillPaymentOperationResponse:
        """Создать операцию оплаты счёта (низкоуровневый метод).

        Args:
            request: Запрос на создание операции оплаты счёта.

        Returns:
            Ответ с данными созданной операции.
        """
        return self.stub.MakeBillPaymentOperation(request)

    def make_bill_payment_operation(self, card_id: str, account_id: str) -> MakeBillPaymentOperationResponse:
        """Создать операцию оплаты счёта.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Ответ с данными созданной операции.
        """
        request = MakeBillPaymentOperationRequest(
            status=faker_ru.proto_enum(OperationStatus), # type: ignore
            amount=faker_ru.amount(),
            card_id=card_id,
            account_id=account_id
        )
        return self.make_bill_payment_operation_api(request)

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequest) -> MakeCashWithdrawalOperationResponse:
        """Создать операцию снятия наличных (низкоуровневый метод).

        Args:
            request: Запрос на создание операции снятия наличных.

        Returns:
            Ответ с данными созданной операции.
        """
        return self.stub.MakeCashWithdrawalOperation(request)

    def make_cash_withdrawal_operation(self, card_id: str, account_id: str) -> MakeCashWithdrawalOperationResponse:
        """Создать операцию снятия наличных.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.

        Returns:
            Ответ с данными созданной операции.
        """
        request = MakeCashWithdrawalOperationRequest(
            status=faker_ru.proto_enum(OperationStatus), # type: ignore
            amount=faker_ru.amount(),
            card_id=card_id,
            account_id=account_id
        )
        return self.make_cash_withdrawal_operation_api(request)

def build_operations_gateway_grpc_client() -> OperationsGatewayGRPCClient:
    """Создать gRPC клиент для Operations Gateway.

    Returns:
        Настроенный экземпляр OperationsGatewayGRPCClient.
    """
    return OperationsGatewayGRPCClient(channel=build_gateway_grpc_client())

def build_operations_gateway_locust_grpc_client(environment: Environment) -> OperationsGatewayGRPCClient:
    """Создать gRPC клиент с интеграцией Locust для Operations Gateway.

    Args:
        environment: Экземпляр окружения Locust.

    Returns:
        Настроенный экземпляр OperationsGatewayGRPCClient с интерцептором.
    """
    return OperationsGatewayGRPCClient(channel=build_gateway_locust_grpc_client(environment))