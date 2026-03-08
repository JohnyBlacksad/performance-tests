"""Builder для генерации тестовых данных (seeds) для нагрузочного тестирования.

Модуль предоставляет класс SeedsBuilder для создания тестовых данных:
- Пользователи с различными типами счетов
- Карты (физические и виртуальные)
- Операции (пополнения, покупки, кэшбэки, переводы и т.д.)

Поддерживает работу как с gRPC, так и с HTTP клиентами.

Пример использования:
    >>> builder = build_grpc_seeds_builder()
    >>> plan = SeedsPlan(users=SeedUsersPlan(count=10))
    >>> result = builder.build(plan)
"""

from clients.grpc.gateway.users.client import UserGatewayGRPCClient, build_users_gateway_grpc_client
from clients.grpc.gateway.cards.client import CardsGatewayGRPCClient, build_cards_gateway_client
from clients.grpc.gateway.accounts.client import AccountsGatewayGRPCClient, build_accounts_gateway_client
from clients.grpc.gateway.operations.client import OperationsGatewayGRPCClient, build_operations_gateway_grpc_client


from clients.http.gateway.users.client import UserGatewayHTTPClient, build_users_gateway_http_client
from clients.http.gateway.cards.client import CardsGatewayHTTPClient, build_cards_gateway_http_client
from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient, build_accounts_gateway_http_client
from clients.http.gateway.operations.client import OperationsGatewayHTTPClient, build_operations_gateway_http_client

from seeds.schema.plan import SeedAccountsPlan, SeedUsersPlan, SeedsPlan
from seeds.schema.result import SeedAccountResult, SeedCardResult, SeedOperationResult, SeedUserResult, SeedsResult

