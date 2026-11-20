import pytest

from technical_support_agent import main


def test_main_prints_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    captured = capsys.readouterr()
    assert "technical-support-agent" in captured.out
