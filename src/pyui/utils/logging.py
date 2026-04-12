"""
Structured logging for PyUI.

In development mode (``PYUI_ENV=development`` or default), output is
pretty-printed with colours using Rich. In production (``PYUI_ENV=production``)
it emits JSON lines for structured log aggregators.

Usage::

    from pyui.utils.logging import get_logger

    log = get_logger(__name__)
    log.info("Server started", port=8000)
    log.debug("IR compiled", nodes=42)
    log.warning("Missing alt text", component="image")
    log.error("Compiler failed", error=str(exc))
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Any

import structlog


def _is_dev() -> bool:
    env = os.environ.get("PYUI_ENV", "development").lower()
    return env == "development"


def configure_logging(level: str = "INFO") -> None:
    """
    Configure structlog for the requested level and environment.

    Call once at application startup (the CLI entry point calls this).
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if _is_dev():
        # Pretty, coloured console output
        processors: list[structlog.types.Processor] = [
            *shared_processors,
            structlog.dev.ConsoleRenderer(),
        ]
    else:
        # JSON lines for production / CI
        processors = [
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> Any:
    """Return a bound structlog logger for *name*."""
    return structlog.get_logger(name)
