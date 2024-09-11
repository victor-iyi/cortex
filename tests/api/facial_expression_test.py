"""Test for facial expression."""

from collections.abc import Callable
from typing import Any, Final, TypeAlias

import pytest

from cortex.api.facial_expression import signature_type, threshold
from cortex.api.id import FacialExpressionID


# Constants.
AUTH_TOKEN: Final[str] = 'xxx'
PROFILE_NAME: Final[str] = 'cortex-v2-example'
SESSION_ID: Final[str] = 'f3a35fd0-9163-4cc4-ab30-4ed224369f91'

# Type aliases.
APIRequest: TypeAlias = Callable[..., dict[str, Any]]


def test_get_signature_type(api_request: APIRequest) -> None:
    """Test getting facial expression signature type."""
    assert signature_type(AUTH_TOKEN, 'get', profile_name=PROFILE_NAME) == api_request(
        id=FacialExpressionID.SIGNATURE_TYPE,
        method='facialExpressionSignatureType',
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'profile': PROFILE_NAME},
    )
    assert signature_type(AUTH_TOKEN, 'get', session_id=SESSION_ID) == api_request(
        id=FacialExpressionID.SIGNATURE_TYPE,
        method='facialExpressionSignatureType',
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'session': SESSION_ID},
    )

    with pytest.raises(ValueError, match='status must be either "set" or "get".'):
        signature_type(AUTH_TOKEN, 'invalid')

    with pytest.raises(
        AttributeError, match='Either profile_name or session_id must be provided, not both at the same time.'
    ):
        signature_type(AUTH_TOKEN, 'get')
        signature_type(AUTH_TOKEN, 'get', profile_name=PROFILE_NAME, session_id=SESSION_ID)

    # Omit signature if status is 'get'.
    assert signature_type(AUTH_TOKEN, 'get', profile_name=PROFILE_NAME, signature='universal') == api_request(
        id=FacialExpressionID.SIGNATURE_TYPE,
        method='facialExpressionSignatureType',
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'profile': PROFILE_NAME},
    )


def test_set_signature_type(api_request: APIRequest) -> None:
    """Test setting facial expression signature type."""
    assert signature_type(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME, signature='universal') == api_request(
        id=FacialExpressionID.SIGNATURE_TYPE,
        method='facialExpressionSignatureType',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'profile': PROFILE_NAME, 'signature': 'universal'},
    )
    assert signature_type(AUTH_TOKEN, 'set', session_id=SESSION_ID, signature='trained') == api_request(
        id=FacialExpressionID.SIGNATURE_TYPE,
        method='facialExpressionSignatureType',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'session': SESSION_ID, 'signature': 'trained'},
    )

    with pytest.raises(ValueError, match='status must be either "set" or "get".'):
        signature_type(AUTH_TOKEN, 'invalid')

    with pytest.raises(
        AttributeError, match='Either profile_name or session_id must be provided, not both at the same time.'
    ):
        signature_type(AUTH_TOKEN, 'set')
        signature_type(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME, session_id=SESSION_ID)

    with pytest.raises(ValueError, match='signature must be either "universal" or "trained".'):
        signature_type(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME, signature='invalid')

    with pytest.raises(AttributeError, match='signature must be provided when status is "set".'):
        signature_type(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME)


def test_get_threshold(api_request: APIRequest) -> None:
    """Test getting the facial expression threshold."""
    assert threshold(AUTH_TOKEN, 'get', action='blink', profile_name=PROFILE_NAME) == api_request(
        id=FacialExpressionID.THRESHOLD,
        method='facialExpressionThreshold',
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'action': 'blink', 'profile': PROFILE_NAME},
    )

    assert threshold(AUTH_TOKEN, 'get', action='blink', session_id=SESSION_ID) == api_request(
        id=FacialExpressionID.THRESHOLD,
        method='facialExpressionThreshold',
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'action': 'blink', 'session': SESSION_ID},
    )

    with pytest.raises(
        AttributeError, match='Either profile_name or session_id must be provided, not both at the same time.'
    ):
        threshold(AUTH_TOKEN, 'get', 'smile')
        threshold(AUTH_TOKEN, 'get', 'smile', profile_name=PROFILE_NAME, session_id=SESSION_ID)


def test_set_threshold(api_request: APIRequest) -> None:
    """Test setting the facial expression threshold."""
    assert threshold(AUTH_TOKEN, 'set', action='smile', profile_name=PROFILE_NAME, value=10) == api_request(
        id=FacialExpressionID.THRESHOLD,
        method='facialExpressionThreshold',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'action': 'smile', 'profile': PROFILE_NAME, 'value': 10},
    )

    assert threshold(AUTH_TOKEN, 'set', action='smile', session_id=SESSION_ID, value=10) == api_request(
        id=FacialExpressionID.THRESHOLD,
        method='facialExpressionThreshold',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'action': 'smile', 'session': SESSION_ID, 'value': 10},
    )

    with pytest.raises(ValueError, match='status must be either "set" or "get".'):
        threshold(AUTH_TOKEN, status='invalid', action='frown')

    with pytest.raises(
        AttributeError, match='Either profile_name or session_id must be provided, not both at the same time.'
    ):
        threshold(AUTH_TOKEN, 'set', 'smile')
        threshold(AUTH_TOKEN, 'set', 'smile', profile_name=PROFILE_NAME, session_id=SESSION_ID)

    with pytest.raises(ValueError, match='value must be between 0 and 1000.'):
        threshold(AUTH_TOKEN, 'set', 'smile', profile_name=PROFILE_NAME, value=1001)

    with pytest.raises(AttributeError, match='value must be provided when status is "set".'):
        threshold(AUTH_TOKEN, 'set', 'blink', profile_name=PROFILE_NAME)