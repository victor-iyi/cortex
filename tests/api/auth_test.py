"""Tests for the auth module."""

from collections.abc import Callable
from typing import Any, Final, TypeAlias

from cortex.api.auth import (
    AuthID,
    access,
    authorize,
    generate_new_token,
    get_info,
    get_license_info,
    get_user_info,
    get_user_login,
)

# Constants.
AUTH_TOKEN: Final[str] = 'xxx'
CLIENT_ID: Final[str] = 'xxx'
CLIENT_SECRET: Final[str] = 'xxx'

# Type aliases.
APIRequest: TypeAlias = Callable[..., dict[str, Any]]


def test_get_info(api_request: APIRequest) -> None:
    """Test getting cortex information."""
    assert get_info() == api_request(id=AuthID.CORTEX_INFO, method='getCortexInfo')


def test_get_user_login(api_request: APIRequest) -> None:
    """Test getting user login."""
    assert get_user_login() == api_request(id=AuthID.USER_LOGIN, method='getUserLogin')


def test_access(api_request: APIRequest) -> None:
    """Test access request."""
    assert access(CLIENT_ID, CLIENT_SECRET, method='requestAccess') == api_request(
        id=AuthID.REQUEST_ACCESS, method='requestAccess', params={'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET}
    )
    assert access(CLIENT_ID, CLIENT_SECRET, method='hasAccessRight') == api_request(
        id=AuthID.HAS_ACCESS_RIGHT,
        method='hasAccessRight',
        params={'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET},
    )


def test_authorize(api_request: APIRequest) -> None:
    """Test authorization."""
    assert authorize(CLIENT_ID, CLIENT_SECRET) == api_request(
        id=AuthID.AUTHORIZE, method='authorize', params={'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET}
    )
    assert authorize(CLIENT_ID, CLIENT_SECRET, license='license') == api_request(
        id=AuthID.AUTHORIZE,
        method='authorize',
        params={'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET, 'license': 'license'},
    )
    assert authorize(CLIENT_ID, CLIENT_SECRET, debit=1) == api_request(
        id=AuthID.AUTHORIZE,
        method='authorize',
        params={'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET, 'debit': 1},
    )


def test_generate_new_token(api_request: APIRequest) -> None:
    """Test generating a new token."""
    assert generate_new_token(AUTH_TOKEN, CLIENT_ID, CLIENT_SECRET) == api_request(
        id=AuthID.GEN_NEW_TOKEN,
        method='generateNewToken',
        params={'cortexToken': AUTH_TOKEN, 'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET},
    )


def test_get_user_info(api_request: APIRequest) -> None:
    """Test getting user information."""
    assert get_user_info(AUTH_TOKEN) == api_request(
        id=AuthID.USER_INFO, method='getUserInformation', params={'cortexToken': AUTH_TOKEN}
    )


def test_get_license_info(api_request: APIRequest) -> None:
    """Test getting license information."""
    assert get_license_info(AUTH_TOKEN) == api_request(
        id=AuthID.LICENSE_INFO, method='getLicenseInfo', params={'cortexToken': AUTH_TOKEN}
    )
