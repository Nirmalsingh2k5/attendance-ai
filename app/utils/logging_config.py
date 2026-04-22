import logging
from logging.handlers import RotatingFileHandler


def configure_logging(settings):
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return root_logger

    log_level = getattr(logging, settings.log_level, logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)

    try:
        settings.logs_dir.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            settings.log_file_path,
            maxBytes=2 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except OSError:
        root_logger.warning("File logging could not be enabled; continuing with console logging only.")
    return root_logger


def get_logger(name):
    return logging.getLogger(name)
