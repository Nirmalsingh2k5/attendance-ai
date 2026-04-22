from ..utils.background_jobs import background_jobs
from ..utils.logging_config import get_logger

logger = get_logger(__name__)


def queue_cache_refresh(refresh_callable, *args, **kwargs):
    logger.info("Queueing face cache refresh job.")
    return background_jobs.submit(refresh_callable, *args, **kwargs)
