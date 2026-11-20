# ADR-001: Run Ollama inside WSL2 and baseline results

Status: Accepted
Date: 2026-11-20

## Context

The agent needs a local LLM. The development laptop has an Intel i5-6300U
(2 cores, 4 threads), 16 GB RAM installed (15.4 GB usable), and no GPU
usable by Ollama. WSL2 runs with the default limits: 7.5 GiB RAM, 4 threads,
2 GiB swap. Two Ollama installs existed (WSL and Windows); the Windows one
was stopped.

## Measurements

Model: llama3.1:8b (default tag), CPU only, WSL2, Ollama 0.32.5.
Prompt: 28 tokens, short answer.

| Run  | Total   | Load    | Prompt eval | Eval (decode) |
|------|---------|---------|-------------|---------------|
| Cold | 54.6 s  | 22.0 s  | 6.35 tok/s  | 3.23 tok/s    |
| Warm | 27.8 s  | 0.4 s   | 88.0 tok/s  | 3.14 tok/s    |

While the model is loaded: 6.2 GiB used, 1.3 GiB available of 7.5 GiB.
`ollama ps` reports 5.6 GB, context 4096, 100% CPU.

## Decision

Run Ollama as a systemd service inside WSL2. The agent calls
http://localhost:11434. The Windows Ollama install is not used.

## Alternatives rejected

- Ollama on Windows: no GPU benefit on this hardware, and a second model
  store would duplicate disk usage.
- llama3.1:8b as a fixed choice: decided later by phase 11 benchmarks.
- qwen2.5:32b: 19 GB, does not fit in 7.5 GiB.

## Consequences

- Decode speed is about 3.2 tok/s, so a 150-token answer takes about 47 s.
  The draft target of 60 s for diagnosis plus LLM is at risk.
- A loaded 8B model leaves about 1.3 GiB of RAM for the rest of the stack.
- Deterministic rules must handle detection and decisions; the LLM only
  explains, off the critical path.
- Smaller models (3-4B class) must be benchmarked in phase 11, with exact
  tags verified at pull time.
