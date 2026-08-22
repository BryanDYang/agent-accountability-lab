"""Shared pytest fixtures and configuration."""
import pytest


@pytest.fixture
def dummy_observation():
    """A minimal observation dict for unit tests."""
    return {
        "position": (0, 0),
        "surroundings": [],
        "energy": 100,
        "step": 0,
    }
