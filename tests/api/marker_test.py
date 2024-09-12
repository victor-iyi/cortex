"""Test for marker module."""

import pytest
import time
from collections.abc import Callable
from typing import Any, Final, TypeAlias

from cortex.api.markers import inject_marker, update_marker
from cortex.api.id import MarkersID


# Constants
AUTH_TOKEN: Final[str] = '<AUTH-TOKEN>'
HEADSET_ID: Final[str] = '<HEADSET-ID>'
SESSION_ID: Final[str] = '<SESSION-ID>'

time_: int = int(time.time() * 1000)
marker_value: int = 42
marker_label: str = 'test label'

# Type aliases
ResponseTemplate: TypeAlias = Callable[..., dict[str, Any]]


def test_inject_marker(response_template: ResponseTemplate) -> None:
    """Test injecting a marker."""
    assert inject_marker(AUTH_TOKEN, SESSION_ID, time_, marker_value, marker_label) == response_template(
        id=MarkersID.INJECT,
        method='injectMarker',
        params={
            'cortexToken': AUTH_TOKEN,
            'session': SESSION_ID,
            'time': time_,
            'value': marker_value,
            'label': marker_label,
        },
    )

    with pytest.raises(ValueError, match='value must be a positive integer.'):
        inject_marker(AUTH_TOKEN, SESSION_ID, time_, -1, marker_label)

    with pytest.raises(TypeError, match='value must be either a string or an integer.'):
        inject_marker(AUTH_TOKEN, SESSION_ID, time_, 1.0, marker_label)

    with pytest.raises(ValueError, match='value must be an integer if it is a string.'):
        inject_marker(AUTH_TOKEN, SESSION_ID, time_, 'invalid', marker_label)

    port = 'Test port'
    assert inject_marker(AUTH_TOKEN, SESSION_ID, time_, marker_value, marker_label, port=port) == response_template(
        id=MarkersID.INJECT,
        method='injectMarker',
        params={
            'cortexToken': AUTH_TOKEN,
            'session': SESSION_ID,
            'time': time_,
            'value': marker_value,
            'label': marker_label,
            'port': port,
        },
    )

    extras = {'key': 'value'}
    assert inject_marker(
        AUTH_TOKEN, SESSION_ID, time_, marker_value, marker_label, port='port', extras=extras
    ) == response_template(
        id=MarkersID.INJECT,
        method='injectMarker',
        params={
            'cortexToken': AUTH_TOKEN,
            'session': SESSION_ID,
            'time': time_,
            'value': marker_value,
            'label': marker_label,
            'port': 'port',
            'extras': extras,
        },
    )


def test_update_marker(response_template: ResponseTemplate) -> None:
    """Test updating a marker."""
    marker_id = '26fccfd8-e487-4623-910a-1ba8591fcdcf'

    assert update_marker(AUTH_TOKEN, SESSION_ID, marker_id, time_) == response_template(
        id=MarkersID.UPDATE,
        method='updateMarker',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID, 'markerId': marker_id, 'time': time_},
    )

    extras = {'key': 'value'}
    assert update_marker(AUTH_TOKEN, SESSION_ID, marker_id, time_, extras=extras) == response_template(
        id=MarkersID.UPDATE,
        method='updateMarker',
        params={
            'cortexToken': AUTH_TOKEN,
            'session': SESSION_ID,
            'markerId': marker_id,
            'time': time_,
            'extras': extras,
        },
    )
