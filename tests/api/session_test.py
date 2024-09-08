"""Test for session module."""

from collections.abc import Callable
from typing import Any, Final, TypeAlias

from cortex.api.session import create_session, update_session, query_session
from cortex.api.id import SessionID

# Constants.
AUTH_TOKEN: Final[str] = '<AUTH-TOKEN>'
SESSION_ID: Final[str] = '<SESSION-ID>'
HEADSET_ID: Final[str] = '<HEADSET-ID>'

# Type aliases.
ResponseTemplate: TypeAlias = Callable[..., dict[str, Any]]


def test_create_session(response_template: ResponseTemplate) -> None:
    """Test creating a session."""
    assert create_session(AUTH_TOKEN, HEADSET_ID, 'open') == response_template(
        id=SessionID.CREATE,
        method='createSession',
        params={'cortexToken': AUTH_TOKEN, 'headset': HEADSET_ID, 'status': 'open'},
    )

    assert create_session(AUTH_TOKEN, HEADSET_ID, 'active') == response_template(
        id=SessionID.CREATE,
        method='createSession',
        params={'cortexToken': AUTH_TOKEN, 'headset': HEADSET_ID, 'status': 'active'},
    )


def test_update_session(response_template: ResponseTemplate) -> None:
    """Test updating a session."""
    assert update_session(AUTH_TOKEN, SESSION_ID, 'active') == response_template(
        id=SessionID.UPDATE,
        method='updateSession',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID, 'status': 'active'},
    )

    assert update_session(AUTH_TOKEN, SESSION_ID, 'close') == response_template(
        id=SessionID.UPDATE,
        method='updateSession',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID, 'status': 'close'},
    )


def test_query_session(response_template: ResponseTemplate) -> None:
    """Test querying a session."""
    assert query_session(AUTH_TOKEN) == response_template(
        id=SessionID.QUERY, method='querySession', params={'cortexToken': AUTH_TOKEN}
    )
