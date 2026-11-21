"""Read-only view of managed Docker containers, reached through docker-socket-proxy."""

from typing import Any, Protocol

import docker
from pydantic import BaseModel, ConfigDict

from technical_support_agent.config import Settings

LABEL_KEY = "tsa.managed"
MANAGED_LABEL = f"{LABEL_KEY}=true"


class ContainerApi(Protocol):
    """The only two Docker API calls this module may use. Both are read-only."""

    def containers(self, *, all: bool, filters: dict[str, Any]) -> list[dict[str, Any]]: ...

    def inspect_container(self, container: str) -> dict[str, Any]: ...


class ContainerInfo(BaseModel):
    """Safe subset of container state. Environment variables are never included."""

    model_config = ConfigDict(frozen=True)

    name: str
    image: str
    status: str
    running: bool
    exit_code: int
    oom_killed: bool
    started_at: str | None
    finished_at: str | None
    restart_count: int


class ReadOnlyDocker:
    """Lists containers that carry the managed label. It has no write methods."""

    def __init__(self, api: ContainerApi) -> None:
        self._api = api

    def list_managed(self) -> list[ContainerInfo]:
        rows = self._api.containers(all=True, filters={"label": [MANAGED_LABEL]})
        result: list[ContainerInfo] = []
        for row in rows:
            raw = self._api.inspect_container(row["Id"])
            labels = raw["Config"].get("Labels") or {}
            if labels.get(LABEL_KEY) != "true":
                continue  # defense in depth: re-check the label on the inspected object
            result.append(self._to_info(raw))
        return result

    @staticmethod
    def _to_info(raw: dict[str, Any]) -> ContainerInfo:
        state = raw["State"]
        return ContainerInfo(
            name=raw["Name"].lstrip("/"),
            image=raw["Config"]["Image"],
            status=state["Status"],
            running=state["Running"],
            exit_code=state["ExitCode"],
            oom_killed=state["OOMKilled"],
            started_at=state.get("StartedAt"),
            finished_at=state.get("FinishedAt"),
            restart_count=raw["RestartCount"],
        )


def build_reader(settings: Settings) -> ReadOnlyDocker:
    """Create a reader that talks to the Docker API through the socket proxy."""
    return ReadOnlyDocker(docker.APIClient(base_url=settings.docker_host, version="auto"))
