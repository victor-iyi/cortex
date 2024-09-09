"""conftest.py: pytest configuration file for the tests in the tests/ directory."""

from collections.abc import Callable
from typing import Any, Final

import pytest


# Constants.
SAMPLE_TIME: Final[float] = 1234567890.123


# pylint: disable=redefined-builtin
@pytest.fixture
def response_template() -> Callable[[int, str, dict[str, Any] | None], dict[str, Any]]:
    """Template structure for the API."""

    def _response_template(id: int, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if params is None:
            return {'id': id, 'jsonrpc': '2.0', 'method': method}
        return {'id': id, 'jsonrpc': '2.0', 'method': method, 'params': params}

    return _response_template


@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Fixture to provide sample data for testing."""
    return {
        'time': SAMPLE_TIME,
        'com': ['action1', 100],
        'fac': [1, 2, 3, 4, 5],
        'eeg': [1.0, 2.0, 3.0, 4.0],
        'mot': [0.1, 0.2, 0.3],
        'dev': [1, 'good', 'device1', 75],
        'met': [0.5, 0.6, 0.7],
        'pow': [10, 20, 30],
        'sys': {'version': '1.0', 'status': 'ok'},
    }
