# agent-accountability-lab

> **Digital Twin Environment for Evaluating Accountability, Memory, and Behavioral Drift in Autonomous AI Agents**

[![CI](https://github.com/YOUR_ORG/agent-accountability-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_ORG/agent-accountability-lab/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)

## Overview

This project explores how long-lived autonomous AI agents can remain **explainable, auditable, and accountable** as they accumulate memories, pursue goals, and adapt behavior over time. The initial implementation uses a simulated environment as a controlled testbed before extending the architecture to embodied robotics.

See [`capstone_project_plan.md`](capstone_project_plan.md) for the full milestone roadmap.

## Repository Structure

```
agent-accountability-lab/
├── src/accountable_agents/   # Python package
│   ├── envs/                 # Simulation environments and adapters
│   ├── agents/               # Baseline, LLM, and memory agents
│   ├── memory/               # Episodic, semantic, retrieval
│   ├── planning/             # Goal management and planner
│   ├── accountability/       # Logger, traces, explanations
│   ├── evaluation/           # Metrics and drift detection
│   └── dashboard/            # Streamlit visualisation app
├── configs/                  # Per-experiment YAML configs
├── experiments/              # Experiment runner + results (gitignored)
├── tests/                    # Pytest test suite
├── docs/                     # Proposal, architecture, evaluation plan
├── pyproject.toml            # Project metadata and dev dependencies
└── .env.example              # Environment variable template
```

## Quick Start

### 1. Clone and set up

```bash
git clone https://github.com/YOUR_ORG/agent-accountability-lab.git
cd agent-accountability-lab
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Run an experiment

```bash
python experiments/run_experiment.py --config configs/baseline.yaml
```

### 4. Run tests

```bash
pytest
```

### 5. Lint and format

```bash
ruff check .
ruff format .
```

## CI

GitHub Actions runs **lint → typecheck → tests** on every push and pull request to `main`.
See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Docs

| Document | Description |
|---|---|
| [`docs/proposal.md`](docs/proposal.md) | Research questions and goals |
| [`docs/architecture.md`](docs/architecture.md) | System design and module map |
| [`docs/evaluation_plan.md`](docs/evaluation_plan.md) | Evaluation methodology and metrics |

## License

[MIT](LICENSE)
