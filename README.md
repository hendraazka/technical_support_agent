# technical-support-agent

An agentic technical support agent for a personal homelab. It watches
labeled containers, diagnoses failures with evidence, asks a human for
approval, applies safe remediation, and verifies the result.

This is a learning and portfolio project, built phase by phase.

## Status

Phase 2 of 15 is complete. The agent can list labeled lab containers
through a socket proxy that denies write requests. There is still no
detection loop, diagnosis, or remediation.

- Phase 1: project skeleton, quality gate, settings, structured UTC logging,
  pre-commit, local LLM baseline ([ADR-001](docs/adr/ADR-001-ollama-location-and-baseline.md)).
- Phase 2: lab targets and read-only Docker access
  ([ADR-002](docs/adr/ADR-002-read-only-docker-access.md)). The proxy denies POST
  requests but does not block every read; the measured limits are in the ADR.

Next: phase 3, health monitoring.

## Design principles

These principles guide the design; most are implemented in later phases.

- The LLM proposes, it never executes. It can only suggest an `action_id`
  from a fixed catalog; a policy engine decides.
- Deterministic rules come first. The LLM explains and ranks, off the
  critical path.
- Human approval is the default for any remediation.
- Every action is recorded with a UTC timestamp.

The target architecture is in
[docs/flow/00-system-overview.md](docs/flow/00-system-overview.md).

## Quick start

Requires Python 3.12, [uv](https://docs.astral.sh/uv/), make and Docker.

    git clone https://github.com/hendraazka/technical_support_agent.git
    cd technical_support_agent
    uv sync
    uv run pre-commit install
    make check

Run the lab and list its labeled containers:

    cp lab/.env.example lab/.env    # then set LAB_DB_PASSWORD to a password you choose
    docker compose -f infra/compose.yaml up -d
    docker compose -f lab/compose.yaml up -d
    uv run python -m technical_support_agent.cli

## Repository layout

- `src/technical_support_agent/`: application code
- `tests/`: pytest suite
- `lab/`: target containers (labeled `tsa.managed=true`, plus one unlabeled)
- `infra/`: read-only docker-socket-proxy
- `docs/adr/`: architecture decision records
- `docs/flow/`: flow diagrams (Mermaid, rendered by GitHub)

## License

See [LICENSE](LICENSE).
