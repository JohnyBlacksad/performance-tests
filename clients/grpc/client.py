"""Клиенты и фабрики для gRPC подключений.

Модуль предоставляет базовый класс GRPCClient и функции для создания
gRPC каналов, включая поддержку интеграции с Locust.
"""

from locust.env import Environment
from grpc import Channel, insecure_channel, intercept_channel
from clients.grpc.interceptors.locust_interceptor import LocustInterceptor
import grpc.experimental.gevent as grpc_gevent

grpc_gevent.init_gevent()

class GRPCClient:
    """Базовый класс для gRPC клиентов.

    Обёртка над gRPC каналом для упрощения работы с gRPC сервисами.

    Attributes:
        channel: gRPC канал для связи с сервером.
    """
    def __init__(self, channel: Channel) -> None:
        """Инициализировать gRPC клиент.

        Args:
            channel: gRPC канал для подключения.
        """
        self.channel = channel


def build_gateway_grpc_client() -> Channel:
    """Создать gRPC канал для подключения к Gateway.

    Возвращает нешифрованный канал для localhost:9003.

    Returns:
        gRPC канал для подключения к Gateway сервису.

    Example:
        >>> channel = build_gateway_grpc_client()
        >>> client = SomeGRPCClient(channel)
    """
    return insecure_channel('localhost:9003')


def build_gateway_locust_grpc_client(environment: Environment) -> Channel:
    """Создать gRPC канал с интеграцией Locust для сбора метрик.

    Создаёт канал с интерцептором, который отправляет события
    в Locust для отслеживания производительности gRPC вызовов.

    Args:
        environment: Экземпляр окружения Locust.

    Returns:
        gRPC канал с интерцептором для сбора метрик.

    Example:
        >>> channel = build_gateway_locust_grpc_client(env)
        >>> client = SomeGRPCClient(channel)
    """
    locust_interceptor = LocustInterceptor(environment=environment)
    channel = insecure_channel('localhost:9003')
    return intercept_channel(channel, locust_interceptor)

