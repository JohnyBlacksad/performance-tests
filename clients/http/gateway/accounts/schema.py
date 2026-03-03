"""Pydantic-модели для валидации данных банковских счетов.

Модели описывают структуру JSON-данных для операций со счетами:
- Открытие счетов
- Получение данных счетов
"""

from pydantic import BaseModel, ConfigDict, Field
from clients.http.gateway.cards.schema import CardSchema
from enum import StrEnum


class AccountType(StrEnum):
    """Тип банковского счёта."""
    UNSPECIFIED = 'UNSPECIFIED'
    DEBIT_CARD = 'DEBIT_CARD'
    CREDIT_CARD = 'CREDIT_CARD'
    DEPOSIT = 'DEPOSIT'
    SAVINGS = 'SAVINGS'


class AccountStatus(StrEnum):
    """Статус банковского счёта."""
    UNSPECIFIED = 'UNSPECIFIED'
    ACTIVE = 'ACTIVE'
    PENDING_CLOSURE = 'PENDING_CLOSURE'
    CLOSED = 'CLOSED'


class GetAccountsQuerySchema(BaseModel):
    """Модель запроса на получение счетов пользователя.

    Attributes:
        user_id: Идентификатор пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias='userId')


class OpenDepositAccountRequestSchema(BaseModel):
    """Модель запроса на открытие депозитного счёта.

    Attributes:
        user_id: Идентификатор пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias='userId')


class OpenSavingAccountRequestSchema(BaseModel):
    """Модель запроса на открытие накопительного счёта.

    Attributes:
        user_id: Идентификатор пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias='userId')


class OpenDebitCardAccountRequestSchema(BaseModel):
    """Модель запроса на открытие счёта дебетовой карты.

    Attributes:
        user_id: Идентификатор пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias='userId')


class OpenCreditCardAccountRequestSchema(BaseModel):
    """Модель запроса на открытие счёта кредитной карты.

    Attributes:
        user_id: Идентификатор пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias='userId')


class AccountSchema(BaseModel):
    """Модель банковского счёта.

    Attributes:
        id: Уникальный идентификатор счёта.
        type: Тип счёта.
        cards: Список карт, привязанных к счёту.
        status: Статус счёта.
        balance: Баланс счёта.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    type: AccountType
    cards: list[CardSchema]
    status: AccountStatus
    balance: float


class GetAccountResponseSchema(BaseModel):
    """Модель ответа на получение счетов.

    Attributes:
        accounts: Список счетов.
    """
    accounts: list[AccountSchema]


class OpenDepositAccountResponseSchema(BaseModel):
    """Модель ответа на открытие депозитного счёта.

    Attributes:
        account: Данные открытого счёта.
    """
    account: AccountSchema


class OpenSavingAccountResponseSchema(BaseModel):
    """Модель ответа на открытие накопительного счёта.

    Attributes:
        account: Данные открытого счёта.
    """
    account: AccountSchema


class OpenDebitCardAccountResponseSchema(BaseModel):
    """Модель ответа на открытие счёта дебетовой карты.

    Attributes:
        account: Данные открытого счёта.
    """
    account: AccountSchema


class OpenCreditCardAccountResponseSchema(BaseModel):
    """Модель ответа на открытие счёта кредитной карты.

    Attributes:
        account: Данные открытого счёта.
    """
    account: AccountSchema