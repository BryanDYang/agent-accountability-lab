# Professor code reference

The initial repository setup draws on the local `contexts/agent-sandbox`
reference supplied by the team. Its README identifies it as Chris
Callison-Burch's group's multi-agent simulation framework. It is not the
meeting recording or transcription pipeline described in the proposal.

The scaffold follows its `pyproject.toml` packaging approach, Python 3.12
development version, `uv` dependency management, and offline Pytest/CI workflow.
The application CLI and tests are new code. No upstream runtime code, datasets,
game assets, credentials, or generated files have been copied into the package.
The ignored `contexts` directory is not needed to install or test this project.

Potential reuse candidates are `text_adventure_games/llm_client.py` for model
adapters, `usage.py` for usage accounting, and their offline tests. Evaluate their
dependencies and fit before integrating them. Simulation memory is not yet a
validated substitute for the proposal's evidence-backed commitment history.

The supplied snapshot's root LICENSE is MIT, copyright 2024
interactive-fiction-class. If source is incorporated later, preserve its notice
and record the exact upstream revision, copied files, and modifications. A
verified upstream revision has not yet been recorded. Check individual assets
separately; the root license alone does not establish their redistribution terms.
