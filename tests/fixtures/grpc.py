import grpc
import pytest
import pytest_asyncio

from playlist.config import Settings
from playlist.adapters.grpc.generated.playlist_pb2_grpc import PlayListStub


@pytest_asyncio.fixture(scope="module")
async def playlist_channel(settings: Settings) -> grpc.Channel:
    channel = grpc.aio.insecure_channel(settings.grpc.socket)
    yield channel
    await channel.close(0)


@pytest.fixture(scope="module")
def playlist_stub(playlist_channel: grpc.Channel) -> PlayListStub:
    return PlayListStub(playlist_channel)
