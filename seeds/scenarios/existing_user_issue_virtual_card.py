"""Сценарий генерации данных для выпуска виртуальной карты.

Генерирует пользователей с дебетовыми счетами для тестирования
сценария выпуска виртуальной карты.
"""

from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan

class ExistingUserIssueVirtualCardSeedsScenario(SeedsScenario):
    """Сценарий генерации данных для выпуска виртуальной карты.

    Создаёт пользователей с дебетовыми счетами для тестирования
    операций выпуска виртуальных карт.

    Example:
        >>> scenario = ExistingUserIssueVirtualCardSeedsScenario()
        >>> scenario.build()
    """
    @property
    def plan(self) -> SeedsPlan:
        """Вернуть план генерации тестовых данных.

        Returns:
            SeedsPlan: План с 300 пользователями, имеющими по одному
                дебетовому счёту.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,
                debit_card_accounts=SeedAccountsPlan(count=1)
            )
        )

    @property
    def scenario(self) -> str:
        """Вернуть имя сценария.

        Returns:
            str: 'existing_user_issue_virtual_card'
        """
        return 'existing_user_issue_virtual_card'

if __name__ == '__main__':
    seed_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    seed_scenario.build()
