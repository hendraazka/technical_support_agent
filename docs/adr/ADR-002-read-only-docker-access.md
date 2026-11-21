# ADR-002: Read-only Docker access through docker-socket-proxy

Status: Accepted
Date: 2026-11-21

## Context

The agent must observe container state. Access to docker.sock is equivalent
to root on the host, and mounting it with the :ro flag does not restrict the
Docker API, only the socket file. A previous prototype mounted the socket
directly into the agent container.

## Decision

- The agent reaches Docker only through tecnativa/docker-socket-proxy, pinned
  by image digest, with CONTAINERS=1 and POST=0, published on 127.0.0.1:12375.
- Managed containers carry the label tsa.managed=true. The proxy itself is not
  labeled, so the agent never manages its own guard.
- Agent code uses ReadOnlyDocker, which exposes only list and inspect, filters
  by label twice (query filter and re-check on the inspected object), and maps
  a fixed set of fields. Environment variables are never mapped.

## Evidence (tested on 2026-11-21)

| Check                                        | Result                    |
|----------------------------------------------|---------------------------|
| GET /_ping                                   | OK                        |
| List with label filter, all=true             | 4 managed, stray excluded |
| POST /containers/stray/restart               | 403, uptime unchanged     |
| GET /images/json                             | 403                       |
| Unit tests with a fake client (8 total)      | pass                      |
| Run against the real lab                     | 4 containers, no env data |

## Known limits (measured, not assumed)

- The proxy filters by method and path, not by container. GET inspect returns
  full environment variables (POSTGRES_PASSWORD present in the lab database).
- GET /containers/{id}/archive returned 200: files can be read from any container.
- GET /containers/{id}/attach/ws with stdin=1 returned 101: the proxy forwards the
  WebSocket upgrade. Whether input reaches a process was not tested (no bytes sent).
- Only managed containers are returned by the agent because of agent code,
  not because of the proxy.

## Consequences and mitigations

- The port is bound to loopback and the only client is the agent.
- ReadOnlyDocker has no write methods; a unit test asserts only read calls are used
  and another asserts environment data does not leak into ContainerInfo.
- Phase 6: the Tool Gateway re-checks the label immediately before any write action.
- Phase 10: restrict /containers/ sub-paths (attach, archive, exec) with custom
  proxy rules or an internal-only network. Exact configuration to be verified
  against the proxy documentation.
- finished_at equal to 0001-01-01 means unknown. Down time is the poller's own
  observation (detected_at); finished_at is supporting evidence only.

## Alternatives rejected

- Mounting docker.sock directly into the agent.
- Mounting the socket with :ro, which does not limit the API.
- Reading raw container attributes everywhere; it leaks environment data.
