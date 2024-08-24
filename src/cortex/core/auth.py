"""Authentication requests for the Emotiv Cortex API.

This module contains functions to request access, authorize, create a
session, and setup a profile.

"""

from enum import IntEnum
from typing import Literal


class AuthID(IntEnum):
    """Authentication request IDs."""

    REQUEST_ACCESS = 3
    AUTHORIZE = 4
    CREATE_SESSION = 5
    HAS_ACCESS_RIGHT = 20
    GET_CURRENT_PROFILE = 21
    CORTEX_INFO = 22


def authorize(
    *,
    client_id: str,
    client_secret: str,
    license: str | None = None,
    debit: int | None = None,
) -> dict[str, str | int, dict[str, str | int]]:
    """Authorize the client.

    Keyword Args:
        client_id (str): The client ID.
        client_secret (str): The client secret.
        license (str): The license.
        debit (int): The debit.

    Returns:
        dict[str, str | int, dict[str, str | int]]: The authorization status.

    """
    _params = {
        'clientId': client_id,
        'clientSecret': client_secret,
    }

    if license is not None:
        _params['license'] = license

    if debit is not None:
        _params['debit'] = debit

    authorization: dict[str, str | int, dict[str, str | int]] = {
        'id': AuthID.AUTHORIZE,
        'jsonrpc': '2.0',
        'method': 'authorize',
        'params': _params,
    }

    return authorization


def session(
    auth: str,
    *,
    headset_id: str | None = None,
    session_id: str | None = None,
    status: Literal['active', 'close'] = 'active',
) -> dict[str, str | int, dict[str, str]]:
    """Create or close a session.

    Args:
        auth (str): The Cortex authentication token.

    Keyword Args:
        headset_id (str, optional): The headset ID.
        session_id (str, optional): The session ID.
        status (Literal['active', 'close'], optional): The session status.

    Returns:
        dict[str, str | int, dict[str, str]]: The session status.

    """
    assert status in ['active', 'close'], 'status must be either "active" or "close".'

    _params: dict[str, str] = {
        'cortexToken': auth,
    }
    if headset_id is not None and status == 'active':
        _method = 'createSession'
        _params['headset'] = headset_id
    elif session_id is not None and status == 'close':
        _method = 'updateSession'
        _params['session'] = session_id
    else:
        raise ValueError(
            'headset_id must be provided for active session, session_id must be provided for close session.'
        )

    _params['status'] = status

    _session: dict[str, str | int, dict[str, str]] = {
        'id': AuthID.CREATE_SESSION,
        'jsonrpc': '2.0',
        'method': _method,
        'params': _params,
    }

    return _session


def access(
    *,
    client_id: str,
    client_secret: str,
    method: Literal['requestAccess', 'hasAccessRight'],
) -> dict[str, str | int | dict[str, str]]:
    """Request access or verify access right.

    Keyword Args:
        client_id (str): The client ID.
        client_secret (str): The client secret.
        method (Literal['requestAccess', 'hasAccessRight']): The method.

    Returns:
        dict[str, str | int | dict[str, str]]: The access status.

    """
    assert method in ['requestAccess', 'hasAccessRight'], 'method must be either "requestAccess" or "hasAccessRight".'

    if method == 'requestAccess':
        _id = AuthID.REQUEST_ACCESS
    else:
        _id = AuthID.HAS_ACCESS_RIGHT

    _access: dict[str, str | int | dict[str, str]] = {
        'id': _id,
        'jsonrpc': '2.0',
        'method': method,
        'params': {
            'clientId': client_id,
            'clientSecret': client_secret,
        },
    }

    return _access


def get_info() -> dict[str, str | int]:
    """Get the Cortex info.

    Returns:
        dict[str, str | int]: The Cortex info.

    """
    _info: dict[str, str | int] = {
        'id': AuthID.CORTEX_INFO,
        'jsonrpc': '2.0',
        'method': 'getCortexInfo',
    }

    return _info
