"""Mental command request functions.

This module provides functions to set or get the mental command action
sensitivity, get the active mental command action, map the profile name
to the corresponding mental command brain, and get the training
threshold for mental commands.

"""

from enum import IntEnum


class MentalCommand(IntEnum):
    """Mental command request IDs."""

    SENSITIVITY_REQUEST = 15
    GET_ACTIVE_ACTION = 16
    BRAIN_MAP = 17
    TRAINING_THRESHOLD = 18
    SET_ACTIVE_ACTION = 19


def action_sensitivity(
    auth: str,
    profile_name: str,
    session_id: str | None = None,
    values: list[int] | None = None,
) -> dict[str, str | int | dict[str, str | list[int]]]:
    """Set or get the mental command action sensitivity.

    Notes:
        If `session_id` and `values` are provided, the sensitivity status is 'set'.
        Otherwise, the sensitivity status is 'get'.

    Args:
        profile_name (str): The name of the profile.
        auth (str): The Cortex authentication token.
        session_id (str, optional): The session ID.
        values (list[int], optional): The sensitivity values.

    Returns:
        dict[str, str | int | dict[str, str | list[int]]]: The mental command
            action sensitivity.

    """
    _params: dict[str, str | list[int]] = {
        'cortexToken': auth,
        'profile': profile_name,
    }
    if session_id is not None and values is not None:
        _params['status'] = 'set'
        _params['session'] = session_id
        _params['values'] = values
    else:
        _params['status'] = 'get'

    sensitivity: dict[str, str | int | dict[str, str | list[int]]] = {
        'id': MentalCommand.SENSITIVITY_REQUEST,
        'jsonrpc': '2.0',
        'method': 'mentalCommandActionSensitivity',
        'params': _params,
    }

    return sensitivity


def active_action(
    auth: str,
    profile_name: str | None = None,
    session_id: str | None = None,
    actions: list[str] | None = None,
) -> dict[str, str | int | dict[str, str | list[str]]]:
    """Set or get the active mental command action.

    Notes:
        If `profile_name`, `session_id`, and `actions` are provided,
        the status is 'set'.  Otherwise, the status is 'get'.

    Args:
        auth (str): The Cortex authentication token.
        profile_name (str, optional): The name of the profile.
        session_id (str, optional): The session ID.
        actions (list[str], optional): The active mental command actions.

    Returns:
        dict[str, str | int | dict[str, str | list[str]]]:
            The active mental command action.

    """
    _params: dict[str, str | list[str]] = {
        'cortexToken': auth,
    }
    if session_id is not None and actions is not None:
        _id = MentalCommand.SET_ACTIVE_ACTION
        _params['status'] = 'set'
        _params['session'] = session_id
        _params['actions'] = actions
    elif profile_name is not None:
        _id = MentalCommand.GET_ACTIVE_ACTION
        _params['status'] = 'get'
        _params['profile_name'] = profile_name
    else:
        raise ValueError('profile_name or session_id and actions must be provided.')

    action: dict[str, str | int | dict[str, str | list[str]]] = {
        'id': _id,
        'jsonrpc': '2.0',
        'method': 'mentalCommandActiveAction',
        'params': _params,
    }

    return action


def brain_map(
    auth: str,
    session_id: str,
    profile_name: str,
) -> dict[str, str | int | dict[str, str]]:
    """Map the profile name to the corresponding mental command brain.

    Args:
        auth (str): The Cortex authentication token.
        session_id (str): The session
        profile_name (str): The name of the profile.

    Returns:
        dict[str, str | int | dict[str, str]]: The mental command brain map.

    """
    _brain_map: dict[str, int | str | dict[str, str]] = {
        'id': MentalCommand.BRAIN_MAP,
        'jsonrpc': '2.0',
        'method': 'mentalCommandBrainMap',
        'params': {
            'cortexToken': auth,
            'profile': profile_name,
            'session': session_id,
        },
    }
    return _brain_map


def training_threshold(
    auth: str,
    session_id: str,
    profile_name: str,
) -> dict[str, int | str | dict[str, str]]:
    """Get the training threshold for mental commands.

    Args:
        auth (str): The Cortex authentication token.
        session_id (str): The session ID.
        profile_name (str): The name of the profile.

    Returns:
        dict[str, str | int | dict[str, str]]:
            The training threshold for mental commands.

    """
    threshold: dict[str, int | str | dict[str, str]] = {
        'id': MentalCommand.TRAINING_THRESHOLD,
        'jsonrpc': '2.0',
        'method': 'mentalCommandTrainingThreshold',
        'params': {
            'cortexToken': auth,
            'profile': profile_name,
            'session': session_id,
        },
    }

    return threshold
