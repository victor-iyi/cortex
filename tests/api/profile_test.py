"""Test for the profile module."""

from collections.abc import Callable
from typing import Any, Final, TypeAlias

import pytest

from cortex.api.profile import query_profile, current_profile, setup_profile, load_guest, detection_info
from cortex.api.id import ProfileID

# Constants.
AUTH_TOKEN: Final[str] = 'xxx'
PROFILE_NAME: Final[str] = 'cortex-v2-example'
HEADSET_ID: Final[str] = 'EPOCX-12345678'

# Type aliases.
APIRequest: TypeAlias = Callable[..., dict[str, Any]]


def test_query_profile(api_request: APIRequest) -> None:
    """Test querying a profile."""
    assert query_profile(AUTH_TOKEN) == api_request(
        id=ProfileID.QUERY, method='queryProfile', params={'cortexToken': AUTH_TOKEN}
    )


def test_current_profile(api_request: APIRequest) -> None:
    """Test getting the current profile."""
    assert current_profile(AUTH_TOKEN, HEADSET_ID) == api_request(
        id=ProfileID.CURRENT, method='getCurrentProfile', params={'cortexToken': AUTH_TOKEN, 'headset': HEADSET_ID}
    )


def test_setup_profile(api_request: APIRequest) -> None:
    """Test setting up a profile."""
    assert setup_profile(AUTH_TOKEN, 'create', PROFILE_NAME, headset_id=HEADSET_ID) == api_request(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={'cortexToken': AUTH_TOKEN, 'status': 'create', 'profile': PROFILE_NAME, 'headset': HEADSET_ID},
    )

    assert setup_profile(AUTH_TOKEN, 'load', PROFILE_NAME, headset_id=HEADSET_ID) == api_request(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={'cortexToken': AUTH_TOKEN, 'status': 'load', 'profile': PROFILE_NAME, 'headset': HEADSET_ID},
    )

    assert setup_profile(AUTH_TOKEN, 'unload', PROFILE_NAME, headset_id=HEADSET_ID) == api_request(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={'cortexToken': AUTH_TOKEN, 'status': 'unload', 'profile': PROFILE_NAME, 'headset': HEADSET_ID},
    )
    assert setup_profile(AUTH_TOKEN, 'save', PROFILE_NAME, headset_id=HEADSET_ID) == api_request(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={'cortexToken': AUTH_TOKEN, 'status': 'save', 'profile': PROFILE_NAME, 'headset': HEADSET_ID},
    )
    assert setup_profile(AUTH_TOKEN, 'delete', PROFILE_NAME) == api_request(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={'cortexToken': AUTH_TOKEN, 'status': 'delete', 'profile': PROFILE_NAME},
    )

    with pytest.raises(ValueError, match='status must be one of create, load, unload, save, rename, delete.'):
        setup_profile(AUTH_TOKEN, 'invalid', PROFILE_NAME)

    with pytest.raises(ValueError, match='new_profile_name must be provided when status is "rename".'):
        setup_profile(AUTH_TOKEN, 'rename', PROFILE_NAME)

    with pytest.raises(
        ValueError, match='headset_id must be provided when status is "create", "load", "unload", or "save".'
    ):
        setup_profile(AUTH_TOKEN, 'create', PROFILE_NAME)
        setup_profile(AUTH_TOKEN, 'load', PROFILE_NAME)
        setup_profile(AUTH_TOKEN, 'unload', PROFILE_NAME)
        setup_profile(AUTH_TOKEN, 'save', PROFILE_NAME)

    assert setup_profile(AUTH_TOKEN, 'rename', PROFILE_NAME, new_profile_name='new-profile') == api_request(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={
            'cortexToken': AUTH_TOKEN,
            'status': 'rename',
            'profile': PROFILE_NAME,
            'newProfileName': 'new-profile',
        },
    )

    assert setup_profile(
        AUTH_TOKEN, 'rename', PROFILE_NAME, headset_id=HEADSET_ID, new_profile_name='new-profile'
    ) == api_request(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={
            'cortexToken': AUTH_TOKEN,
            'status': 'rename',
            'profile': PROFILE_NAME,
            'newProfileName': 'new-profile',
        },
    )
    assert setup_profile(AUTH_TOKEN, 'delete', PROFILE_NAME, headset_id=HEADSET_ID) == api_request(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={'cortexToken': AUTH_TOKEN, 'status': 'delete', 'profile': PROFILE_NAME},
    )


def test_load_guest_profile(api_request: APIRequest) -> None:
    """Test loading a guest profile."""
    assert load_guest(AUTH_TOKEN, HEADSET_ID) == api_request(
        id=ProfileID.GUEST, method='loadGuestProfile', params={'cortexToken': AUTH_TOKEN, 'headset': HEADSET_ID}
    )


def test_detection_info(api_request: APIRequest) -> None:
    """Test getting detection information."""
    assert detection_info('mentalCommand') == api_request(
        id=ProfileID.DETECTION_INFO, method='getDetectionInfo', params={'detection': 'mentalCommand'}
    )
    assert detection_info('facialExpression') == api_request(
        id=ProfileID.DETECTION_INFO, method='getDetectionInfo', params={'detection': 'facialExpression'}
    )

    with pytest.raises(ValueError, match='detection must be either "mentalCommand" or "facialExpression".'):
        detection_info('invalid')
