from dataclasses import dataclass
import sqlite3

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
except ImportError:  # pragma: no cover - optional during local bootstrap
    create_engine = None
    text = None
    sessionmaker = None

from ..config import settings


@dataclass
class DatabaseRuntime:
    engine = None
    SessionLocal = None

    def initialize(self):
        settings.database_dir.mkdir(parents=True, exist_ok=True)
        if create_engine is None or sessionmaker is None:
            self.engine = None
            self.SessionLocal = None
            return
        self.engine = create_engine(settings.resolved_database_url, future=True, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, future=True)

    def get_session(self):
        if self.SessionLocal is None:
            self.initialize()
        return self.SessionLocal()

    def get_sqlite_connection(self):
        settings.database_dir.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(
            settings.sqlite_database_path,
            timeout=30,
            check_same_thread=False,
        )
        conn.row_factory = sqlite3.Row
        return conn

    def healthcheck(self):
        try:
            if self.engine is None:
                self.initialize()
            if self.engine is None or text is None:
                return {"ok": True, "driver": "sqlite3-legacy", "note": "SQLAlchemy not installed yet"}
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return {"ok": True, "driver": self.engine.url.drivername}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}


database_runtime = DatabaseRuntime()
