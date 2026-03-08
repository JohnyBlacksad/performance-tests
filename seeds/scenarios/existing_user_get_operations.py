"""Сценарий генерации данных для получения операций существующим пользователем.

Генерирует пользователей с кредитными счетами, картами и операциями
для тестирования сценария получения истории операций.
"""

from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan, SeedOperationsPlan

class ExistingUserGetOperationsSeedsScenario(SeedsScenario):
    """Сценарий генерации данных для получения истории операций.

    Создаёт пользователей с кредитными счетами, включая операции
    пополнения, покупки и снятия наличных.

    Example:
        >>> scenario = ExistingUserGetOperationsSeedsScenario()
        >>> scenario.build()
    """
    @property
    def plan(self) -> SeedsPlan:
        """Вернуть план генерации тестовых данных.

        Returns:
            SeedsPlan: План с 300 пользователями, имеющими по одному
                кредитному счёту с операциями (1 пополнение, 5 покупок,
                1 снятие наличных).
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,
                credit_card_accounts=SeedAccountsPlan(
                    count=1,
                    top_up_operations=SeedOperationsPlan(count=1),
                    purchase_operations=SeedOperationsPlan(count=5),
                    cash_withdrawal_operations=SeedOperationsPlan(count=1)
                    )
            )
        )

    @property
    def scenario(self) -> str:
        """Вернуть имя сценария.

        Returns:
            str: 'existing_user_get_operations'
        """
        return 'existing_user_get_operations'


if __name__ == '__main__':
    seed_scenario = ExistingUserGetOperationsSeedsScenario()
    seed_scenario.build()
