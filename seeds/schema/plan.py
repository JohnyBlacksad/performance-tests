"""Pydantic-модели для планирования генерации тестовых данных.

Модели описывают структуру плана для генерации:
- Пользователей
- Счетов (депозитные, накопительные, кредитные, дебетовые)
- Карт (физические, виртуальные)
- Операций (пополнения, покупки, кэшбэки, переводы и т.д.)

Пример использования:
    >>> plan = SeedsPlan(
    ...     users=SeedUsersPlan(
    ...         count=10,
    ...         deposit_accounts=SeedAccountsPlan(count=2)
    ...     )
    ... )
"""

from pydantic import BaseModel, Field, ConfigDict

class SeedCardsPlan(BaseModel):
    """План генерации карт для счёта.

    Attributes:
        count: Количество карт для генерации.

    Пример использования:
        >>> plan = SeedCardsPlan(count=2)
    """
    count: int = 0

class SeedOperationsPlan(BaseModel):
    """План генерации операций для счёта.

    Attributes:
        count: Количество операций для генерации.

    Пример использования:
        >>> plan = SeedOperationsPlan(count=5)
    """
    count: int = 0

class SeedAccountsPlan(BaseModel):
    """План генерации счетов с связанными картами и операциями.

    Attributes:
        count: Количество счетов для генерации.
        physical_cards: План генерации физических карт.
        virtual_cards: План генерации виртуальных карт.
        top_up_operations: План генерации операций пополнения.
        purchase_operations: План генерации операций покупки.
        cashback_operations: План генерации операций кэшбэка.
        transfer_operations: План генерации операций перевода.
        bill_payment_operations: План генерации операций оплаты счетов.
        cash_withdrawal_operations: План генерации операций снятия наличных.

    Пример использования:
        >>> plan = SeedAccountsPlan(
        ...     count=2,
        ...     physical_cards=SeedCardsPlan(count=1),
        ...     purchase_operations=SeedOperationsPlan(count=10)
        ... )
    """
    count: int = 0
    physical_cards: SeedCardsPlan = Field(default_factory=SeedCardsPlan)
    virtual_cards: SeedCardsPlan = Field(default_factory=SeedCardsPlan)

    top_up_operations: SeedOperationsPlan = Field(default_factory=SeedOperationsPlan)
    purchase_operations: SeedOperationsPlan = Field(default_factory=SeedOperationsPlan)

    cashback_operations: SeedOperationsPlan = Field(default_factory=SeedOperationsPlan)
    transfer_operations: SeedOperationsPlan = Field(default_factory=SeedOperationsPlan)
    bill_payment_operations: SeedOperationsPlan = Field(default_factory=SeedOperationsPlan)
    cash_withdrawal_operations: SeedOperationsPlan = Field(default_factory=SeedOperationsPlan)


class SeedUsersPlan(BaseModel):
    """План генерации пользователей с связанными счетами.

    Attributes:
        count: Количество пользователей для генерации.
        deposit_accounts: План генерации депозитных счетов.
        saving_accounts: План генерации накопительных счетов.
        credit_card_accounts: План генерации кредитных счетов.
        debit_card_accounts: План генерации дебетовых счетов.

    Пример использования:
        >>> plan = SeedUsersPlan(
        ...     count=10,
        ...     credit_card_accounts=SeedAccountsPlan(count=1),
        ...     debit_card_accounts=SeedAccountsPlan(count=2)
        ... )
    """
    count: int = 0
    deposit_accounts: SeedAccountsPlan = Field(default_factory=SeedAccountsPlan)
    saving_accounts: SeedAccountsPlan = Field(default_factory=SeedAccountsPlan)
    credit_card_accounts: SeedAccountsPlan = Field(default_factory=SeedAccountsPlan)
    debit_card_accounts: SeedAccountsPlan = Field(default_factory=SeedAccountsPlan)


class SeedsPlan(SeedUsersPlan):
    """Корневой план генерации всех тестовых данных.

    Наследуется от SeedUsersPlan и добавляет поле users для
    конфигурации генерации пользователей.

    Attributes:
        users: План генерации пользователей.

    Пример использования:
        >>> plan = SeedsPlan(
        ...     users=SeedUsersPlan(
        ...         count=100,
        ...         debit_card_accounts=SeedAccountsPlan(count=2)
        ...     )
        ... )
    """
    users: SeedUsersPlan = Field(default_factory=SeedUsersPlan)