from common.exception import DomainException


class PlaylistException(DomainException):
    """Rise in playlist context"""


class NotFoundException(PlaylistException):
    """Common exception for some not found"""


class PlaylistNotFoundException(NotFoundException):
    """Playlist not found"""

    def __init__(self, playlist_id):
        super(PlaylistNotFoundException, self).__init__(
            "Playlist with id '{}' not found".format(playlist_id)
        )


class SongNotFoundException(NotFoundException):
    """Song not found"""

    def __init__(self, song_id):
        super(SongNotFoundException, self).__init__(
            "Song with id '{}' not found".format(song_id)
        )
