"""Mental command request functions.

This module provides functions to set or get the mental command action sensitivity, get the active mental command
action, map the profile name to the corresponding mental command brain, and get the training threshold for mental
commands.

"""

# mypy: disable-error-code=assignment

from typing import Literal

from cortex.api.id import MentalCommandID
from cortex.api.types import BaseRequest, MentalCommandActionRequest


def active_action(
    auth: str,
    status: Literal['set', 'get'],
    *,
    profile_name: str | None = None,
    session_id: str | None = None,
    actions: list[str] | None = None,
) -> MentalCommandActionRequest:
    """Set or get the active mental command action.

    Notes:
        If `profile_name`, `session_id`, and `actions` are provided,
        the status is 'set'.  Otherwise, the status is 'get'.

    Args:
        auth (str): The Cortex authentication token.
        status (Literal['set', 'get']): The status. Whether to set or get the active action.

    Keyword Args:
        profile_name (str, optional): The name of the profile.
        session_id (str, optional): The session ID.
        actions (list[str], optional): If the status is "set", this parameter
            is the list of active actions. You can't have more than 4 actions.
            This doesn't include "neutral".

    Read More:
        [mentalCommandActiveAction](https://emotiv.gitbook.io/cortex-api/advanced-bci/mentalcommandactiveaction)

    Returns:
        MentalCommandActionRequest: The active mental command action.

    """
    assert status in ['set', 'get'], 'status must be either "set" or "get".'

    _params = {'cortexToken': auth, 'status': status}

    # Either profile_name or session_id must be provided, not both at the same time.
    if profile_name is not None and session_id is None:
        _params['profile'] = profile_name
    elif session_id is not None and profile_name is None:
        _params['session'] = session_id
    else:
        raise ValueError('Either profile_name or session_id must be provided, not both at the same time.')

    if actions is not None and status == 'set':
        if len(actions) > 4:
            raise ValueError('You can have at most 4 actions.')
        _params['actions'] = actions

    _action = {
        'id': MentalCommandID.SET_ACTIVE_ACTION if status == 'set' else MentalCommandID.GET_ACTIVE_ACTION,
        'jsonrpc': '2.0',
        'method': 'mentalCommandActiveAction',
        'params': _params,
    }

    return _action


def brain_map(auth: str, *, session_id: str | None = None, profile_name: str | None = None) -> BaseRequest:
    """Map the profile name to the corresponding mental command brain.

    Args:
        auth (str): The Cortex authentication token.

    Keyword Args:
        session_id (str, optional): The session
        profile_name (str, optional): The name of the profile.

    Read More:
        [mentalCommandBrainMap](https://emotiv.gitbook.io/cortex-api/advanced-bci/mentalcommandbrainmap)

    Returns:
        BaseRequest: The mental command brain map.

    """
    _params = {'cortexToken': auth}

    # Either profile_name or session_id must be provided, not both at the same time.
    if profile_name is not None and session_id is None:
        _params['profile'] = profile_name
    elif session_id is not None and profile_name is None:
        _params['session'] = session_id
    else:
        raise ValueError('Either profile_name or session_id must be provided, not both at the same time.')

    _brain_map = {
        'id': MentalCommandID.BRAIN_MAP,
        'jsonrpc': '2.0',
        'method': 'mentalCommandBrainMap',
        'params': _params,
    }
    return _brain_map


def get_skill_rating(
    auth: str, *, profile_name: str | None = None, session_id: str | None = None, action: str | None = None
) -> BaseRequest:
    """Get the skill rating of the mental command action.

    Args:
        auth (str): The Cortex authentication token.

    Keyword Args:
        profile_name (str, optional): The name of the profile.
        session_id (str, optional): The session ID.
        action (str, optional): The mental command action.

    Read More:
        [mentalCommandGetSkillRating](https://emotiv.gitbook.io/cortex-api/advanced-bci/mentalcommandgetskillrating)

    Returns:
        BaseRequest: The skill rating of the mental command action.

    """
    _params = {'cortexToken': auth}

    # Either profile_name or session_id must be provided, not both at the same time.
    if profile_name is not None and session_id is None:
        _params['profile'] = profile_name
    elif session_id is not None and profile_name is None:
        _params['session'] = session_id
    else:
        raise ValueError('Either profile_name or session_id must be provided, not both at the same time.')

    if action is not None:
        _params['action'] = action

    skill_rating = {
        'id': MentalCommandID.SKILL_RATING,
        'jsonrpc': '2.0',
        'method': 'mentalCommandGetSkillRating',
        'params': _params,
    }

    return skill_rating


def training_threshold(auth: str, *, profile_name: str | None = None, session_id: str | None = None) -> BaseRequest:
    """Get the training threshold for mental commands.

    Args:
        auth (str): The Cortex authentication token.

    Keyword Args:
        profile_name (str): The name of the profile.
        session_id (str): The session ID.

    Read More:
        [mentalCommandTrainingThreshold](https://emotiv.gitbook.io/cortex-api/advanced-bci/mentalcommandtrainingthreshold)

    Returns:
        dict[str, str | int | dict[str, str]]:
            The training threshold for mental commands.

    """
    _params = {'cortexToken': auth}

    # Either profile_name or session_id must be provided, not both at the same time.
    if profile_name is not None and session_id is None:
        _params['profile'] = profile_name
    elif session_id is not None and profile_name is None:
        _params['session'] = session_id
    else:
        raise ValueError('Either profile_name or session_id must be provided, not both at the same time.')

    threshold = {
        'id': MentalCommandID.TRAINING_THRESHOLD,
        'jsonrpc': '2.0',
        'method': 'mentalCommandTrainingThreshold',
        'params': _params,
    }

    return threshold


def action_sensitivity(
    auth: str,
    status: Literal['set', 'get'],
    *,
    profile_name: str | None = None,
    session_id: str | None = None,
    values: list[int] | None = None,
) -> MentalCommandActionRequest:
    """Set or get the mental command action sensitivity.

    Notes:
        If `session_id` and `values` are provided, the sensitivity status is 'set'.
        Otherwise, the sensitivity status is 'get'.

    Args:
        auth (str): The Cortex authentication token.
        status (Literal['set', 'get']): The sensitivity status.

    Keyword Args:
        profile_name (str): The name of the profile.
        session_id (str, optional): The session ID.
        values (list[int], optional): If the status is "set", this parameter is
            the new sensitivities. Each value must be between 1 and 10.
            Bigger number indicates higher sensitivity.

    Read More:
        [mentalCommandActionSensitivity](https://emotiv.gitbook.io/cortex-api/advanced-bci/mentalcommandactionsensitivity)

    Returns:
        MentalCommandActionRequest: The mental command action sensitivity.

    """
    assert status in ['set', 'get'], 'status must be either "set" or "get".'

    _params = {'cortexToken': auth, 'status': status}

    # Either profile_name or session_id must be provided, not both at the same time.
    if profile_name is not None and session_id is None:
        _params['profile'] = profile_name
    elif session_id is not None and profile_name is None:
        _params['session'] = session_id
    else:
        raise ValueError('Either profile_name or session_id must be provided, not both at the same time.')

    if values is not None and status == 'set':
        if all(1 <= value <= 10 for value in values):
            _params['values'] = values
        else:
            raise ValueError('values must be between 1 and 10.')

    sensitivity = {
        'id': MentalCommandID.ACTION_SENSITIVITY,
        'jsonrpc': '2.0',
        'method': 'mentalCommandActionSensitivity',
        'params': _params,
    }

    return sensitivity