class SeedsBuilder:
    """Builder для создания тестовых данных (seeds) для нагрузочного тестирования.

    Предоставляет методы для генерации пользователей, счетов, карт и операций
    через gRPC или HTTP клиенты Gateway сервисов.

    Attributes:
        user_client: Клиент для сервиса пользователей.
        cards_client: Клиент для сервиса карт.
        accounts_client: Клиент для сервиса счетов.
        operations_client: Клиент для сервиса операций.

    Пример использования:
        >>> builder = build_grpc_seeds_builder()
        >>> plan = SeedsPlan(users=SeedUsersPlan(count=10))
        >>> result = builder.build(plan)
    """
    def __init__(
        self,
        users_client: UserGatewayGRPCClient | UserGatewayHTTPClient,
        cards_client: CardsGatewayGRPCClient | CardsGatewayHTTPClient,
        accounts_client: AccountsGatewayGRPCClient | AccountsGatewayHTTPClient,
        operations_client: OperationsGatewayGRPCClient | OperationsGatewayHTTPClient
    ) -> None:
        """Инициализировать SeedsBuilder с клиентами Gateway сервисов.

        Args:
            users_client: Клиент для сервиса пользователей.
            cards_client: Клиент для сервиса карт.
            accounts_client: Клиент для сервиса счетов.
            operations_client: Клиент для сервиса операций.

        Example:
            >>> builder = SeedsBuilder(
            ...     users_client=build_users_gateway_grpc_client(),
            ...     cards_client=build_cards_gateway_client(),
            ...     accounts_client=build_accounts_gateway_client(),
            ...     operations_client=build_operations_gateway_grpc_client()
            ... )
        """
        self.user_client = users_client
        self.cards_client = cards_client
        self.accounts_client = accounts_client
        self.operations_client = operations_client

    def build_physical_card_result(self, user_id: str, account_id: str) -> SeedCardResult:
        """Создать результат выпуска физической карты.

        Отправляет запрос на выпуск физической карты и возвращает
        результат с идентификатором карты.

        Args:
            user_id: Уникальный идентификатор пользователя.
            account_id: Уникальный идентификатор счёта.

        Returns:
            SeedCardResult с идентификатором выпущенной карты.

        Example:
            >>> result = builder.build_physical_card_result(
            ...     user_id='u123',
            ...     account_id='a456'
            ... )
        """
        response = self.cards_client.issue_physical_card(user_id=user_id, account_id=account_id)
        return SeedCardResult(card_id=response.card.id)

    def build_virtual_card_result(self, user_id: str, account_id: str) -> SeedCardResult:
        """Создать результат выпуска виртуальной карты.

        Отправляет запрос на выпуск виртуальной карты и возвращает
        результат с идентификатором карты.

        Args:
            user_id: Уникальный идентификатор пользователя.
            account_id: Уникальный идентификатор счёта.

        Returns:
            SeedCardResult с идентификатором выпущенной карты.

        Example:
            >>> result = builder.build_virtual_card_result(
            ...     user_id='u123',
            ...     account_id='a456'
            ... )
        """
        response = self.cards_client.issue_virtual_card(user_id=user_id, account_id=account_id)
        return SeedCardResult(card_id=response.card.id)

    def build_cashback_operations_result(self, card_id: str, account_id: str) -> SeedOperationResult:
        """Создать результат операции кэшбэка.

        Отправляет запрос на создание операции кэшбэка и возвращает
        результат с идентификатором операции.

        Args:
            card_id: Уникальный идентификатор карты.
            account_id: Уникальный идентификатор счёта.

        Returns:
            SeedOperationResult с идентификатором операции.

        Example:
            >>> result = builder.build_cashback_operations_result(
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
        """
        response = self.operations_client.make_cashback_operation(account_id=account_id, card_id=card_id)
        return SeedOperationResult(operation_id=response.operation.id)

    def build_transfer_operations_result(self, card_id: str, account_id: str) -> SeedOperationResult:
        """Создать результат операции перевода.

        Отправляет запрос на создание операции перевода и возвращает
        результат с идентификатором операции.

        Args:
            card_id: Уникальный идентификатор карты.
            account_id: Уникальный идентификатор счёта.

        Returns:
            SeedOperationResult с идентификатором операции.

        Example:
            >>> result = builder.build_transfer_operations_result(
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
        """
        response = self.operations_client.make_transfer_operation(card_id=card_id, account_id=account_id)
        return SeedOperationResult(operation_id=response.operation.id)

    def build_bill_payment_operations_result(self, card_id: str, account_id: str) -> SeedOperationResult:
        """Создать результат операции оплаты счёта.

        Отправляет запрос на создание операции оплаты счёта и возвращает
        результат с идентификатором операции.

        Args:
            card_id: Уникальный идентификатор карты.
            account_id: Уникальный идентификатор счёта.

        Returns:
            SeedOperationResult с идентификатором операции.

        Example:
            >>> result = builder.build_bill_payment_operations_result(
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
        """
        response = self.operations_client.make_bill_payment_operation(card_id=card_id, account_id=account_id)
        return SeedOperationResult(operation_id=response.operation.id)

    def build_cash_withdrawal_operations_result(self, card_id: str, account_id: str) -> SeedOperationResult:
        """Создать результат операции снятия наличных.

        Отправляет запрос на создание операции снятия наличных и возвращает
        результат с идентификатором операции.

        Args:
            card_id: Уникальный идентификатор карты.
            account_id: Уникальный идентификатор счёта.

        Returns:
            SeedOperationResult с идентификатором операции.

        Example:
            >>> result = builder.build_cash_withdrawal_operations_result(
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
        """
        response = self.operations_client.make_cash_withdrawal_operation(account_id=account_id, card_id=card_id)
        return SeedOperationResult(operation_id=response.operation.id)


    def build_top_up_operations_result(self, card_id: str, account_id: str) -> SeedOperationResult:
        """Создать результат операции пополнения счёта.

        Отправляет запрос на создание операции пополнения и возвращает
        результат с идентификатором операции.

        Args:
            card_id: Уникальный идентификатор карты.
            account_id: Уникальный идентификатор счёта.

        Returns:
            SeedOperationResult с идентификатором операции.

        Example:
            >>> result = builder.build_top_up_operations_result(
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
        """
        response = self.operations_client.make_top_up_operation(card_id=card_id, account_id=account_id)
        return SeedOperationResult(operation_id=response.operation.id)

    def build_purchase_operations_result(self, card_id: str, account_id: str) -> SeedOperationResult:
        """Создать результат операции покупки.

        Отправляет запрос на создание операции покупки и возвращает
        результат с идентификатором операции.

        Args:
            card_id: Уникальный идентификатор карты.
            account_id: Уникальный идентификатор счёта.

        Returns:
            SeedOperationResult с идентификатором операции.

        Example:
            >>> result = builder.build_purchase_operations_result(
            ...     card_id='c1',
            ...     account_id='a1'
            ... )
        """
        response = self.operations_client.make_purchase_operation(card_id=card_id, account_id=account_id)
        return SeedOperationResult(operation_id=response.operation.id)

    def build_savings_account_result(self, user_id: str) -> SeedAccountResult:
        """Создать результат открытия накопительного счёта.

        Отправляет запрос на открытие накопительного счёта и возвращает
        результат с идентификатором счёта.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            SeedAccountResult с идентификатором открытого счёта.

        Example:
            >>> result = builder.build_savings_account_result(user_id='u123')
        """
        response = self.accounts_client.open_saving_account(user_id)
        return SeedAccountResult(account_id=response.account.id)

    def build_deposit_account_result(self, user_id: str) -> SeedAccountResult:
        """Создать результат открытия депозитного счёта.

        Отправляет запрос на открытие депозитного счёта и возвращает
        результат с идентификатором счёта.

        Args:
            user_id: Уникальный идентификатор пользователя.

        Returns:
            SeedAccountResult с идентификатором открытого счёта.

        Example:
            >>> result = builder.build_deposit_account_result(user_id='u123')
        """
        response = self.accounts_client.open_deposit_account(user_id)
        return SeedAccountResult(account_id=response.account.id)

    def build_credit_card_account_result(self, plan: SeedAccountsPlan, user_id: str) -> SeedAccountResult:
        """Создать результат открытия кредитного счёта с картами и операциями.

        Отправляет запрос на открытие кредитного счёта, выпускает карты
        и создаёт операции согласно плану.

        Args:
            plan: План генерации карт и операций (SeedAccountsPlan).
            user_id: Уникальный идентификатор пользователя.

        Returns:
            SeedAccountResult с идентификатором счёта, картами и операциями.

        Example:
            >>> plan = SeedAccountsPlan(
            ...     physical_cards=SeedCardsPlan(count=1),
            ...     purchase_operations=SeedOperationsPlan(count=5)
            ... )
            >>> result = builder.build_credit_card_account_result(
            ...     plan=plan,
            ...     user_id='u123'
            ... )
        """
        response = self.accounts_client.open_credit_card_account(user_id)
        account_id = response.account.id
        card_id = response.account.cards[0].id
        return SeedAccountResult(
            account_id=response.account.id,
            physical_cards=[self.build_physical_card_result(account_id=account_id, user_id=user_id) for _ in range(plan.physical_cards.count)],
            virtual_cards=[self.build_virtual_card_result(account_id=account_id, user_id=user_id) for _ in range(plan.virtual_cards.count)],
            top_up_operations=[self.build_top_up_operations_result(card_id=card_id, account_id=account_id) for _ in range(plan.top_up_operations.count)],
            purchase_operations=[self.build_purchase_operations_result(card_id=card_id, account_id=account_id) for _ in range(plan.purchase_operations.count)],
            cashback_operations=[self.build_cashback_operations_result(account_id=account_id, card_id=card_id) for _ in range(plan.cashback_operations.count)],
            transfer_operations=[self.build_transfer_operations_result(account_id=account_id, card_id=card_id) for _ in range(plan.transfer_operations.count)],
            bill_payment_operations=[self.build_bill_payment_operations_result(account_id=account_id, card_id=card_id) for _ in range(plan.bill_payment_operations.count)],
            cash_withdrawal_operations=[self.build_cash_withdrawal_operations_result(account_id=account_id, card_id=card_id) for _ in range(plan.cash_withdrawal_operations.count)])

    def build_debit_card_accounts_result(self, plan: SeedAccountsPlan, user_id: str) -> SeedAccountResult:
        """Создать результат открытия дебетового счёта с картами и операциями.

        Отправляет запрос на открытие дебетового счёта, выпускает карты
        и создаёт операции согласно плану.

        Args:
            plan: План генерации карт и операций (SeedAccountsPlan).
            user_id: Уникальный идентификатор пользователя.

        Returns:
            SeedAccountResult с идентификатором счёта, картами и операциями.

        Example:
            >>> plan = SeedAccountsPlan(
            ...     physical_cards=SeedCardsPlan(count=1),
            ...     purchase_operations=SeedOperationsPlan(count=10)
            ... )
            >>> result = builder.build_debit_card_accounts_result(
            ...     plan=plan,
            ...     user_id='u123'
            ... )
        """
        response = self.accounts_client.open_deposit_account(user_id)
        account_id = response.account.id
        card_id = response.account.cards[0].id
        return SeedAccountResult(
            account_id=response.account.id,
            physical_cards=[self.build_physical_card_result(account_id=account_id, user_id=user_id) for _ in range(plan.physical_cards.count)],
            virtual_cards=[self.build_virtual_card_result(account_id=account_id, user_id=user_id) for _ in range(plan.virtual_cards.count)],
            top_up_operations=[self.build_top_up_operations_result(card_id=card_id, account_id=account_id) for _ in range(plan.top_up_operations.count)],
            purchase_operations=[self.build_purchase_operations_result(card_id=card_id, account_id=account_id) for _ in range(plan.purchase_operations.count)],
            cashback_operations=[self.build_cashback_operations_result(account_id=account_id, card_id=card_id) for _ in range(plan.cashback_operations.count)],
            transfer_operations=[self.build_transfer_operations_result(account_id=account_id, card_id=card_id) for _ in range(plan.transfer_operations.count)],
            bill_payment_operations=[self.build_bill_payment_operations_result(account_id=account_id, card_id=card_id) for _ in range(plan.bill_payment_operations.count)],
            cash_withdrawal_operations=[self.build_cash_withdrawal_operations_result(account_id=account_id, card_id=card_id) for _ in range(plan.cash_withdrawal_operations.count)])

    def build_user(self, plan: SeedUsersPlan) -> SeedUserResult:
        """Создать результат генерации пользователя со счетами.

        Отправляет запрос на создание пользователя, затем создаёт
        все счета согласно плану (депозитные, накопительные, кредитные, дебетовые).

        Args:
            plan: План генерации счетов для пользователя (SeedUsersPlan).

        Returns:
            SeedUserResult с идентификатором пользователя и всеми счетами.

        Example:
            >>> plan = SeedUsersPlan(
            ...     deposit_accounts=SeedAccountsPlan(count=1),
            ...     debit_card_accounts=SeedAccountsPlan(count=2)
            ... )
            >>> result = builder.build_user(plan=plan)
        """
        response = self.user_client.create_user()
        return SeedUserResult(
            user_id=response.user.id,
            deposit_accounts=[self.build_deposit_account_result(response.user.id) for _ in range(plan.deposit_accounts.count)],
            saving_accounts=[self.build_savings_account_result(user_id=response.user.id) for _ in range(plan.saving_accounts.count)],
            credit_card_accounts=[self.build_credit_card_account_result(plan=plan.credit_card_accounts, user_id=response.user.id) for _ in range(plan.credit_card_accounts.count)],
            debit_card_accounts=[self.build_debit_card_accounts_result(plan=plan.debit_card_accounts, user_id=response.user.id) for _ in range(plan.debit_card_accounts.count)],
        )

    def build(self, plan: SeedsPlan) -> SeedsResult:
        """Сгенерировать тестовые данные по плану.

        Создаёт указанное количество пользователей со всеми связанными
        счетами, картами и операциями согласно плану.

        Args:
            plan: План генерации тестовых данных (SeedsPlan).

        Returns:
            SeedsResult с результатами генерации.

        Example:
            >>> builder = build_grpc_seeds_builder()
            >>> plan = SeedsPlan(users=SeedUsersPlan(count=10))
            >>> result = builder.build(plan)
        """
        return SeedsResult(users=[self.build_user(plan.users) for _ in range(plan.users.count)])

