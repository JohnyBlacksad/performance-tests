"""Сценарий нагрузочного тестирования: создание и получение пользователя.

Модуль содержит класс GetUserScenarioUser для Locust, который:
1. Создаёт нового пользователя через POST /api/v1/users
2. Выполняет GET запросы к созданному пользователю

Пример запуска:
    locust -f tools/locust_get_user_scenario.py --host=http://localhost:8003
"""

from locust import HttpUser, between, task
from tools.fakers import faker_ru

class GetUserScenarioUser(HttpUser):
    """Пользователь для сценария тестирования пользователя.

    Сценарий создаёт пользователя при старте и периодически
    выполняет запросы на получение его данных.

    Attributes:
        wait_time: Время ожидания между задачами (1-3 секунды).
        user_data: Данные созданного пользователя.
    """
    wait_time = between(1, 3)
    user_data: dict

    def on_start(self) -> None:
        """Создать нового пользователя при старте воркера.

        Отправляет POST-запрос на создание пользователя с фейковыми данными
        и сохраняет ответ для последующих запросов.
        """
        request = {
            "email": faker_ru.email(),
            "lastName": faker_ru.last_name(),
            "firstName": faker_ru.first_name(),
            "middleName": faker_ru.middle_name(),
            "phoneNumber": faker_ru.phone_number()
        }
        response = self.client.post("/api/v1/users", json=request)
        self.user_data = response.json()

    @task
    def get_user(self):
        """Получить данные пользователя по ID.

        Выполняет GET-запрос к эндпоинту /api/v1/users/{user_id}.
        """
        self.client.get(f'/api/v1/users/{self.user_data.get('user').get('id')}', name='/api/v1/users/{user_id}') # type: ignore