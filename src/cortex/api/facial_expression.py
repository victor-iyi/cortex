from typing import Literal

from cortex.api.id import FacialExpressionID


def signature_type(
    auth: str,
    status: Literal['set', 'get'],
    *,
    profile_name: str | None = None,
    session_id: str | None = None,
    signature: Literal['set', 'universal', 'trained'] | None = None,
) -> dict[str, str | int | dict[str, str]]:
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
        dict[str, str | int | dict[str, str]]: The facial expression signature type.

    """

    assert status in ['set', 'get'], 'status must be either "set" or "get".'

    _params: dict[str, str] = {
        'cortexToken': auth,
        'status': status,
    }
    if profile_name is not None:
        _params['profile'] = profile_name

    if session_id is not None:
        _params['session'] = session_id

    if signature is not None:
        assert signature in [
            'set',
            'universal',
            'trained',
        ], 'signature must be either "set", "universal", or "trained".'
        _params['signature'] = signature

    _signature: dict[str, str | int | dict[str, str]] = {
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
) -> dict[str, str | int | dict[str, str | int]]:
    """Set or get the facial expression action threshold for a specific
    profile.

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
        dict[str, str | int | dict[str, str]]: The facial expression threshold.

    """

    assert status in ['set', 'get'], 'status must be either "set" or "get".'

    _params: dict[str, str | int] = {
        'cortexToken': auth,
        'status': status,
        'action': action,
    }
    if profile_name is not None:
        _params['profile'] = profile_name

    if session_id is not None:
        _params['session'] = session_id

    if value is not None and status == 'set':
        assert 0 <= value <= 1000, 'value must be between 0 and 1000.'
        _params['value'] = value

    _threshold: dict[str, str | int | dict[str, str | int]] = {
        'id': FacialExpressionID.THRESHOLD,
        'jsonrpc': '2.0',
        'method': 'facialExpressionThreshold',
        'params': _params,
    }

    return _threshold
