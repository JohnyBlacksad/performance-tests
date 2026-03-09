from pydantic import BaseModel

class GRPCClientConfig(BaseModel):
    host: str
    port: int

    @property
    def client_url(self):
        return f'{self.host}:{self.port}'