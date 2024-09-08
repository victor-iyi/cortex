"""Tests for the handler module."""

from collections.abc import Callable
from typing import Any, Final, TypeAlias
import pytest
from cortex.api.handler import stream_data

# Constants
SAMPLE_TIME: Final[float] = 1234567890.123
# Type aliases.
SampleData: TypeAlias = Callable[[], dict[str, Any]]


def test_stream_data_com(sample_data: SampleData) -> None:
    """Test streaming 'com' data."""
    result = stream_data(sample_data(), 'com')
    assert result == {'action': 'action1', 'power': 100, 'time': SAMPLE_TIME}


def test_stream_data_fac(sample_data: SampleData) -> None:
    """Test streaming 'fac' data."""
    result = stream_data(sample_data(), 'fac')
    assert result == {'eyeAct': 1, 'uAct': 2, 'uPow': 3, 'lAct': 4, 'lPow': 5, 'time': SAMPLE_TIME}


def test_stream_data_eeg(sample_data: SampleData) -> None:
    """Test streaming 'eeg' data."""
    result = stream_data(sample_data(), 'eeg')
    assert result == {'eeg': [1.0, 2.0, 3.0, 4.0], 'time': SAMPLE_TIME}


def test_stream_data_dev(sample_data: SampleData) -> None:
    """Test streaming 'dev' data."""
    result = stream_data(sample_data(), 'dev')
    assert result == {'signal': 'good', 'dev': 'device1', 'batteryPercent': 75, 'time': SAMPLE_TIME}


def test_stream_data_sys(sample_data: SampleData) -> None:
    """Test streaming 'sys' data."""
    result = stream_data(sample_data(), 'sys')
    assert result == {'version': '1.0', 'status': 'ok'}


def test_stream_data_invalid_key(sample_data: SampleData) -> None:
    """Test streaming with an invalid key."""
    with pytest.raises(KeyError, match='Unknown key: invalid'):
        stream_data(sample_data(), 'invalid')
