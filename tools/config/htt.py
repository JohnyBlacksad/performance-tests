from pydantic import BaseModel, HttpUrl

class HTTPClientConfig(BaseModel):
    url: HttpUrl
    api_version: int
    timeout: float = 100.0

    @property
    def client_url(self) -> str:
        return f'{str(self.url)}/api/v{self.api_version}/'
