from httpx import Response
from base_client import BaseHTTPClient

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