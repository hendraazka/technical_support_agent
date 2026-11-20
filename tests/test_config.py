import pytest

from technical_support_agent.config import Settings


def test_settings_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TSA_LOG_LEVEL", raising=False)
    assert Settings().log_level == "INFO"


def test_settings_read_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TSA_LOG_LEVEL", "DEBUG")
    assert Settings().log_level == "DEBUG"
