"""Test for the profile module."""

from collections.abc import Callable
from typing import Any, Final, TypeAlias

import pytest

from cortex.api.profile import query_profile, current_profile, setup_profile, load_guest, detection_info
from cortex.api.id import ProfileID

# Constants.
AUTH_TOKEN: Final[str] = '<AUTH-TOKEN>'
PROFILE_NAME: Final[str] = '<PROFILE-NAME>'
HEADSET_ID: Final[str] = '<HEADSET-ID>'

# Type aliases.
ResponseTemplate: TypeAlias = Callable[..., dict[str, Any]]


def test_query_profile(response_template: ResponseTemplate) -> None:
    """Test querying a profile."""
    assert query_profile(AUTH_TOKEN) == response_template(
        id=ProfileID.QUERY, method='queryProfile', params={'cortexToken': AUTH_TOKEN}
    )


def test_current_profile(response_template: ResponseTemplate) -> None:
    """Test getting the current profile."""
    assert current_profile(AUTH_TOKEN, HEADSET_ID) == response_template(
        id=ProfileID.CURRENT, method='getCurrentProfile', params={'cortexToken': AUTH_TOKEN, 'headset': HEADSET_ID}
    )


def test_setup_profile(response_template: ResponseTemplate) -> None:
    """Test setting up a profile."""
    assert setup_profile(AUTH_TOKEN, 'create', PROFILE_NAME, headset_id=HEADSET_ID) == response_template(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={'cortexToken': AUTH_TOKEN, 'status': 'create', 'profile': PROFILE_NAME, 'headset': HEADSET_ID},
    )

    assert setup_profile(AUTH_TOKEN, 'load', PROFILE_NAME, headset_id=HEADSET_ID) == response_template(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={'cortexToken': AUTH_TOKEN, 'status': 'load', 'profile': PROFILE_NAME, 'headset': HEADSET_ID},
    )

    assert setup_profile(AUTH_TOKEN, 'unload', PROFILE_NAME, headset_id=HEADSET_ID) == response_template(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={'cortexToken': AUTH_TOKEN, 'status': 'unload', 'profile': PROFILE_NAME, 'headset': HEADSET_ID},
    )
    assert setup_profile(AUTH_TOKEN, 'save', PROFILE_NAME, headset_id=HEADSET_ID) == response_template(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={'cortexToken': AUTH_TOKEN, 'status': 'save', 'profile': PROFILE_NAME, 'headset': HEADSET_ID},
    )
    assert setup_profile(AUTH_TOKEN, 'delete', PROFILE_NAME) == response_template(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={'cortexToken': AUTH_TOKEN, 'status': 'delete', 'profile': PROFILE_NAME},
    )

    with pytest.raises(AssertionError, match='status must be one of create, load, unload, save, rename, delete.'):
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

    assert setup_profile(AUTH_TOKEN, 'rename', PROFILE_NAME, new_profile_name='new-profile') == response_template(
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
    ) == response_template(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={
            'cortexToken': AUTH_TOKEN,
            'status': 'rename',
            'profile': PROFILE_NAME,
            'newProfileName': 'new-profile',
        },
    )
    assert setup_profile(AUTH_TOKEN, 'delete', PROFILE_NAME, headset_id=HEADSET_ID) == response_template(
        id=ProfileID.SETUP,
        method='setupProfile',
        params={'cortexToken': AUTH_TOKEN, 'status': 'delete', 'profile': PROFILE_NAME},
    )


def test_load_guest_profile(response_template: ResponseTemplate) -> None:
    """Test loading a guest profile."""
    assert load_guest(AUTH_TOKEN, HEADSET_ID) == response_template(
        id=ProfileID.GUEST, method='loadGuestProfile', params={'cortexToken': AUTH_TOKEN, 'headset': HEADSET_ID}
    )


def test_detection_info(response_template: ResponseTemplate) -> None:
    """Test getting detection information."""
    assert detection_info('mentalCommand') == response_template(
        id=ProfileID.DETECTION_INFO, method='getDetectionInfo', params={'detection': 'mentalCommand'}
    )
    assert detection_info('facialExpression') == response_template(
        id=ProfileID.DETECTION_INFO, method='getDetectionInfo', params={'detection': 'facialExpression'}
    )

    with pytest.raises(AssertionError, match='detection must be either "mentalCommand" or "facialExpression".'):
        detection_info('invalid')
