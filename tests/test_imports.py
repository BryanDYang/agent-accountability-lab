"""Smoke tests – verify the package imports without errors."""


def test_package_imports():
    import accountable_agents  # noqa: F401
    import accountable_agents.agents  # noqa: F401
    import accountable_agents.envs  # noqa: F401
    import accountable_agents.memory  # noqa: F401
    import accountable_agents.planning  # noqa: F401
    import accountable_agents.accountability  # noqa: F401
    import accountable_agents.evaluation  # noqa: F401
