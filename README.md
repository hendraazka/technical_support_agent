# technical-support-agent

An agentic technical support agent for a personal homelab. It watches
labeled containers, diagnoses failures with evidence, asks a human for
approval, applies safe remediation, and verifies the result.

This is a learning and portfolio project, built phase by phase.

## Status

Phase 1 of 15 (foundation) is complete. There is no agent logic yet.
Phase 1 delivers the project skeleton, a quality gate (`make check`),
settings and structured UTC logging, pre-commit hooks, and a measured
local LLM baseline ([ADR-001](docs/adr/ADR-001-ollama-location-and-baseline.md)).

Next: phase 2, read-only Docker access to labeled lab containers.

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

Requires Python 3.12, [uv](https://docs.astral.sh/uv/) and make.

    git clone https://github.com/hendraazka/technical_support_agent.git
    cd technical_support_agent
    uv sync
    uv run pre-commit install
    make check

## Repository layout

- `src/technical_support_agent/`: application code
- `tests/`: pytest suite
- `docs/adr/`: architecture decision records
- `docs/flow/`: flow diagrams (Mermaid, rendered by GitHub)

## License

See [LICENSE](LICENSE).