def build_grpc_seeds_builder() -> SeedsBuilder:
    """Создать SeedsBuilder с gRPC клиентами.

    Возвращает настроенный экземпляр SeedsBuilder для работы
    с Gateway сервисами через gRPC.

    Returns:
        Настроенный экземпляр SeedsBuilder с gRPC клиентами.

    Example:
        >>> builder = build_grpc_seeds_builder()
        >>> result = builder.build(plan)
    """
    return SeedsBuilder(
        users_client=build_users_gateway_grpc_client(),
        accounts_client=build_accounts_gateway_client(),
        operations_client=build_operations_gateway_grpc_client(),
        cards_client=build_cards_gateway_client()
    )

def build_http_seeds_builder() -> SeedsBuilder:
    """Создать SeedsBuilder с HTTP клиентами.

    Возвращает настроенный экземпляр SeedsBuilder для работы
    с Gateway сервисами через HTTP.

    Returns:
        Настроенный экземпляр SeedsBuilder с HTTP клиентами.

    Example:
        >>> builder = build_http_seeds_builder()
        >>> result = builder.build(plan)
    """
    return SeedsBuilder(
        users_client=build_users_gateway_http_client(),
        accounts_client=build_accounts_gateway_http_client(),
        operations_client=build_operations_gateway_http_client(),
        cards_client=build_cards_gateway_http_client()
    )