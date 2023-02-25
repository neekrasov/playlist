import os
from dataclasses import dataclass, field


@dataclass
class PGSettings:
    user: str = field(init=False)
    password: str = field(init=False)
    host: str = field(init=False)
    db: str = field(init=False)
    port: str = field(init=False)
    url: str = field(init=False)

    def __post_init__(self):
        self._read_env()

    def _read_env(self):
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.host = os.getenv("POSTGRES_HOST")
        self.db = os.getenv("POSTGRES_DB")
        self.port = os.getenv("POSTGRES_PORT")
        self.url = (
            "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                db=self.db,
            )
        )


@dataclass
class Settings:
    postgres: PGSettings = field(
        init=False, default_factory=PGSettings
    )
