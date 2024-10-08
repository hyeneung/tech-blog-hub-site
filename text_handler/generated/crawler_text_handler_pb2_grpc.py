# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

# from generated import crawler_text_handler_pb2
from generated import crawler_text_handler_pb2 as crawler__text__handler__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in crawler_text_handler_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class CrawlerTextHandlerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StreamUrlSummaries = channel.stream_stream(
                '/CrawlerTextHandler/StreamUrlSummaries',
                request_serializer=crawler__text__handler__pb2.UrlRequest.SerializeToString,
                response_deserializer=crawler__text__handler__pb2.SummarizedDataResponse.FromString,
                _registered_method=True)


class CrawlerTextHandlerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def StreamUrlSummaries(self, request_iterator, context):
        """Bidirectional streaming where Crawler sends URLs and receives summarized data in response
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CrawlerTextHandlerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StreamUrlSummaries': grpc.stream_stream_rpc_method_handler(
                    servicer.StreamUrlSummaries,
                    request_deserializer=crawler__text__handler__pb2.UrlRequest.FromString,
                    response_serializer=crawler__text__handler__pb2.SummarizedDataResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'CrawlerTextHandler', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('CrawlerTextHandler', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class CrawlerTextHandler(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def StreamUrlSummaries(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/CrawlerTextHandler/StreamUrlSummaries',
            crawler__text__handler__pb2.UrlRequest.SerializeToString,
            crawler__text__handler__pb2.SummarizedDataResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
