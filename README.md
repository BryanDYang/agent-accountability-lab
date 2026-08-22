# agent-accountability-lab

> **Trajectory-level detection of memory-induced behavioral drift in persistent AI agents**

[![CI](https://github.com/YOUR_ORG/agent-accountability-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_ORG/agent-accountability-lab/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)

## Overview

This research-driven capstone builds a reproducible framework for detecting and diagnosing deliberately induced behavioral drift in a persistent, memory-augmented AI agent. A deterministic grid world provides the controlled testbed; the primary contribution is the trajectory evidence, drift-injection protocol, quantitative evaluation, and investigation workflow.

The minimum experiment compares a reactive baseline, a memory-enabled control agent, and two controlled drift conditions: **memory poisoning** and **retrieval bias**. More complex memory, autonomous goal management, robotics simulation, and physical embodiment are future work.

See [`capstone_project_plan.md`](capstone_project_plan.md) for the course-aligned milestone roadmap and [`docs/evaluation_plan.md`](docs/evaluation_plan.md) for the experiment protocol.

## Repository Structure

```
agent-accountability-lab/
├── src/accountable_agents/   # Environment, agents, memory, traces, and evaluation
├── configs/                  # Reproducible experimental conditions
├── experiments/              # Experiment runner and generated results
├── tests/                    # Unit, schema, metric, and integration tests
├── docs/                     # Proposal, architecture, and evaluation protocol
├── pyproject.toml            # Project metadata and dependencies
└── .env.example              # Environment variable template
```

## Quick Start

```bash
# 1. Clone
git clone https://github.com/YOUR_ORG/agent-accountability-lab.git
cd agent-accountability-lab

# 2. Create a virtual environment and install
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# 3. Configure secrets
cp .env.example .env   # then edit .env with your API keys

# 4. Verify
pytest

# 5. Run the baseline experiment
python experiments/run_experiment.py --config configs/baseline.yaml
```

The experiment runner is currently a scaffold. Milestone 2 will make the baseline command deterministic and produce versioned trajectory records and metrics.

For the full walkthrough — prerequisites, expected output, and next steps — see [`docs/quickstart.md`](docs/quickstart.md).

## CI

GitHub Actions runs **lint → typecheck → tests** on every push and pull request to `main`.
See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Docs

| Document | Description |
|---|---|
| [`docs/proposal.md`](docs/proposal.md) | Track declaration, research question, MVP, and risks |
| [`docs/architecture.md`](docs/architecture.md) | System design and module map |
| [`docs/evaluation_plan.md`](docs/evaluation_plan.md) | Conditions, interventions, metrics, and experiment protocol |

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the branching strategy, coding standards, testing expectations, and PR process.

## License

[MIT](LICENSE)
