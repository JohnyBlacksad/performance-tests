from httpx import Response, Client, QueryParams

def build_gateway_http_client() -> Client:
    return Client(base_url='http://localhost:8003/api/v1/', timeout=100)