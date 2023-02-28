# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import control_pb2 as control__pb2


class PlaylistControlStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PlaySong = channel.unary_unary(
            "/PlaylistControl/PlaySong",
            request_serializer=control__pb2.PlaySongRequest.SerializeToString,
            response_deserializer=control__pb2.PlaySongResponse.FromString,
        )
        self.PauseSong = channel.unary_unary(
            "/PlaylistControl/PauseSong",
            request_serializer=control__pb2.PauseSongRequest.SerializeToString,
            response_deserializer=control__pb2.PauseSongResponse.FromString,
        )
        self.NextSong = channel.unary_unary(
            "/PlaylistControl/NextSong",
            request_serializer=control__pb2.NextSongRequest.SerializeToString,
            response_deserializer=control__pb2.NextSongResponse.FromString,
        )
        self.PrevSong = channel.unary_unary(
            "/PlaylistControl/PrevSong",
            request_serializer=control__pb2.PrevSongRequest.SerializeToString,
            response_deserializer=control__pb2.PrevSongResponse.FromString,
        )


class PlaylistControlServicer(object):
    """Missing associated documentation comment in .proto file."""

    def PlaySong(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def PauseSong(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def NextSong(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def PrevSong(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_PlaylistControlServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "PlaySong": grpc.unary_unary_rpc_method_handler(
            servicer.PlaySong,
            request_deserializer=control__pb2.PlaySongRequest.FromString,
            response_serializer=control__pb2.PlaySongResponse.SerializeToString,
        ),
        "PauseSong": grpc.unary_unary_rpc_method_handler(
            servicer.PauseSong,
            request_deserializer=control__pb2.PauseSongRequest.FromString,
            response_serializer=control__pb2.PauseSongResponse.SerializeToString,
        ),
        "NextSong": grpc.unary_unary_rpc_method_handler(
            servicer.NextSong,
            request_deserializer=control__pb2.NextSongRequest.FromString,
            response_serializer=control__pb2.NextSongResponse.SerializeToString,
        ),
        "PrevSong": grpc.unary_unary_rpc_method_handler(
            servicer.PrevSong,
            request_deserializer=control__pb2.PrevSongRequest.FromString,
            response_serializer=control__pb2.PrevSongResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "PlaylistControl", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class PlaylistControl(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def PlaySong(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/PlaylistControl/PlaySong",
            control__pb2.PlaySongRequest.SerializeToString,
            control__pb2.PlaySongResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def PauseSong(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/PlaylistControl/PauseSong",
            control__pb2.PauseSongRequest.SerializeToString,
            control__pb2.PauseSongResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def NextSong(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/PlaylistControl/NextSong",
            control__pb2.NextSongRequest.SerializeToString,
            control__pb2.NextSongResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def PrevSong(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/PlaylistControl/PrevSong",
            control__pb2.PrevSongRequest.SerializeToString,
            control__pb2.PrevSongResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
