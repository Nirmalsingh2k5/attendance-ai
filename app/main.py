from .config import settings
from .models.db import database_runtime
from .routes.system_routes import system_blueprint
from .utils.logging_config import configure_logging, get_logger

configure_logging(settings)
logger = get_logger(__name__)

database_runtime.initialize()

from .legacy_app import app as flask_app  # noqa: E402

flask_app.register_blueprint(system_blueprint)
flask_app.config["SQLALCHEMY_DATABASE_URI"] = settings.resolved_database_url
flask_app.config["ATTENDANCE_PROJECT_ROOT"] = str(settings.project_root)

logger.info("Application bootstrapped with package-based runtime.")


def create_app():
    return flask_app


app = create_app()
