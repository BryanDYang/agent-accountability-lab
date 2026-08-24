# Quick Start Guide

> **Goal:** Get the project running locally and execute your first experiment in under 10 minutes.

## Prerequisites

| Requirement | Minimum version | Check |
|---|---|---|
| Python | 3.11 | `python --version` |
| Git | any recent | `git --version` |
| An LLM API key | — | OpenAI, Anthropic, or a local Ollama instance |

---

## Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_ORG/agent-accountability-lab.git
cd agent-accountability-lab
```

---

## Step 2 — Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

---

## Step 3 — Install the package and dev dependencies

```bash
pip install -e ".[dev]"
```

This installs the `accountable_agents` package in editable mode so code changes in `src/` are picked up immediately, along with all dev tools (pytest, ruff, mypy).

---

## Step 4 — Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in at minimum:

```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

> **Note:** `.env` is gitignored. Never commit it.

---

## Step 5 — Verify the setup

Run the test suite to confirm everything installed correctly:

```bash
pytest
```

Expected output:

```
collected 1 item

tests/test_imports.py .                                    [100%]

======= 1 passed in ...s =======
```

---

## Step 6 — Run your first experiment

The **baseline** config runs a rule-based agent with no LLM or memory — no API key required:

```bash
python experiments/run_experiment.py --config configs/baseline.yaml
```

Expected output:

```
Loaded config: configs/baseline.yaml
Output dir:    experiments/results/baseline
Agent type:    baseline

Experiment runner not yet implemented – skeleton only.
```

> The runner is a scaffold at this stage (Milestone 0). Full agent loop implementation begins in Milestone 1–2.

---

## Step 7 — Try a more capable config (requires API key)

Once your `.env` is configured with an LLM key:

```bash
python experiments/run_experiment.py --config configs/memory_agent.yaml
```

---

## Useful Commands

| Task | Command |
|---|---|
| Run tests | `pytest` |
| Run tests with verbose output | `pytest -v` |
| Run a single test file | `pytest tests/test_imports.py` |
| Lint | `ruff check .` |
| Auto-fix lint issues | `ruff check . --fix` |
| Format code | `ruff format .` |
| Type check | `mypy src/` |

---

## Next Steps

- Read [`docs/architecture.md`](architecture.md) to understand the system design.
- Check [`docs/evaluation_plan.md`](evaluation_plan.md) for the experiment methodology.
- See [`CONTRIBUTING.md`](../CONTRIBUTING.md) before opening a PR.
- Follow the milestone plan in [`capstone_project_plan.md`](../capstone_project_plan.md).
