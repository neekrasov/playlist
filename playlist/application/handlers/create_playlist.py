from dataclasses import dataclass

from common.handler import Handler
from playlist.domain.entities import PlaylistID
from ..protocols.playlist_repo import PlaylistRepository


@dataclass
class CreatePlaylistCommand:
    title: str


class CreatePlaylistHandler(Handler[CreatePlaylistCommand, PlaylistID]):
    def __init__(self, playlist_repo: PlaylistRepository):
        self.playlist_repo = playlist_repo

    async def execute(self, command: CreatePlaylistCommand) -> PlaylistID:
        playlist_id = await self.playlist_repo.create_playlist(command.title)
        return playlist_id
