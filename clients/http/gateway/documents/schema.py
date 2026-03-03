"""Pydantic-модели для валидации данных документов.

Модели описывают структуру JSON-данных для операций с документами:
- Тарифы
- Договоры
"""

from pydantic import BaseModel, HttpUrl


class TariffSchema(BaseModel):
    """Модель тарифа.

    Attributes:
        url: URL документа тарифа.
        document: Содержимое документа.
    """
    url: HttpUrl
    document: str


class GetTariffDocumentResponseSchema(BaseModel):
    """Модель ответа на получение документа тарифа.

    Attributes:
        tariff: Данные тарифа.
    """
    tariff: TariffSchema


class ContractSchema(BaseModel):
    """Модель договора.

    Attributes:
        url: URL документа договора.
        document: Содержимое документа.
    """
    url: HttpUrl
    document: str


class GetContractDocumentResponseSchema(BaseModel):
    """Модель ответа на получение документа договора.

    Attributes:
        contract: Данные договора.
    """
    contract: ContractSchema