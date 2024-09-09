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
    signature: Literal['set', 'universal', 'trained'] | None = None,
) -> FacialExpressionRequest:
    """Set or get the facial expression signature type.

    Args:
        auth (str): The Cortex authentication token.
        status (Literal['set', 'get']): The status.

    Keyword Args:
        profile_name (str, optional): The profile name.
        session_id (str, optional): The session ID.
        signature (Literal['set', 'universal', 'trained'], optional): The signature type.

    Read More:
        [facialExpressionSignatureType](https://emotiv.gitbook.io/cortex-api/advanced-bci/facialexpressionsignaturetype)

    Returns:
        FacialExpressionRequest: The facial expression signature type.

    """
    assert status in {'set', 'get'}, 'status must be either "set" or "get".'

    _params = {'cortexToken': auth, 'status': status}

    # Either profile_name or session_id must be provided, not both at the same time.
    if profile_name is not None and session_id is None:
        _params['profile'] = profile_name
    elif session_id is not None and profile_name is None:
        _params['session'] = session_id
    else:
        raise ValueError('Either profile_name or session_id must be provided, not both at the same time.')

    if signature is not None:
        assert signature in {
            'set',
            'universal',
            'trained',
        }, 'signature must be either "set", "universal", or "trained".'
        _params['signature'] = signature

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
    assert status in ['set', 'get'], 'status must be either "set" or "get".'

    # Either profile_name or session_id must be provided, not both at the same time.
    assert (
        profile_name is not None and session_id is None or profile_name is None and session_id is not None
    ), 'Either profile_name or session_id must be provided, not both at the same time.'

    _params = {'cortexToken': auth, 'status': status, 'action': action}

    if profile_name is not None:
        _params['profile'] = profile_name
    elif session_id is not None:
        _params['session'] = session_id

    if value is not None and status == 'set':
        if not 0 <= value <= 1000:
            raise ValueError('value must be between 0 and 1000.')
        _params['value'] = value  # type: ignore[assignment]

    _threshold = {
        'id': FacialExpressionID.THRESHOLD,
        'jsonrpc': '2.0',
        'method': 'facialExpressionThreshold',
        'params': _params,
    }

    return _threshold
