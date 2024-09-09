"""Test for session module."""

from collections.abc import Callable
from typing import Any, Final, TypeAlias

from cortex.api.session import create_session, update_session, query_session
from cortex.api.id import SessionID

# Constants.
AUTH_TOKEN: Final[str] = 'xxx'
SESSION_ID: Final[str] = 'f3a35fd0-9163-4cc4-ab30-4ed224369f91'
HEADSET_ID: Final[str] = 'EPOCX-12345678'

# Type aliases.
APIRequest: TypeAlias = Callable[..., dict[str, Any]]


def test_create_session(api_request: APIRequest) -> None:
    """Test creating a session."""
    assert create_session(AUTH_TOKEN, HEADSET_ID, 'open') == api_request(
        id=SessionID.CREATE,
        method='createSession',
        params={'cortexToken': AUTH_TOKEN, 'headset': HEADSET_ID, 'status': 'open'},
    )

    assert create_session(AUTH_TOKEN, HEADSET_ID, 'active') == api_request(
        id=SessionID.CREATE,
        method='createSession',
        params={'cortexToken': AUTH_TOKEN, 'headset': HEADSET_ID, 'status': 'active'},
    )


def test_update_session(api_request: APIRequest) -> None:
    """Test updating a session."""
    assert update_session(AUTH_TOKEN, SESSION_ID, 'active') == api_request(
        id=SessionID.UPDATE,
        method='updateSession',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID, 'status': 'active'},
    )

    assert update_session(AUTH_TOKEN, SESSION_ID, 'close') == api_request(
        id=SessionID.UPDATE,
        method='updateSession',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID, 'status': 'close'},
    )


def test_query_session(api_request: APIRequest) -> None:
    """Test querying a session."""
    assert query_session(AUTH_TOKEN) == api_request(
        id=SessionID.QUERY, method='querySession', params={'cortexToken': AUTH_TOKEN}
    )
