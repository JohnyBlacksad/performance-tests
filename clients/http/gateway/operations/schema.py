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
    """Базовая модель запроса на создание операции.

    Содержит общие поля для всех типов операций:
    - status: Статус операции
    - amount: Сумма операции
    - card_id: Идентификатор карты
    - account_id: Идентификатор счёта

    Attributes:
        status: Статус операции.
        amount: Сумма операции.
        card_id: Идентификатор карты.
        account_id: Идентификатор счёта.

    Пример использования:
        >>> request = MakeOperationBaseRequestSchema(
        ...     status=OperationStatus.COMPLETED,
        ...     amount=1000,
        ...     card_id='c1',
        ...     account_id='a1'
        ... )
    """
    model_config = ConfigDict(populate_by_name=True)
    status: OperationStatus
    amount: float
    card_id: str = Field(alias='cardId')
    account_id: str = Field(alias='accountId')

    @classmethod
    def get_fake_data(cls, card_id, account_id, **kwargs):
        """Сгенерировать тестовые данные для запроса.

        Создаёт экземпляр модели с фейковыми данными, используя
        переданные card_id и account_id.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.
            **kwargs: Дополнительные поля для переопределения.

        Returns:
            Экземпляр модели с тестовыми данными.

        Example:
            >>> request = MakeOperationBaseRequestSchema.get_fake_data(
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
        """
        data = {
            'status': faker_ru.enum(OperationStatus),
            'amount': faker_ru.amount(),
            'card_id': card_id,
            'account_id': account_id
        }
        data.update(kwargs)
        return cls(**data)

class MakeFeeOperationRequestSchema(MakeOperationBaseRequestSchema):
    """Модель запроса на создание операции начисления комиссии.

    Наследуется от MakeOperationBaseRequestSchema.

    Пример использования:
        >>> request = MakeFeeOperationRequestSchema(
        ...     status=OperationStatus.COMPLETED,
        ...     amount=100,
        ...     card_id='c1',
        ...     account_id='a1'
        ... )
    """
    pass

class MakeTopUpOperationRequestSchema(MakeOperationBaseRequestSchema):
    """Модель запроса на создание операции пополнения счёта.

    Наследуется от MakeOperationBaseRequestSchema.

    Пример использования:
        >>> request = MakeTopUpOperationRequestSchema(
        ...     status=OperationStatus.COMPLETED,
        ...     amount=5000,
        ...     card_id='c1',
        ...     account_id='a1'
        ... )
    """
    pass

class MakeCashbackOperationRequestSchema(MakeOperationBaseRequestSchema):
    """Модель запроса на создание операции кэшбэка.

    Наследуется от MakeOperationBaseRequestSchema.

    Пример использования:
        >>> request = MakeCashbackOperationRequestSchema(
        ...     status=OperationStatus.COMPLETED,
        ...     amount=500,
        ...     card_id='c1',
        ...     account_id='a1'
        ... )
    """
    pass

class MakeTransferOperationRequestSchema(MakeOperationBaseRequestSchema):
    """Модель запроса на создание операции перевода.

    Наследуется от MakeOperationBaseRequestSchema.

    Пример использования:
        >>> request = MakeTransferOperationRequestSchema(
        ...     status=OperationStatus.COMPLETED,
        ...     amount=10000,
        ...     card_id='c1',
        ...     account_id='a1'
        ... )
    """
    pass

class MakeBillPaymentOperationRequestSchema(MakeOperationBaseRequestSchema):
    """Модель запроса на создание операции оплаты счёта.

    Наследуется от MakeOperationBaseRequestSchema.

    Пример использования:
        >>> request = MakeBillPaymentOperationRequestSchema(
        ...     status=OperationStatus.COMPLETED,
        ...     amount=3000,
        ...     card_id='c1',
        ...     account_id='a1'
        ... )
    """
    pass

class MakeCashWithdrawalOperationRequestSchema(MakeOperationBaseRequestSchema):
    """Модель запроса на создание операции снятия наличных.

    Наследуется от MakeOperationBaseRequestSchema.

    Пример использования:
        >>> request = MakeCashWithdrawalOperationRequestSchema(
        ...     status=OperationStatus.COMPLETED,
        ...     amount=5000,
        ...     card_id='c1',
        ...     account_id='a1'
        ... )
    """
    pass

class MakePurchaseOperationRequestSchema(MakeOperationBaseRequestSchema):
    """Модель запроса на создание операции покупки.

    Наследуется от MakeOperationBaseRequestSchema и добавляет
    поле category для категории покупки.

    Attributes:
        category: Категория покупки (например, 'groceries', 'coffee').

    Пример использования:
        >>> request = MakePurchaseOperationRequestSchema(
        ...     status=OperationStatus.COMPLETED,
        ...     amount=2500,
        ...     card_id='c1',
        ...     account_id='a1',
        ...     category='groceries'
        ... )
    """
    category: str

    @classmethod
    def get_fake_data(cls, card_id, account_id, **kwargs):
        """Сгенерировать тестовые данные для запроса покупки.

        Создаёт экземпляр модели с фейковыми данными, используя
        переданные card_id и account_id. Категория генерируется
        автоматически, если не указана.

        Args:
            card_id: Идентификатор карты.
            account_id: Идентификатор счёта.
            **kwargs: Дополнительные поля для переопределения.

        Returns:
            Экземпляр модели с тестовыми данными.

        Example:
            >>> request = MakePurchaseOperationRequestSchema.get_fake_data(
            ...     card_id='c1',
            ...     account_id='a1',
            ...     category='coffee'
            ... )
        """
        if "category" not in kwargs:
            kwargs["category"] = faker_ru.category()
        return super().get_fake_data(card_id=card_id, account_id=account_id, **kwargs)