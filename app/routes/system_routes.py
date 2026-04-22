from flask import Blueprint, jsonify

from ..config import settings
from ..models.db import database_runtime
from ..utils.background_jobs import background_jobs
from ..utils.cache import face_cache_backend

system_blueprint = Blueprint("system", __name__, url_prefix="/api/system")


@system_blueprint.get("/health")
def system_health():
    return jsonify(
        {
            "success": True,
            "status": "ok",
            "database": database_runtime.healthcheck(),
            "cache": face_cache_backend.describe(),
            "background_jobs": background_jobs.describe(),
        }
    )


@system_blueprint.get("/runtime")
def runtime_info():
    return jsonify(
        {
            "success": True,
            "database_url": settings.resolved_database_url.split("://", 1)[0],
            "redis_enabled": bool(settings.redis_url),
            "celery_configured": bool(settings.celery_broker_url),
            "logs_dir": str(settings.logs_dir),
        }
    )
