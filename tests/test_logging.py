import json

import pytest
import structlog

from technical_support_agent.config import Settings
from technical_support_agent.logging_config import configure_logging


def test_json_log_has_utc_timestamp(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(Settings(log_json=True, log_level="INFO"))
    structlog.get_logger().info("service_down", container="web")
    event = json.loads(capsys.readouterr().out.strip())
    assert event["event"] == "service_down"
    assert event["container"] == "web"
    assert event["timestamp"].endswith("Z")
