"""Developer entry point: list managed containers once."""

import structlog

from technical_support_agent.config import get_settings
from technical_support_agent.docker_reader import build_reader
from technical_support_agent.logging_config import configure_logging


def list_main() -> None:
    settings = get_settings()
    configure_logging(settings)
    log = structlog.get_logger()
    for info in build_reader(settings).list_managed():
        log.info("container_seen", **info.model_dump())


if __name__ == "__main__":
    list_main()
