from collections.abc import Callable
import time
from grpc import _CallFuture, _TRequest, _TResponse, ClientCallDetails, UnaryUnaryClientInterceptor, RpcError
from locust.env import Environment

class LocustInterceptor(UnaryUnaryClientInterceptor):
    def __init__(self, environment: Environment) -> None:
        self.environment = environment
        super().__init__()

    def intercept_unary_unary(self, continuation: Callable[[ClientCallDetails, _TRequest], _CallFuture[_TResponse]], client_call_details: ClientCallDetails, request: _TRequest) -> _CallFuture[_TResponse]:
        response = None
        exception: RpcError | None = None
        start_time = time.perf_counter()
        response_length = 0
        try:
            response = continuation(client_call_details, request)
            response_length = response.result().ByteSize() # type: ignore
        except RpcError as e:
            exception = e

        self.environment.events.request.fire(
            name = client_call_details.method,
            context = None,
            response = response,
            exception = exception,
            request_type = "gRPC",
            response_time = (time.perf_counter() - start_time) * 1000,
            response_length = response_length
        )


        return response # type: ignore