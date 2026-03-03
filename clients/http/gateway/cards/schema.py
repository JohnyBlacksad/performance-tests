"""Pydantic-модели для валидации данных банковских карт.

Модели описывают структуру JSON-данных для операций с картами:
- Выпуск карт
- Получение данных карт
"""

from pydantic import BaseModel, ConfigDict, Field
from enum import StrEnum


class CardType(StrEnum):
    """Тип банковской карты."""
    UNSPECIFIED = 'UNSPECIFIED'
    VIRTUAL = 'VIRTUAL'
    PHYSICAL = 'PHYSICAL'


class CardStatus(StrEnum):
    """Статус банковской карты."""
    UNSPECIFIED = 'UNSPECIFIED'
    ACTIVE = 'ACTIVE'
    FROZEN = 'FROZEN'
    CLOSED = 'CLOSED'
    BLOCKED = 'BLOCKED'


class CardPaymentSystem(StrEnum):
    """Платёжная система карты."""
    UNSPECIFIED = 'UNSPECIFIED'
    MASTERCARD = 'MASTERCARD'
    VISA = 'VISA'


class CardSchema(BaseModel):
    """Модель банковской карты.

    Attributes:
        id: Уникальный идентификатор карты.
        pin: PIN-код карты.
        cvv: CVV-код карты.
        type: Тип карты.
        status: Статус карты.
        account_id: Идентификатор счёта, к которому привязана карта.
        card_number: Номер карты.
        card_holder: Имя держателя карты.
        expiry_date: Срок действия карты.
        payment_system: Платёжная система.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    pin: str
    cvv: str
    type: CardType
    status: CardStatus
    account_id: str = Field(alias='accountId')
    card_number: str = Field(alias='cardNumber')
    card_holder: str = Field(alias='cardHolder')
    expiry_date: str = Field(alias='expiryDate')
    payment_system: str = Field(alias='paymentSystem')


class IssueVirtualCardResponseSchema(BaseModel):
    """Модель ответа на выпуск виртуальной карты.

    Attributes:
        card: Данные выпущенной карты.
    """
    card: CardSchema


class IssuePhysicalCardResponseSchema(BaseModel):
    """Модель ответа на выпуск физической карты.

    Attributes:
        card: Данные выпущенной карты.
    """
    card: CardSchema


class IssueVirtualCardRequestSchema(BaseModel):
    """Модель запроса на выпуск виртуальной карты.

    Attributes:
        user_id: Идентификатор пользователя.
        account_id: Идентификатор счёта.
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias='userId')
    account_id: str = Field(alias='accountId')


class IssuePhysicalCardRequestSchema(BaseModel):
    """Модель запроса на выпуск физической карты.

    Attributes:
        user_id: Идентификатор пользователя.
        account_id: Идентификатор счёта.
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias='userId')
    account_id: str = Field(alias='accountId')