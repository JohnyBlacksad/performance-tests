"""Сценарий генерации данных для получения документов существующим пользователем.

Генерирует пользователей с накопительными и депозитными счетами
для тестирования сценария получения документов.
"""

from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan

class ExistingUserGetDocumentsSeedScenario(SeedsScenario):
    """Сценарий генерации данных для получения документов.

    Создаёт пользователей с накопительными и депозитными счетами
    для тестирования операций получения документов.

    Example:
        >>> scenario = ExistingUserGetDocumentsSeedScenario()
        >>> scenario.build()
    """
    @property
    def plan(self) -> SeedsPlan:
        """Вернуть план генерации тестовых данных.

        Returns:
            SeedsPlan: План с 100 пользователями, имеющими по одному
                накопительному и одному депозитному счёту.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=100,
                saving_accounts=SeedAccountsPlan(count=1),
                deposit_accounts=SeedAccountsPlan(count=1)
            )
        )

    @property
    def scenario(self) -> str:
        """Вернуть имя сценария.

        Returns:
            str: 'existing_user_get_documents'
        """
        return 'existing_user_get_documents'

if __name__ == "__main__":
    seed_scenario = ExistingUserGetDocumentsSeedScenario()
    seed_scenario.build()