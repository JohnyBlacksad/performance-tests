"""Pydantic-модели для валидации данных операций.

Модели описывают структуру JSON-данных для операций:
- Получение операций
- Создание операций
- Получение сводки по операциям
"""

from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from datetime import date
from enum import StrEnum
from tools.fakers import faker_en, faker_ru

class OperationType(StrEnum):
    """Тип банковской операции."""
    FEE = 'FEE'
    TOP_UP = 'TOP_UP'
    PURCHASE = 'PURCHASE'
    CASHBACK = 'CASHBACK'
    TRANSFER = 'TRANSFER'
    BILL_PAYMENT = 'BILL_PAYMENT'
    CASH_WITHDRAWAL = 'CASH_WITHDRAWAL'


class OperationStatus(StrEnum):
    """Статус банковской операции."""
    FAILED = 'FAILED'
    COMPLETED = 'COMPLETED'
    IN_PROGRESS = 'IN_PROGRESS'
    UNSPECIFIED = 'UNSPECIFIED'


class OperationSchema(BaseModel):
    """Модель банковской операции.

    Attributes:
        id: Уникальный идентификатор операции.
        type: Тип операции.
        status: Статус операции.
        amount: Сумма операции.
        card_id: Идентификатор карты.
        category: Категория операции.
        created_at: Дата создания операции.
        account_id: Идентификатор счёта.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    type: OperationType
    status: OperationStatus
    amount: float
    card_id: str = Field(alias='cardId')
    category: str
    created_at: date = Field(alias='createdAt')
    account_id: str = Field(alias='accountId')


class GetOperationsResponseSchema(BaseModel):
    """Модель ответа на получение списка операций.

    Attributes:
        operations: Список операций.
    """
    operations: list[OperationSchema]


class GetOperationResponseSchema(BaseModel):
    """Модель ответа на получение операции.

    Attributes:
        operation: Данные операции.
    """
    operation: OperationSchema


class SummarySchema(BaseModel):
    """Модель сводки по операциям.

    Attributes:
        spent_amount: Общая сумма расходов.
        received_amount: Общая сумма поступлений.
        cashback_amount: Общая сумма кэшбэка.
    """
    model_config = ConfigDict(populate_by_name=True)
    spent_amount: float = Field(alias='spentAmount')
    received_amount: float = Field(alias='receivedAmount')
    cashback_amount: float = Field(alias='cashbackAmount')


class GetOperationsSummaryResponseSchema(BaseModel):
    """Модель ответа на получение сводки по операциям.

    Attributes:
        summary: Данные сводки.
    """
    summary: SummarySchema


class ReceiptSchema(BaseModel):
    """Модель чека операции.

    Attributes:
        url: URL документа чека.
        document: Содержимое документа.
    """
    url: HttpUrl
    document: str


class GetOperationReceiptResponseSchema(BaseModel):
    """Модель ответа на получение чека операции.

    Attributes:
        receipt: Данные чека.
    """
    receipt: ReceiptSchema


class MakeFeeOperationResponseSchema(BaseModel):
    """Модель ответа на создание операции начисления комиссии.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationSchema


class MakeTopUpOperationResponseSchema(BaseModel):
    """Модель ответа на создание операции пополнения.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationSchema


class MakeCashbackOperationResponseSchema(BaseModel):
    """Модель ответа на создание операции кэшбэка.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationSchema


class MakeTransferOperationResponseSchema(BaseModel):
    """Модель ответа на создание операции перевода.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationSchema


class MakePurchaseOperationResponseSchema(BaseModel):
    """Модель ответа на создание операции покупки.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationSchema


class MakeBillPaymentOperationResponseSchema(BaseModel):
    """Модель ответа на создание операции оплаты счёта.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationSchema


class MakeCashWithdrawalOperationResponseSchema(BaseModel):
    """Модель ответа на создание операции снятия наличных.

    Attributes:
        operation: Данные созданной операции.
    """
    operation: OperationSchema


class GetOperationsQuerySchema(BaseModel):
    """Модель query-параметров для получения списка операций.

    Attributes:
        account_id: Идентификатор счёта.
    """
    model_config = ConfigDict(populate_by_name=True)
    account_id: str = Field(alias='accountId')


class GetOperationsSummaryQuerySchema(BaseModel):
    """Модель query-параметров для получения сводки по операциям.

    Attributes:
        account_id: Идентификатор счёта.
    """
    model_config = ConfigDict(populate_by_name=True)
    account_id: str = Field(alias='accountId')


class MakeOperationBaseRequestSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    status: OperationStatus
    amount: float
    card_id: str = Field(alias='cardId')
    account_id: str = Field(alias='accountId')

    @classmethod
    def get_fake_data(cls, card_id, account_id, **kwargs):
        data = {
            'status': faker_ru.enum(OperationStatus),
            'amount': faker_ru.amount(),
            'card_id': card_id,
            'account_id': account_id
        }
        data.update(kwargs)
        return cls(**data)

class MakeFeeOperationRequestSchema(MakeOperationBaseRequestSchema):pass
class MakeTopUpOperationRequestSchema(MakeOperationBaseRequestSchema):pass
class MakeCashbackOperationRequestSchema(MakeOperationBaseRequestSchema):pass
class MakeTransferOperationRequestSchema(MakeOperationBaseRequestSchema):pass
class MakeBillPaymentOperationRequestSchema(MakeOperationBaseRequestSchema):pass
class MakeCashWithdrawalOperationRequestSchema(MakeOperationBaseRequestSchema):pass

class MakePurchaseOperationRequestSchema(MakeOperationBaseRequestSchema):
    category: str

    @classmethod
    def get_fake_data(cls, card_id, account_id, **kwargs):
        if "category" not in kwargs:
            kwargs["category"] = faker_ru.category()
        return super().get_fake_data(card_id=card_id, account_id=account_id, **kwargs)