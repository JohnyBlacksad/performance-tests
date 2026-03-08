"""Pydantic-модели для представления результатов генерации тестовых данных.

Модели описывают структуру результатов после генерации:
- Пользователей
- Счетов
- Карт
- Операций

Пример использования:
    >>> result = SeedsResult(users=[...])
    >>> user = result.get_next_user()
"""

from pydantic import BaseModel, Field
from random import choice

class SeedCardResult(BaseModel):
    """Результат генерации карты.

    Attributes:
        card_id: Уникальный идентификатор сгенерированной карты.

    Пример использования:
        >>> card = SeedCardResult(card_id='card_123')
    """
    card_id: str

class SeedOperationResult(BaseModel):
    """Результат генерации операции.

    Attributes:
        operation_id: Уникальный идентификатор сгенерированной операции.

    Пример использования:
        >>> operation = SeedOperationResult(operation_id='op_456')
    """
    operation_id: str

class SeedAccountResult(BaseModel):
    """Результат генерации счёта.

    Attributes:
        account_id: Уникальный идентификатор сгенерированного счёта.
        physical_cards: Список сгенерированных физических карт.
        virtual_cards: Список сгенерированных виртуальных карт.
        top_up_operations: Список сгенерированных операций пополнения.
        purchase_operations: Список сгенерированных операций покупки.
        cashback_operations: Список сгенерированных операций кэшбэка.
        transfer_operations: Список сгенерированных операций перевода.
        bill_payment_operations: Список сгенерированных операций оплаты счетов.
        cash_withdrawal_operations: Список сгенерированных операций снятия наличных.

    Пример использования:
        >>> account = SeedAccountResult(
        ...     account_id='acc_123',
        ...     physical_cards=[SeedCardResult(card_id='card_1')]
        ... )
    """
    account_id: str

    physical_cards: list[SeedCardResult] = Field(default_factory=list)
    virtual_cards: list[SeedCardResult] = Field(default_factory=list)

    top_up_operations: list[SeedOperationResult] = Field(default_factory=list)
    purchase_operations: list[SeedOperationResult] = Field(default_factory=list)
    cashback_operations: list[SeedOperationResult] = Field(default_factory=list)
    transfer_operations: list[SeedOperationResult] = Field(default_factory=list)
    bill_payment_operations: list[SeedOperationResult] = Field(default_factory=list)
    cash_withdrawal_operations: list[SeedOperationResult] = Field(default_factory=list)

class SeedUserResult(BaseModel):
    """Результат генерации пользователя.

    Attributes:
        user_id: Уникальный идентификатор сгенерированного пользователя.
        deposit_accounts: Список сгенерированных депозитных счетов.
        saving_accounts: Список сгенерированных накопительных счетов.
        credit_card_accounts: Список сгенерированных кредитных счетов.
        debit_card_accounts: Список сгенерированных дебетовых счетов.

    Пример использования:
        >>> user = SeedUserResult(
        ...     user_id='user_123',
        ...     debit_card_accounts=[SeedAccountResult(account_id='acc_1')]
        ... )
    """
    user_id: str
    deposit_accounts: list[SeedAccountResult] = Field(default_factory=list)
    saving_accounts: list[SeedAccountResult] = Field(default_factory=list)
    credit_card_accounts: list[SeedAccountResult] = Field(default_factory=list)
    debit_card_accounts: list[SeedAccountResult] = Field(default_factory=list)

class SeedsResult(BaseModel):
    """Результат генерации всех тестовых данных.

    Содержит список сгенерированных пользователей и предоставляет
    методы для получения пользователей для тестов.

    Attributes:
        users: Список сгенерированных пользователей.

    Пример использования:
        >>> result = SeedsResult(users=[user1, user2])
        >>> user = result.get_next_user()
    """
    users: list[SeedUserResult] = Field(default_factory=list)

    def get_next_user(self) -> SeedUserResult:
        """Получить следующего пользователя из списка (извлекает первого).

        Извлекает и возвращает первого пользователя из списка,
        удаляя его из списка.

        Returns:
            SeedUserResult: Данные следующего пользователя.

        Raises:
            IndexError: Если список пользователей пуст.

        Example:
            >>> result = SeedsResult(users=[user1, user2])
            >>> user = result.get_next_user()
        """
        return self.users.pop(0)

    def get_random_user(self) -> SeedUserResult:
        """Получить случайного пользователя из списка.

        Возвращает случайного пользователя из списка без удаления.

        Returns:
            SeedUserResult: Данные случайного пользователя.

        Raises:
            IndexError: Если список пользователей пуст.

        Example:
            >>> result = SeedsResult(users=[user1, user2])
            >>> user = result.get_random_user()
        """
        return choice(self.users)