from dataclasses import dataclass

from common.handler import Handler
from playlist.domain.entities import PlaylistID
from ..protocols.playlist_repo import PlaylistRepository


@dataclass
class DeletePlaylistCommand:
    playlist_id: PlaylistID


class DeletePlaylistHandler(Handler[DeletePlaylistCommand, None]):
    def __init__(self, playlist_repo: PlaylistRepository):
        self.playlist_repo = playlist_repo

    async def execute(self, command: DeletePlaylistCommand) -> None:
        await self.playlist_repo.delete_playlist(command.playlist_id)
