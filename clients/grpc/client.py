from grpc import Channel, insecure_channel
import grpc.experimental.gevent as grpc_gevent

grpc_gevent.init_gevent()

class GRPCClient:
    def __init__(self, channel: Channel) -> None:
        self.channel = channel


def build_gateway_grpc_client() -> Channel:
    return insecure_channel('localhost:9003')