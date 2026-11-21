from typing import Any

from technical_support_agent.docker_reader import ReadOnlyDocker


def _raw(
    name: str,
    *,
    labeled: bool = True,
    oom: bool = False,
    exit_code: int = 0,
) -> dict[str, Any]:
    labels = {"tsa.managed": "true"} if labeled else {}
    return {
        "Id": f"id-{name}",
        "Name": f"/{name}",
        "RestartCount": 0,
        "Config": {
            "Image": "nginx:alpine",
            "Labels": labels,
            "Env": ["POSTGRES_PASSWORD=super-secret"],
        },
        "State": {
            "Status": "exited",
            "Running": False,
            "ExitCode": exit_code,
            "OOMKilled": oom,
            "StartedAt": "2026-11-21T00:00:00Z",
            "FinishedAt": "2026-11-21T00:10:00Z",
        },
    }


class FakeApi:
    """Fake client with read methods only: any write attempt raises AttributeError."""

    def __init__(self, items: list[dict[str, Any]]) -> None:
        self._items = {item["Id"]: item for item in items}
        self.calls: list[str] = []

    def containers(self, *, all: bool, filters: dict[str, Any]) -> list[dict[str, Any]]:
        self.calls.append("containers")
        return [{"Id": key} for key in self._items]

    def inspect_container(self, container: str) -> dict[str, Any]:
        self.calls.append("inspect_container")
        return self._items[container]


def test_maps_state_fields() -> None:
    reader = ReadOnlyDocker(FakeApi([_raw("web", oom=True, exit_code=137)]))
    (info,) = reader.list_managed()
    assert info.name == "web"
    assert info.exit_code == 137
    assert info.oom_killed is True
    assert info.finished_at == "2026-11-21T00:10:00Z"


def test_skips_unlabeled_even_if_api_returns_it() -> None:
    api = FakeApi([_raw("web"), _raw("stray", labeled=False)])
    names = [c.name for c in ReadOnlyDocker(api).list_managed()]
    assert names == ["web"]


def test_does_not_leak_environment() -> None:
    (info,) = ReadOnlyDocker(FakeApi([_raw("db")])).list_managed()
    assert "super-secret" not in repr(info)


def test_only_uses_read_calls() -> None:
    api = FakeApi([_raw("web")])
    ReadOnlyDocker(api).list_managed()
    assert set(api.calls) <= {"containers", "inspect_container"}
