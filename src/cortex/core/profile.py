from enum import IntEnum
from typing import Literal


class ProfileID(IntEnum):
    """Profile request IDs."""

    SETUP = 7
    QUERY = 8
    CURRENT_PROFILE = 21


def query_profile(auth: str) -> dict[str, str | int | dict[str, str]]:
    """Query the profile.

    Read More:
        [queryProfile](https://emotiv.gitbook.io/cortex-api/profile/queryprofile)

    Returns:
        dict[str, str | int | dict[str, str]]: The profile query status.

    """
    _query: dict[str, str | int | dict[str, str]] = {
        'id': ProfileID.QUERY,
        'jsonrpc': '2.0',
        'method': 'queryProfile',
        'params': {
            'cortexToken': auth,
        },
    }

    return _query


def current_profile(
    auth: str,
    headset_id: str,
) -> dict[str, str | int | dict[str, str]]:
    """Get the current profile.

    Args:
        auth (str): The Cortex authentication token.
        headset_id (str): The headset ID.

    Returns:
        dict[str, str | int | dict[str, str]]: The current profile status.

    """
    _profile: dict[str, str | int | dict[str, str]] = {
        'id': ProfileID.CURRENT_PROFILE,
        'jsonrpc': '2.0',
        'method': 'getCurrentProfile',
        'params': {
            'cortexToken': auth,
            'headset': headset_id,
        },
    }

    return _profile


def setup_profile(
    auth: str,
    headset_id: str,
    profile_name: str,
    *,
    status: Literal['create', 'load', 'unload', 'save', 'rename', 'delete'],
) -> dict[str, str | int | dict[str, str]]:
    """Setup a profile.

    Args:
        auth (str): The Cortex authentication token.
        headset_id (str): The headset ID.
        profile_name (str): The profile name.

    Keyword Args:
        status (Literal['create', 'load', 'unload', 'save', 'rename', 'delete']):
            The profile status.

    Returns:
        dict[str, str | int | dict[str, str]]: The profile status.

    """
    assert status in [
        'create',
        'load',
        'unload',
        'save',
        'rename',
        'delete',
    ], 'status must be either "create", "load", "unload", "save", "rename", or "delete".'

    _params: dict[str, str] = {
        'cortexToken': auth,
        'headset': headset_id,
        'profile': profile_name,
        'status': status,
    }

    _profile: dict[str, str | int | dict[str, str]] = {
        'id': ProfileID.SETUP,
        'jsonrpc': '2.0',
        'method': 'setupProfile',
        'params': _params,
    }

    return _profile
