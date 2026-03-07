from locust import TaskSet, SequentialTaskSet
from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient, build_accounts_locust_gateway_http_client
from clients.http.gateway.cards.client import CardsGatewayHTTPClient, build_cards_locust_gateway_http_client
from clients.http.gateway.documents.client import DocumentsGatewayHTTPClient, build_documents_locust_gateway_http_client
from clients.http.gateway.operations.client import OperationsGatewayHTTPClient, build_operations_locust_gateway_http_client
from clients.http.gateway.users.client import UserGatewayHTTPClient, build_users_locust_gateway_http_client

class GatewayHTTPTaskSet(TaskSet):
    user_client: UserGatewayHTTPClient
    cards_client: CardsGatewayHTTPClient
    accounts_client: AccountsGatewayHTTPClient
    documents_client: DocumentsGatewayHTTPClient
    operations_client: OperationsGatewayHTTPClient

    def on_start(self) -> None:
        self.user_client = build_users_locust_gateway_http_client(self.user.environment)
        self.cards_client = build_cards_locust_gateway_http_client(self.user.environment)
        self.accounts_client = build_accounts_locust_gateway_http_client(self.user.environment)
        self.documents_client = build_documents_locust_gateway_http_client(self.user.environment)
        self.operations_client = build_operations_locust_gateway_http_client(self.user.environment)


class GatewayHTTPSequentialTaskSet(SequentialTaskSet):
    user_client: UserGatewayHTTPClient
    cards_client: CardsGatewayHTTPClient
    accounts_client: AccountsGatewayHTTPClient
    documents_client: DocumentsGatewayHTTPClient
    operations_client: OperationsGatewayHTTPClient

    def on_start(self) -> None:
        self.user_client = build_users_locust_gateway_http_client(self.user.environment)
        self.cards_client = build_cards_locust_gateway_http_client(self.user.environment)
        self.accounts_client = build_accounts_locust_gateway_http_client(self.user.environment)
        self.documents_client = build_documents_locust_gateway_http_client(self.user.environment)
        self.operations_client = build_operations_locust_gateway_http_client(self.user.environment)


