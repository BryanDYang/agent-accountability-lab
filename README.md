# Meeting Follow-Through Assistant

A proposed assistant that turns meeting recordings into summaries, cited decisions, and a living action-item list that updates across later meetings.

The repository has an installable Python CLI scaffold and offline smoke tests.
Meeting processing and the background service are not implemented yet. See the
[Milestone 1 proposal](docs/milestone_1/project_proposal.md) for the planned scope.

**Repository:** https://github.com/BryanDYang/ai-capstone

## Quick start

Install Python 3.12 and uv, then run:

```bash
git clone https://github.com/BryanDYang/ai-capstone.git
cd ai-capstone
uv sync --locked --extra dev
uv run labsync --help
uv run labsync status
uv run labsync status --json
```

No API keys, meeting data, or `contexts` files are needed for this scaffold.

## Development

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run pytest
```

CI runs these checks and the installed CLI on every push and pull request.
Application code lives in `src/labsync`, tests in `tests`, and project documents
in `docs`. See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow
and [upstream provenance](docs/upstream.md) for how the professor's
`agent-sandbox` informed this setup.

## License

Project code uses the [MIT license](LICENSE). Third-party code and assets retain
their own licenses and notices.

**Team:** Bryan Yang, Will Liu, and Guadalupe Cantera

**Course:** CIS-5980, AI Engineering track

Previous project materials are retained in [the guardian-agent archive](docs/archive/guardian-agent/). They describe a superseded direction. The [weekly journal](docs/weekly_journal.md) preserves historical progress; its earlier entries refer to that direction.
