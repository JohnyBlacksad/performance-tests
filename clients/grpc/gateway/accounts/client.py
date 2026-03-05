from grpc import Channel

from clients.grpc.client import GRPCClient, build_gateway_grpc_client
from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub
from contracts.services.gateway.accounts.rpc_get_accounts_pb2 import GetAccountsRequest, GetAccountsResponse
from contracts.services.gateway.accounts.rpc_open_credit_card_account_pb2 import OpenCreditCardAccountRequest, OpenCreditCardAccountResponse
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountRequest, OpenDebitCardAccountResponse
from contracts.services.gateway.accounts.rpc_open_deposit_account_pb2 import OpenDepositAccountRequest, OpenDepositAccountResponse
from contracts.services.gateway.accounts.rpc_open_savings_account_pb2 import OpenSavingsAccountRequest, OpenSavingsAccountResponse
from tools.fakers import faker_ru

class AccountsGatewayGRPCClient(GRPCClient):
    def __init__(self, channel: Channel) -> None:
        super().__init__(channel)

        self.stub = AccountsGatewayServiceStub(channel)

    def get_accounts_api(self, request: GetAccountsRequest) -> GetAccountsResponse:
        return self.stub.GetAccounts(request)

    def open_credit_card_account_api(self, request: OpenCreditCardAccountRequest) -> OpenCreditCardAccountResponse:
        return self.stub.OpenCreditCardAccount(request)

    def open_debit_card_account_api(self, request: OpenDebitCardAccountRequest) -> OpenDebitCardAccountResponse:
        return self.stub.OpenDebitCardAccount(request)

    def open_deposit_account_api(self, request: OpenDepositAccountRequest) -> OpenDepositAccountResponse:
        return self.stub.OpenDepositAccount(request)

    def open_saving_account_api(self, request: OpenSavingsAccountRequest) -> OpenSavingsAccountResponse:
        return self.stub.OpenSavingsAccount(request)

    def get_accounts(self, user_id: str) -> GetAccountsResponse:
        request = GetAccountsRequest(user_id=user_id)
        return self.get_accounts_api(request)

    def open_credit_card_account(self, user_id: str) -> OpenCreditCardAccountResponse:
        request = OpenCreditCardAccountRequest(user_id=user_id)
        return self.open_credit_card_account_api(request)

    def open_debit_card_account(self, user_id: str) -> OpenDebitCardAccountResponse:
        request = OpenDebitCardAccountRequest(user_id=user_id)
        return self.open_debit_card_account_api(request)

    def open_deposit_account(self, user_id: str) -> OpenDepositAccountResponse:
        request = OpenDepositAccountRequest(user_id=user_id)
        return self.open_deposit_account_api(request)

    def open_saving_account(self, user_id: str) -> OpenSavingsAccountResponse:
        request = OpenSavingsAccountRequest(user_id=user_id)
        return self.open_saving_account_api(request)

def build_accounts_gateway_client() -> AccountsGatewayGRPCClient:
    return AccountsGatewayGRPCClient(channel=build_gateway_grpc_client())