from httpx import Response
from clients.http.base_client import BaseHTTPClient
from clients.http.gateway.gateway_client import build_gateway_http_client

class DocumentsGatewayHTTPClient(BaseHTTPClient):
    """HTTP-клиент для Documents Gateway API."""

    def get_tariff_document_api(self, account_id: str) -> Response:
        """Получить тарифный документ по счёту.

        Args:
            account_id: Уникальный идентификатор счёта.

        Returns:
            HTTP-ответ с тарифным документом.
        """
        return self.get(f'documents/tariff-document/{account_id}')

    def get_contract_document_api(self, account_id: str) -> Response:
        """Получить договор по счёту.

        Args:
            account_id: Уникальный идентификатор счёта.

        Returns:
            HTTP-ответ с договором.
        """
        return self.get(f'documents/contract-document/{account_id}')

def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """Создать HTTP-клиент для Documents Gateway API.

    Returns:
        Настроенный экземпляр DocumentsGatewayHTTPClient.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())