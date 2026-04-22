from dataclasses import dataclass
import os
from pathlib import Path

from .utils.env import load_env_file


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_env_file(PROJECT_ROOT / ".env")


def _resolve_storage_root() -> Path:
    explicit_root = os.getenv("ATTENDANCE_STORAGE_ROOT", "").strip()
    render_disk_root = os.getenv("RENDER_DISK_PATH", "").strip()
    selected_root = explicit_root or render_disk_root
    if not selected_root:
        return PROJECT_ROOT

    candidate = Path(selected_root)
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    return candidate.resolve()


STORAGE_ROOT = _resolve_storage_root()


@dataclass(frozen=True)
class AppConfig:
    project_root: Path = PROJECT_ROOT
    storage_root: Path = STORAGE_ROOT
    database_dir: Path = STORAGE_ROOT / "database"
    sqlite_database_path: Path = STORAGE_ROOT / "database" / "teachers.db"
    photos_dir: Path = STORAGE_ROOT / "photos"
    embeddings_file: Path = STORAGE_ROOT / "embeddings.pkl"
    attendance_dir: Path = STORAGE_ROOT / "attendance"
    temp_dir: Path = STORAGE_ROOT / "temp"
    templates_dir: Path = PROJECT_ROOT / "templates"
    static_dir: Path = PROJECT_ROOT / "static"
    logs_dir: Path = STORAGE_ROOT / "logs"
    secret_key: str = os.getenv("ATTENDANCE_SECRET_KEY", "attendance_by_ai_secret")
    session_cookie_secure: bool = os.getenv("SESSION_COOKIE_SECURE", "0").strip() == "1"
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_file_name: str = os.getenv("LOG_FILE_NAME", "attendance.log")
    database_url: str = os.getenv("DATABASE_URL", "").strip()
    redis_url: str = os.getenv("REDIS_URL", "").strip()
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "").strip()

    @property
    def resolved_database_url(self):
        if self.database_url:
            if self.database_url.startswith("postgres://"):
                return "postgresql://" + self.database_url[len("postgres://") :]
            return self.database_url
        return f"sqlite:///{self.sqlite_database_path.as_posix()}"

    @property
    def log_file_path(self):
        return self.logs_dir / self.log_file_name


settings = AppConfig()
