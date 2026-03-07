"""Event hooks для интеграции HTTP запросов с Locust.

Модуль предоставляет функции обратного вызова для httpx event hooks,
которые перехватывают HTTP запросы и ответы, отправляя метрики в Locust.
"""

from httpx import Request, Response, HTTPError, HTTPStatusError
from locust.env import Environment
import time

def locust_request_event_hook(request: Request) -> None:
    """Зафиксировать время начала HTTP запроса.

    Сохраняет timestamp начала запроса в extensions для последующего
    расчёта времени выполнения в response hook.

    Args:
        request: Объект HTTP запроса.
    """
    request.extensions['start_time'] = time.time()

def locust_response_event_hook(environment: Environment):
    """Создать обработчик HTTP ответов для отправки метрик в Locust.

    Фабричная функция, возвращающая обработчик ответов, который:
    - Извлекает время начала запроса из extensions
    - Вычисляет время выполнения и размер ответа
    - Отправляет событие request в Locust

    Args:
        environment: Экземпляр окружения Locust.

    Returns:
        Функция-обработчик HTTP ответов.

    Example:
        >>> hook = locust_response_event_hook(env)
        >>> client = Client(event_hooks={'response': [hook]})
    """
    def inner(response: Response) -> None:
        request = response.request
        route = request.extensions.get('route', request.url.path)
        exception: HTTPError | HTTPStatusError | None = None
        start_time = request.extensions.get('start_time', time.time())
        response_time = (time.time() - start_time) * 1000
        response_length = len(response.read())
        try:
            response = response.raise_for_status()
        except (HTTPError, HTTPStatusError) as e:
            exception = e

        environment.events.request.fire(
            name=f'{request.method} {route}',
            context=None,
            response=response,
            exception=exception,
            request_type='HTTP',
            response_time=response_time,
            response_length=response_length
        )

    return inner