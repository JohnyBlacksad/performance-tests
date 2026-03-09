"""Базовый класс для сценариев генерации тестовых данных.

Модуль предоставляет абстрактный класс SeedsScenario для определения
сценариев генерации тестовых данных с возможностью сохранения и загрузки.
"""

from abc import ABC, abstractmethod
from seeds.builder import build_grpc_seeds_builder
from seeds.schema.plan import SeedsPlan
from seeds.schema.result import SeedsResult
from seeds.dumps import save_seeds_results, load_seeds_results
from tools.logger import get_logger

logger = get_logger('SEEDS_SCENARIO')

class SeedsScenario(ABC):
    """Абстрактный базовый класс для сценариев генерации тестовых данных.

    Предоставляет шаблон для создания сценариев генерации данных с
    возможностью сохранения результатов в JSON и загрузки из него.

    Attributes:
        builder: Экземпляр SeedsBuilder для генерации данных.

    Пример использования:
        >>> class MyScenario(SeedsScenario):
        ...     @property
        ...     def plan(self) -> SeedsPlan:
        ...         return SeedsPlan(users=SeedUsersPlan(count=10))
        ...
        ...     @property
        ...     def scenario(self) -> str:
        ...         return 'my_scenario'
    """
    def __init__(self):
        """Инициализировать сценарий с SeedsBuilder."""
        self.builder = build_grpc_seeds_builder()

    @property
    @abstractmethod
    def plan(self) -> SeedsPlan:
        """Вернуть план генерации тестовых данных.

        Returns:
            SeedsPlan: План генерации пользователей, счетов, карт и операций.
        """
        pass

    @property
    @abstractmethod
    def scenario(self) -> str:
        """Вернуть имя сценария.

        Returns:
            str: Имя сценария, используемое для сохранения/загрузки результатов.
        """
        pass

    def save(self, result: SeedsResult) -> None:
        """Сохранить результаты генерации в JSON-файл.

        Args:
            result: Результаты генерации тестовых данных (SeedsResult).

        Example:
            >>> result = builder.build(plan)
            >>> scenario.save(result)
        """
        logger.info(f'[{self.scenario}] Savings seeding result to file.')
        save_seeds_results(result=result, scenario=self.scenario)
        logger.info(f'[{self.scenario}] Seeding result saved successfully.')

    def load(self) -> SeedsResult:
        """Загрузить результаты генерации из JSON-файла.

        Returns:
            SeedsResult: Загруженные результаты генерации.

        Example:
            >>> result = scenario.load()
        """
        logger.info(f'[{self.scenario}] Loading seeding from file.')
        result = load_seeds_results(scenario=self.scenario)
        logger.info(f'[{self.scenario}] Seeding result loaded successfully.')
        return result

    def build(self) -> None:
        """Сгенерировать тестовые данные и сохранить результаты.

        Создаёт тестовые данные согласно плану и сохраняет результаты
        в JSON-файл с именем {scenario}_seeds.json.

        Example:
            >>> scenario = MyScenario()
            >>> scenario.build()
        """
        plan_json = self.plan.model_dump_json(indent=2, exclude_defaults=True)
        logger.info(f'[{self.scenario}] Starting seeding data generation for plan: {plan_json}.')
        result = self.builder.build(self.plan)
        logger.info(f'[{self.scenario}] Seeding data generation completed.')
        self.save(result)