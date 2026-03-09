"""Базовый класс пользователя для Locust-тестов.

Модуль предоставляет базовый класс LocustBaseUser с предустановленными
настройками для всех сценариев нагрузочного тестирования.

Пример использования:
    class MyUser(LocustBaseUser):
        tasks = [MyTaskSet]
"""

from locust import User, between
from config import settings

class LocustBaseUser(User):
    """Базовый класс пользователя для Locust-тестов.

    Предоставляет стандартные настройки для всех пользовательских
    сценариев:
    - host: 'localhost'
    - wait_time: от 1 до 3 секунд между задачами
    - abstract: True (не регистрируется как отдельный пользователь)

    Attributes:
        host: Базовый URL для тестирования.
        abstract: Флаг абстрактного класса (не регистрируется в Locust).
        wait_time: Время ожидания между выполнением задач.

    Пример использования:
        >>> class MyUser(LocustBaseUser):
        ...     tasks = [MyTaskSet]
    """
    host = 'localhost'
    abstract = True
    wait_time = between(
        min_wait=settings.locust_user.min_wait,
        max_wait=settings.locust_user.max_wait
    )