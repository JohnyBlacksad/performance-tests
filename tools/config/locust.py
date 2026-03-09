from pydantic import BaseModel

class LocustUserConfig(BaseModel):
    min_wait: float = 1
    max_wait: float = 3