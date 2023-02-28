import grpc
import pytest
import pytest_asyncio

from playlist.config import Settings
from playlist.adapters.grpc.generated.playlist_pb2_grpc import PlayListStub
from playlist.adapters.grpc.generated.song_pb2_grpc import SongStub
from playlist.adapters.grpc.generated.control_pb2_grpc import (
    PlaylistControlStub,
)


@pytest_asyncio.fixture(scope="module")
async def channel(settings: Settings) -> grpc.Channel:
    channel = grpc.aio.insecure_channel(settings.grpc.socket)
    yield channel
    await channel.close(0)


@pytest.fixture(scope="module")
def playlist_stub(channel: grpc.Channel) -> PlayListStub:
    return PlayListStub(channel)


@pytest.fixture(scope="module")
def song_stub(channel: grpc.Channel) -> SongStub:
    return SongStub(channel)


@pytest.fixture(scope="module")
def control_stub(channel: grpc.Channel) -> PlaylistControlStub:
    return PlaylistControlStub(channel)
