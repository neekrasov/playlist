from common.exception import DomainException
from playlist.constants import SONG_NOT_FOUND, PLAYLIST_NOT_FOUND


class PlaylistException(DomainException):
    """Rise in playlist context"""


class NotFoundException(PlaylistException):
    """Common exception for some not found"""


class PlaylistNotFoundException(NotFoundException):
    """Playlist not found"""

    def __init__(self, playlist_id):
        super(PlaylistNotFoundException, self).__init__(
            PLAYLIST_NOT_FOUND.format(playlist_id)
        )


class SongNotFoundException(NotFoundException):
    """Song not found"""

    def __init__(self, song_id):
        super(SongNotFoundException, self).__init__(
            SONG_NOT_FOUND.format(song_id)
        )
