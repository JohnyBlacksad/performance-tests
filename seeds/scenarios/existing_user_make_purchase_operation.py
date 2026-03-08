"""Сценарий генерации данных для совершения покупки.

Генерирует пользователей с кредитными счетами и физическими картами
для тестирования сценария совершения покупок.
"""

from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan, SeedCardsPlan


class ExistingUserMakePurchaseOperationSeedsScenario(SeedsScenario):
    """Сценарий генерации данных для совершения операций покупки.

    Создаёт пользователей с кредитными счетами и физическими картами
    для тестирования операций покупки.

    Example:
        >>> scenario = ExistingUserMakePurchaseOperationSeedsScenario()
        >>> scenario.build()
    """

    @property
    def plan(self) -> SeedsPlan:
        """Вернуть план генерации тестовых данных.

        Returns:
            SeedsPlan: План с 300 пользователями, имеющими по одному
                кредитному счёту с одной физической картой.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,
                credit_card_accounts=SeedAccountsPlan(
                    count=1,
                    physical_cards=SeedCardsPlan(count=1)
                )
            )
        )

    @property
    def scenario(self) -> str:
        """Вернуть имя сценария.

        Returns:
            str: 'existing_user_make_purchase_operation'
        """
        return 'existing_user_make_purchase_operation'

if __name__ == '__main__':
    seeds_scenario = ExistingUserMakePurchaseOperationSeedsScenario()
    seeds_scenario.build()
    seeds_scenario.load()