"""Интерцептор для интеграции gRPC вызовов с Locust.

Модуль предоставляет класс LocustInterceptor — интерцептор для gRPC,
который перехватывает unary-unary вызовы и отправляет метрики
производительности в Locust.
"""

from collections.abc import Callable
import time
from grpc import _CallFuture, _TRequest, _TResponse, ClientCallDetails, UnaryUnaryClientInterceptor, RpcError
from locust.env import Environment

class LocustInterceptor(UnaryUnaryClientInterceptor):
    """Интерцептор для сбора метрик gRPC вызовов в Locust.

    Перехватывает unary-unary вызовы, измеряет время выполнения
    и размер ответа, отправляя данные в события Locust.

    Attributes:
        environment: Экземпляр окружения Locust для отправки событий.

    Example:
        >>> interceptor = LocustInterceptor(environment=env)
        >>> channel = intercept_channel(base_channel, interceptor)
    """
    def __init__(self, environment: Environment) -> None:
        """Инициализировать интерцептор.

        Args:
            environment: Экземпляр окружения Locust.
        """
        self.environment = environment
        super().__init__()

    def intercept_unary_unary(self, continuation: Callable[[ClientCallDetails, _TRequest], _CallFuture[_TResponse]], client_call_details: ClientCallDetails, request: _TRequest) -> _CallFuture[_TResponse]:
        """Перехватить unary-unary gRPC вызов.

        Измеряет время выполнения вызова, размер ответа и отправляет
        метрики в Locust через события request.

        Args:
            continuation: Функция продолжения вызова.
            client_call_details: Детали вызова клиента.
            request: Запрос protobuf.

        Returns:
            Будущий результат вызова (CallFuture).
        """
        response = None
        exception: RpcError | None = None
        start_time = time.perf_counter()
        response_length = 0
        try:
            response = continuation(client_call_details, request)
            response_length = response.result().ByteSize() # type: ignore
        except RpcError as e:
            exception = e

        self.environment.events.request.fire(
            name = client_call_details.method,
            context = None,
            response = response,
            exception = exception,
            request_type = "gRPC",
            response_time = (time.perf_counter() - start_time) * 1000,
            response_length = response_length
        )


        return response # type: ignore