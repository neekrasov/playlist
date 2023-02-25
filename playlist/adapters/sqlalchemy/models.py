import uuid
from decimal import Decimal
from datetime import datetime
from typing_extensions import Annotated
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, registry
from sqlalchemy import UUID, TIMESTAMP
from sqlalchemy import ForeignKey

from playlist.domain.entities import (
    Playlist as PlaylistEntity,
    Song as SongEntity,
)

uuidpk = Annotated[
    uuid.UUID,
    UUID(as_uuid=True),
    mapped_column(primary_key=True, default=uuid.uuid4, unique=True),
]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            datetime: TIMESTAMP(timezone=True),
            uuid.UUID: UUID(as_uuid=True),
        }
    )
    id: Mapped[uuidpk]


class Song(Base):
    __tablename__ = "songs"

    title: Mapped[str] = mapped_column()
    duration: Mapped[Decimal] = mapped_column()
    playlist_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("playlists.id", ondelete="CASCADE"),
    )
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Playlist(Base):
    __tablename__ = "playlists"

    title: Mapped[str] = mapped_column()


def start_mapping():
    mapper_registry = Base.registry
    mapper_registry.map_imperatively(SongEntity, Song.__table__)
    mapper_registry.map_imperatively(
        PlaylistEntity,
        Playlist.__table__,
    )
