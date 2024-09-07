"""Tests for the auth module."""

from typing import Any, Final
from cortex.api.auth import (
    access,
    authorize,
    generate_new_token,
    get_info,
    get_license_info,
    get_user_info,
    get_user_login,
)
from cortex.api.auth import AuthID


# Constants.
AUTH_TOKEN: Final[str] = '<AUTH-TOKEN>'
CLIENT_ID: Final[str] = '<CLIENT-ID>'
CLIENT_SECRET: Final[str] = '<CLIENT-SECRET>'


def response_template(id: int, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Template structure for the API."""
    if params is None:
        return {'id': id, 'jsonrpc': '2.0', 'method': method}
    return {'id': id, 'jsonrpc': '2.0', 'method': method, 'params': params}


def test_get_info() -> None:
    """Test getting cortex information."""
    assert get_info() == response_template(id=AuthID.CORTEX_INFO, method='getCortexInfo')


def test_get_user_login() -> None:
    """Test getting user login."""
    assert get_user_login() == response_template(id=AuthID.USER_LOGIN, method='getUserLogin')


def test_access() -> None:
    """Test access request."""
    assert access(CLIENT_ID, CLIENT_SECRET, method='requestAccess') == response_template(
        id=AuthID.REQUEST_ACCESS, method='requestAccess', params={'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET}
    )
    assert access(CLIENT_ID, CLIENT_SECRET, method='hasAccessRight') == response_template(
        id=AuthID.HAS_ACCESS_RIGHT,
        method='hasAccessRight',
        params={'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET},
    )


def test_authorize() -> None:
    """Test authorization."""
    assert authorize(CLIENT_ID, CLIENT_SECRET) == response_template(
        id=AuthID.AUTHORIZE, method='authorize', params={'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET}
    )
    assert authorize(CLIENT_ID, CLIENT_SECRET, license='license') == response_template(
        id=AuthID.AUTHORIZE,
        method='authorize',
        params={'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET, 'license': 'license'},
    )
    assert authorize(CLIENT_ID, CLIENT_SECRET, debit=1) == response_template(
        id=AuthID.AUTHORIZE,
        method='authorize',
        params={'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET, 'debit': 1},
    )


def test_generate_new_token() -> None:
    """Test generating a new token."""
    assert generate_new_token(AUTH_TOKEN, CLIENT_ID, CLIENT_SECRET) == response_template(
        id=AuthID.GEN_NEW_TOKEN,
        method='generateNewToken',
        params={'cortexToken': AUTH_TOKEN, 'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET},
    )


def test_get_user_info() -> None:
    """Test getting user information."""
    assert get_user_info(AUTH_TOKEN) == response_template(
        id=AuthID.USER_INFO, method='getUserInformation', params={'cortexToken': AUTH_TOKEN}
    )


def test_get_license_info() -> None:
    """Test getting license information."""
    assert get_license_info(AUTH_TOKEN) == response_template(
        id=AuthID.LICENSE_INFO, method='getLicenseInfo', params={'cortexToken': AUTH_TOKEN}
    )
