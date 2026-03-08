"""Утилиты для сохранения и загрузки результатов генерации тестовых данных.

Модуль предоставляет функции для сериализации результатов генерации
в JSON-файлы и последующей десериализации.

Пример использования:
    >>> save_seeds_results(result, 'my_scenario')
    >>> result = load_seeds_results('my_scenario')
"""

from seeds.schema.result import SeedsResult
import os

def save_seeds_results(result: SeedsResult, scenario: str) -> None:
    """Сохранить результаты генерации тестовых данных в JSON-файл.

    Создаёт директорию 'dumps' (если не существует) и сохраняет
    результаты в файл с именем {scenario}_seeds.json.

    Args:
        result: Результаты генерации тестовых данных (SeedsResult).
        scenario: Имя сценария, используемое в имени файла.

    Example:
        >>> result = builder.build(plan)
        >>> save_seeds_results(result, 'my_scenario')
    """
    if not os.path.exists('dumps'):
        os.mkdir('dumps')

    with open(f'./dumps/{scenario}_seeds.json', 'w+', encoding='utf-8') as file:
        file.write(result.model_dump_json())

def load_seeds_results(scenario: str) -> SeedsResult:
    """Загрузить результаты генерации тестовых данных из JSON-файла.

    Читает файл {scenario}_seeds.json из директории 'dumps' и
    возвращает десериализованный объект SeedsResult.

    Args:
        scenario: Имя сценария, используемое в имени файла.

    Returns:
        SeedsResult: Загруженные результаты генерации.

    Raises:
        FileNotFoundError: Если файл не существует.
        ValidationError: Если данные не соответствуют схеме SeedsResult.

    Example:
        >>> result = load_seeds_results('my_scenario')
    """
    with open(f'./dumps/{scenario}_seeds.json', 'r', encoding='utf-8') as file:
       return SeedsResult.model_validate_json(file.read())