"""Structured logging with ISO 8601 UTC timestamps."""

import logging
import sys

import structlog
from structlog.typing import Processor

from technical_support_agent.config import Settings


def configure_logging(settings: Settings) -> None:
    """Configure structlog. Every event carries a UTC timestamp."""
    shared: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]
    renderer: Processor = (
        structlog.processors.JSONRenderer()
        if settings.log_json
        else structlog.dev.ConsoleRenderer()
    )
    level = logging.getLevelNamesMapping()[settings.log_level]
    structlog.configure(
        processors=[*shared, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,
    )
