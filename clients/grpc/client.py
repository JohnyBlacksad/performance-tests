from locust.env import Environment
from grpc import Channel, insecure_channel, intercept_channel
from clients.grpc.interceptors.locust_interceptor import LocustInterceptor
import grpc.experimental.gevent as grpc_gevent

grpc_gevent.init_gevent()

class GRPCClient:
    def __init__(self, channel: Channel) -> None:
        self.channel = channel


def build_gateway_grpc_client() -> Channel:
    return insecure_channel('localhost:9003')


def build_gateway_locust_grpc_client(environment: Environment) -> Channel:
    locust_interceptor = LocustInterceptor(environment=environment)
    channel = insecure_channel('localhost:9003')
    return intercept_channel(channel, locust_interceptor)

