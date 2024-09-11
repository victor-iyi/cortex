"""Facial Expression API."""

from typing import Literal

from cortex.api.id import FacialExpressionID
from cortex.api.types import FacialExpressionRequest


def signature_type(
    auth: str,
    status: Literal['set', 'get'],
    *,
    profile_name: str | None = None,
    session_id: str | None = None,
    signature: Literal['universal', 'trained'] | None = None,
) -> FacialExpressionRequest:
    """Set or get the facial expression signature type.

    Args:
        auth (str): The Cortex authentication token.
        status (Literal['set', 'get']): The status.

    Keyword Args:
        profile_name (str, optional): The profile name.
        session_id (str, optional): The session ID.
        signature (Literal['universal', 'trained'], optional): The signature type.

    Read More:
        [facialExpressionSignatureType](https://emotiv.gitbook.io/cortex-api/advanced-bci/facialexpressionsignaturetype)

    Returns:
        FacialExpressionRequest: The facial expression signature type.

    """
    if status not in ('set', 'get'):
        raise ValueError('status must be either "set" or "get".')

    _params = {'cortexToken': auth, 'status': status}

    # Either profile_name or session_id must be provided, not both at the same time.
    if profile_name is not None and session_id is None:
        _params['profile'] = profile_name
    elif session_id is not None and profile_name is None:
        _params['session'] = session_id
    else:
        raise AttributeError('Either profile_name or session_id must be provided, not both at the same time.')

    if signature is not None and status == 'set':
        if signature not in {'universal', 'trained'}:
            raise ValueError('signature must be either "universal" or "trained".')
        _params['signature'] = signature
    else:
        if status == 'set':
            raise AttributeError('signature must be provided when status is "set".')

    _signature = {
        'id': FacialExpressionID.SIGNATURE_TYPE,
        'jsonrpc': '2.0',
        'method': 'facialExpressionSignatureType',
        'params': _params,
    }

    return _signature


def threshold(
    auth: str,
    status: Literal['set', 'get'],
    action: str,
    *,
    profile_name: str | None = None,
    session_id: str | None = None,
    value: int | None = None,
) -> FacialExpressionRequest:
    """Set or get the facial expression action threshold for a specific profile.

    Notes:
        Actions with a low threshold are less likely to be detected.
        Actions with a high threshold will be detected more often.

    Args:
        auth (str): The Cortex authentication token.
        status (Literal['set', 'get']): The status.
        action(str): You get or set threshold for this action.

    Keyword Args:
        profile_name (str, optional): The profile name.
        session_id (str, optional): The session ID.
        value(int, optional):  If the status is "set", this parameter must be
            between 0 and 1000. This will be the new threshold for the action.

    Read More:
        [facialExpressionThreshold](https://emotiv.gitbook.io/cortex-api/advanced-bci/facialexpressionthreshold)

    Returns:
        FacialExpressionRequest: The facial expression threshold.

    """
    if status not in ('set', 'get'):
        raise ValueError('status must be either "set" or "get".')

    _params = {'cortexToken': auth, 'status': status, 'action': action}

    # Either profile_name or session_id must be provided, not both at the same time.
    if profile_name is not None and session_id is None:
        _params['profile'] = profile_name
    elif session_id is not None and profile_name is None:
        _params['session'] = session_id
    else:
        raise AttributeError('Either profile_name or session_id must be provided, not both at the same time.')

    if value is not None and status == 'set':
        if not 0 <= value <= 1000:
            raise ValueError('value must be between 0 and 1000.')
        _params['value'] = value  # type: ignore[assignment]
    else:
        if status == 'set':
            raise AttributeError('value must be provided when status is "set".')

    _threshold = {
        'id': FacialExpressionID.THRESHOLD,
        'jsonrpc': '2.0',
        'method': 'facialExpressionThreshold',
        'params': _params,
    }

    return _threshold
