"""## [Sessions].

A session is an object that makes the link between your application and an
EMOTIV headset. When the user wants to work with a headset, your application
should create a session first.

Then you can:
    - subscribe to the [data stream] of the headset
    - create a [record] and add [markers]
    - use [BCI]

Your application can open only one session at a time with a given headset.
But it can open multiple sessions with multiple headsets.

[Sessions]: https://emotiv.gitbook.io/cortex-api/session
[data stream]: https://emotiv.gitbook.io/cortex-api/data-subscription
[record]: https://emotiv.gitbook.io/cortex-api/records
[markers]: https://emotiv.gitbook.io/cortex-api/markers
[BCI]: https://emotiv.gitbook.io/cortex-api/bci

"""

from typing import Literal

from cortex.api.id import SessionID
from cortex.api.types import BaseRequest


def create_session(auth: str, headset_id: str, status: Literal['open', 'active']) -> BaseRequest:
    """Either open a session or open and activate a session.

    Args:
        auth (str): The Cortex authentication token.
        headset_id (str): The headset ID.
        status (Literal['open', 'active']): The session status.
            'open' to just open the session,
            'activate' to open and activate the session.

    Read More:
        [createSession](https://emotiv.gitbook.io/cortex-api/session/createsession)

    Returns:
        BaseRequest: The session status.

    """
    if status not in ('open', 'active'):
        raise ValueError('status must be either "open" or "active".')

    _session = {
        'id': SessionID.CREATE,
        'jsonrpc': '2.0',
        'method': 'createSession',
        'params': {'cortexToken': auth, 'headset': headset_id, 'status': status},
    }

    return _session


def update_session(auth: str, session_id: str, status: Literal['active', 'close']) -> BaseRequest:
    """Update or close a session.

    Args:
        auth (str): The Cortex authentication token.
        session_id (str): The session ID.
        status (Literal['active', 'close']): The session status.
            'active' to activate a session,
            'close' to close a session.

    Read More:
        [updateSession](https://emotiv.gitbook.io/cortex-api/session/updatesession)

    Returns:
        BaseRequest: The session status.

    """
    if status not in ('active', 'close'):
        raise ValueError('status must be either "active" or "close".')

    _session = {
        'id': SessionID.UPDATE,
        'jsonrpc': '2.0',
        'method': 'updateSession',
        'params': {'cortexToken': auth, 'session': session_id, 'status': status},
    }

    return _session


def query_session(auth: str) -> BaseRequest:
    """Query the session.

    Args:
        auth (str): The Cortex authentication token.

    Read More:
        [querySession](https://emotiv.gitbook.io/cortex-api/session/querysessions)

    Returns:
        BaseRequest: The session status.

    """
    _session = {'id': SessionID.QUERY, 'jsonrpc': '2.0', 'method': 'querySession', 'params': {'cortexToken': auth}}

    return _session
