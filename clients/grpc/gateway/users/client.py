"""gRPC клиент для Users Gateway сервиса.

Модуль предоставляет класс UserGatewayGRPCClient для управления пользователями:
- Создание новых пользователей
- Получение данных пользователей по ID

Пример использования:
    >>> client = build_users_gateway_grpc_client()
    >>> user = client.get_user(user_id='u123')
    >>> new_user = client.create_user()
"""

from clients.grpc.client import GRPCClient, build_gateway_grpc_client, build_gateway_locust_grpc_client
from locust.env import Environment
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub
from contracts.services.gateway.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from grpc import Channel
from tools.fakers import faker_ru

class UserGatewayGRPCClient(GRPCClient):
    """gRPC клиент для Users Gateway сервиса.

    Предоставляет методы для создания и получения данных пользователей.

    Example:
        >>> client = build_users_gateway_grpc_client()
        >>> user = client.get_user(user_id='u123')
    """
    def __init__(self, channel: Channel) -> None:
        """Инициализировать клиент для работы с пользователями.

        Args:
            channel: gRPC канал для подключения.
        """
        super().__init__(channel)
        self.stub = UsersGatewayServiceStub(channel)

    def get_user_api(self, request: GetUserRequest) -> GetUserResponse:
        """Получить пользователя по ID (низкоуровневый метод).

        Args:
            request: Запрос на получение пользователя.

        Returns:
            Ответ с данными пользователя.
        """
        return self.stub.GetUser(request)

    def create_user_api(self, request: CreateUserRequest) -> CreateUserResponse:
        """Создать пользователя (низкоуровневый метод).

        Args:
            request: Запрос на создание пользователя.

        Returns:
            Ответ с данными созданного пользователя.
        """
        return self.stub.CreateUser(request)

    def get_user(self, user_id: str) -> GetUserResponse:
        """Получить пользователя по ID.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Ответ с данными пользователя.
        """
        request = GetUserRequest(id=user_id)
        return self.get_user_api(request)

    def create_user(self) -> CreateUserResponse:
        """Создать нового пользователя с фейковыми данными.

        Returns:
            Ответ с данными созданного пользователя.
        """
        request = CreateUserRequest(
            email=faker_ru.email(),
            last_name=faker_ru.last_name(),
            first_name=faker_ru.first_name(),
            middle_name=faker_ru.middle_name(),
            phone_number=faker_ru.phone_number()
        )
        return self.create_user_api(request)

def build_users_gateway_grpc_client() -> UserGatewayGRPCClient:
    """Создать gRPC клиент для Users Gateway.

    Returns:
        Настроенный экземпляр UserGatewayGRPCClient.
    """
    return UserGatewayGRPCClient(channel=build_gateway_grpc_client())

def build_users_gateway_locust_grpc_client(environment: Environment) -> UserGatewayGRPCClient:
    """Создать gRPC клиент с интеграцией Locust для Users Gateway.

    Args:
        environment: Экземпляр окружения Locust.

    Returns:
        Настроенный экземпляр UserGatewayGRPCClient с интерцептором.
    """
    return UserGatewayGRPCClient(channel=build_gateway_locust_grpc_client(environment))