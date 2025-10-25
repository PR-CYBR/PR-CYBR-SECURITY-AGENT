"""Logging configuration utilities for the PR-CYBR security agent."""

from __future__ import annotations

import json
import logging
import logging.config
import os
from datetime import datetime, timezone
from typing import Any, Dict


_CONFIGURED = False


class JsonFormatter(logging.Formatter):
    """Simple JSON formatter for structured logging output.

    The formatter emits log records as JSON objects, preserving any custom
    attributes passed via ``extra``. This avoids adding third-party
    dependencies while still producing machine-parseable logs that integrate
    with the existing logging configuration entry point.
    """

    _RESERVED = {
        "name",
        "msg",
        "args",
        "levelname",
        "levelno",
        "pathname",
        "filename",
        "module",
        "exc_info",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "msecs",
        "relativeCreated",
        "thread",
        "threadName",
        "processName",
        "process",
        "message",
    }

    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        extra = {
            key: value
            for key, value in record.__dict__.items()
            if key not in self._RESERVED
        }

        if extra:
            payload.update(extra)

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info:
            payload["stack_info"] = self.formatStack(record.stack_info)

        return json.dumps(payload, default=str)


def configure_logging(level: str | int | None = None) -> None:
    """Configure structured logging for the application.

    The configuration is applied at most once per interpreter session.
    Subsequent calls become no-ops to avoid interfering with consumer-defined
    logging settings.
    """

    global _CONFIGURED

    if _CONFIGURED:
        return

    log_level = level or os.getenv("LOG_LEVEL", "INFO")

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": JsonFormatter,
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "level": log_level,
                }
            },
            "root": {
                "handlers": ["console"],
                "level": log_level,
            },
        }
    )

    _CONFIGURED = True


# Configure logging immediately when the module is imported so that all
# consumers benefit from structured output without additional boilerplate.
configure_logging()
