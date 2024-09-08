"""Test for facial expression."""

from collections.abc import Callable
from typing import Any, Final, TypeAlias

import pytest

from cortex.api.facial_expression import signature_type, threshold
from cortex.api.id import FacialExpressionID


# Constants.
AUTH_TOKEN: Final[str] = '<AUTH-TOKEN>'
PROFILE_NAME: Final[str] = '<PROFILE-NAME>'
SESSION_ID: Final[str] = '<SESSION-ID>'

# Type aliases.
ResponseTemplate: TypeAlias = Callable[..., dict[str, Any]]


def test_signature_type(response_template: ResponseTemplate) -> None:
    """Test setting the facial expression signature type."""
    _id = FacialExpressionID.SIGNATURE_TYPE
    method = 'facialExpressionSignatureType'

    # Either profile_name or session_id must be provided, not both at the same time.
    with pytest.raises((AssertionError, ValueError)):
        # This should raise AssertionError: status must be either "set" or "get".
        signature_type(AUTH_TOKEN, 'post', profile_name=PROFILE_NAME)

        # This should raise AssertionError: profile_name & session_id are provided.
        signature_type(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME, session_id=SESSION_ID)

        # This should raise AssertionError: signature must be either "set", "universal", or "trained".
        signature_type(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME, signature='invalid')

    # status is 'set'.
    assert signature_type(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME, signature='set') == response_template(
        id=_id,
        method=method,
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'profile': PROFILE_NAME, 'signature': 'set'},
    )
    assert signature_type(AUTH_TOKEN, 'set', session_id=SESSION_ID, signature='set') == response_template(
        id=_id,
        method=method,
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'session': SESSION_ID, 'signature': 'set'},
    )

    # status is 'get'.
    assert signature_type(AUTH_TOKEN, 'get', session_id=SESSION_ID, signature='universal') == response_template(
        id=_id,
        method=method,
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'session': SESSION_ID, 'signature': 'universal'},
    )
    assert signature_type(AUTH_TOKEN, 'get', profile_name=PROFILE_NAME, signature='trained') == response_template(
        id=_id,
        method=method,
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'profile': PROFILE_NAME, 'signature': 'trained'},
    )


def test_threshold(response_template: ResponseTemplate) -> None:
    """Test setting the facial expression threshold."""
    _id = FacialExpressionID.THRESHOLD
    method = 'facialExpressionThreshold'

    with pytest.raises(AssertionError):
        # This should raise AssertionError: status must be either "set" or "get".
        threshold(AUTH_TOKEN, status='post', action='smile', profile_name=PROFILE_NAME, value=10)
        # This should raise AssertionError: profile_name & session_id are provided.
        threshold(AUTH_TOKEN, status='set', action='smile', profile_name=PROFILE_NAME, session_id=SESSION_ID, value=10)

    with pytest.raises(ValueError, match='value must be between 0 and 1000.'):
        # This should raise ValueError: value is not between 0 and 1000.
        threshold(AUTH_TOKEN, status='set', action='smile', profile_name=PROFILE_NAME, value=1001)

    # status is 'set'.
    assert threshold(
        AUTH_TOKEN, status='set', action='smile', profile_name=PROFILE_NAME, value=10
    ) == response_template(
        id=_id,
        method=method,
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'action': 'smile', 'profile': PROFILE_NAME, 'value': 10},
    )

    assert threshold(AUTH_TOKEN, status='set', action='smile', session_id=SESSION_ID, value=10) == response_template(
        id=_id,
        method=method,
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'action': 'smile', 'session': SESSION_ID, 'value': 10},
    )

    # status is 'get'.
    assert threshold(AUTH_TOKEN, status='get', action='smile', profile_name=PROFILE_NAME) == response_template(
        id=_id,
        method=method,
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'action': 'smile', 'profile': PROFILE_NAME},
    )

    assert threshold(AUTH_TOKEN, status='get', action='smile', session_id=SESSION_ID) == response_template(
        id=_id,
        method=method,
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'action': 'smile', 'session': SESSION_ID},
    )
