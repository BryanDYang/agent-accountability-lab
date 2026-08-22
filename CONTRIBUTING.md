# Contributing to agent-accountability-lab

Thank you for your interest in contributing! This document covers the workflow, coding standards, and expectations for contributions.

## Table of Contents

- [Getting Started](#getting-started)
- [Branching Strategy](#branching-strategy)
- [Making Changes](#making-changes)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

---

## Getting Started

1. **Fork** the repository and clone your fork:

   ```bash
   git clone https://github.com/YOUR_USERNAME/agent-accountability-lab.git
   cd agent-accountability-lab
   ```
2. **Set up the dev environment:**

   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev]"
   ```
3. **Copy the environment template and fill in your keys:**

   ```bash
   cp .env.example .env
   ```
4. **Verify everything works:**

   ```bash
   pytest
   ruff check .
   ```

---

## Branching Strategy

| Branch                          | Purpose                         |
| ------------------------------- | ------------------------------- |
| `main`                        | Stable, always passing CI       |
| `feature/<short-description>` | New features or modules         |
| `fix/<short-description>`     | Bug fixes                       |
| `docs/<short-description>`    | Documentation-only changes      |
| `experiment/<name>`           | Exploratory / research branches |

Create your branch from `main`:

```bash
git checkout -b feature/my-feature
```

---

## Making Changes

- Keep commits small and focused — one logical change per commit.
- Write a clear commit message in the imperative mood:✅ `Add episodic memory retrieval`❌ `Added some stuff to memory`
- Never commit `.env` or any file containing secrets or API keys.
- Experiment results (`experiments/results/`) are gitignored — do not force-add them.

---

## Code Standards

This project uses [`ruff`](https://docs.astral.sh/ruff/) for linting and formatting, and [`mypy`](https://mypy.readthedocs.io/) for type checking.

**Before every commit, run:**

```bash
ruff check . --fix   # auto-fix lint issues
ruff format .        # auto-format code
mypy src/            # check types
```

Key conventions:

- Line length: **100 characters**
- Target Python version: **3.11+**
- Use type annotations on all public functions and methods.
- Docstrings on all public classes and functions (one-line summary is fine for simple cases).
- No hardcoded secrets — use `os.environ` or `python-dotenv`.

---

## Testing

All new code should include tests in `tests/`. Run the full suite with:

```bash
pytest
```

For a specific file or test:

```bash
pytest tests/test_imports.py
pytest -k "test_my_feature"
```

Coverage is reported automatically. Aim to keep coverage at or above its current level — CI will show you the diff.

---

## Pull Request Process

1. Push your branch and open a PR against `main`.
2. Fill in the PR description — explain **what** changed and **why**.
3. Ensure all CI checks pass (lint → typecheck → tests).
4. Request a review from at least one other contributor.
5. Address review feedback; do not force-push after a review has started.
6. A maintainer will merge once approved and CI is green.

---

## Reporting Issues

Open a [GitHub Issue](../../issues) with:

- A clear title describing the problem.
- Steps to reproduce.
- Expected vs. actual behaviour.
- Python version, OS, and any relevant config.

For security vulnerabilities, please **do not** open a public issue — contact a maintainer directly.
