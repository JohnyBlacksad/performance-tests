from clients.grpc.client import GRPCClient, build_gateway_grpc_client, build_gateway_locust_grpc_client
from locust.env import Environment
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub
from contracts.services.gateway.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from grpc import Channel
from tools.fakers import faker_ru

class UserGatewayGRPCClient(GRPCClient):
    def __init__(self, channel: Channel) -> None:
        super().__init__(channel)

        self.stub = UsersGatewayServiceStub(channel)

    def get_user_api(self, request: GetUserRequest) -> GetUserResponse:
        return self.stub.GetUser(request)

    def create_user_api(self, request: CreateUserRequest) -> CreateUserResponse:
        return self.stub.CreateUser(request)

    def get_user(self, user_id: str) -> GetUserResponse:
        request = GetUserRequest(id=user_id)
        return self.get_user_api(request)

    def create_user(self) -> CreateUserResponse:
        request = CreateUserRequest(
            email=faker_ru.email(),
            last_name=faker_ru.last_name(),
            first_name=faker_ru.first_name(),
            middle_name=faker_ru.middle_name(),
            phone_number=faker_ru.phone_number()
        )
        return self.create_user_api(request)

def build_users_gateway_grpc_client() -> UserGatewayGRPCClient:
    return UserGatewayGRPCClient(channel=build_gateway_grpc_client())

def build_users_gateway_locust_grpc_client(environment: Environment) -> UserGatewayGRPCClient:
    return UserGatewayGRPCClient(channel=build_gateway_locust_grpc_client(environment))