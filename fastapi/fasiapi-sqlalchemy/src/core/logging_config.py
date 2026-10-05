import logging.config
import os
from pathlib import Path

LOG_LEVEL = "INFO"
LOG_FORMAT = "text"         # text | json
LOG_FILE = "/home/blacky/working/github-workspace/python-webframework/fastapi/fasiapi-sqlalchemy/logs/app.log"                     # e.g. /var/log/app/worker.log


def _build_config() -> dict:
    handlers = {"console": {"class": "logging.StreamHandler", "formatter": LOG_FORMAT}}
    active = ["console"]

    if LOG_FILE:
        Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
        handlers["file"] = {
            "class": "logging.handlers.WatchedFileHandler",  # cooperates with logrotate
            "filename": LOG_FILE,
            "formatter": LOG_FORMAT,
        }
        active.append("file")

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "text": {"format": "%(asctime)s | %(levelname)s | %(processName)s | %(name)s | %(message)s"},
            "json": {
                "()": "pythonjsonlogger.json.JsonFormatter",
                "format": "%(asctime)s %(levelname)s %(processName)s %(name)s %(message)s",
            },
        },
        "handlers": handlers,
        "root": {"level": LOG_LEVEL, "handlers": active},
        "loggers": {
            "celery": {"level": LOG_LEVEL},
            "uvicorn.access": {"level": "INFO"},
        },
    }


def app_setup_logging():
    logging.config.dictConfig(_build_config())