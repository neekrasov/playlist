from typing import Dict

from playlist.domain.entities import PlaylistID, Playlist
from playlist.domain.exceptions import PlaylistNotFoundException
from playlist.application.protocols import PlaylistReader


class InMemoryPlaylistReader(PlaylistReader):
    def __init__(self, playlists: Dict[PlaylistID, Playlist]):
        self.playlists = playlists

    async def get_playlist(self, playlist_id: PlaylistID) -> Playlist:
        playlist = self.playlists.get(playlist_id)
        if playlist is None:
            raise PlaylistNotFoundException(playlist_id)
        return playlist
