"""## [Sessions]

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

from typing import Literal, Mapping, TypeAlias

from cortex.api.id import SessionID

# Return type aliases.
SessionRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str]]


def create(
    auth: str,
    headset_id: str,
    status: Literal['open', 'active'],
) -> SessionRequest:
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
        SessionRequest: The session status.

    """
    assert status in ['open', 'active'], 'status must be either "open" or "active".'

    _session = {
        'id': SessionID.CREATE,
        'jsonrpc': '2.0',
        'method': 'createSession',
        'params': {
            'cortexToken': auth,
            'headset': headset_id,
            'status': status,
        },
    }

    return _session


def update(
    auth: str,
    session_id: str,
    status: Literal['active', 'close'],
) -> SessionRequest:
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
        SessionRequest: The session status.

    """
    assert status in ['active', 'close'], 'status must be either "active" or "close".'

    _session = {
        'id': SessionID.UPDATE,
        'jsonrpc': '2.0',
        'method': 'updateSession',
        'params': {
            'cortexToken': auth,
            'session': session_id,
            'status': status,
        },
    }

    return _session


def query(auth: str) -> SessionRequest:
    """Query the session.

    Args:
        auth (str): The Cortex authentication token.

    Read More:
        [querySession](https://emotiv.gitbook.io/cortex-api/session/querysessions)

    Returns:
        SessionRequest: The session status.

    """
    _session = {
        'id': SessionID.QUERY,
        'jsonrpc': '2.0',
        'method': 'querySession',
        'params': {
            'cortexToken': auth,
        },
    }

    return _session


# def session(
#     auth: str,
#     *,
#     status: Literal['active', 'open', 'close'],
#     headset_id: str | None = None,
#     session_id: str | None = None,
# ) -> SessionRequest:
#     """Create or close a session.
#
#     Args:
#         auth (str): The Cortex authentication token.
#
#     Keyword Args:
#         headset_id (str, optional): The headset ID.
#         session_id (str, optional): The session ID.
#         status (Literal['active', 'close'], optional): The session status.
#
#     Returns:
#         SessionRequest: The session status.
#
#     """
#     assert status in ['active', 'close'], 'status must be either "active" or "close".'
#
#     _params = {
#         'cortexToken': auth,
#     }
#     if headset_id is not None and status == 'active':
#         _method = 'createSession'
#         _params['headset'] = headset_id
#     elif session_id is not None and status == 'close':
#         _method = 'updateSession'
#         _params['session'] = session_id
#     else:
#         raise ValueError(
#             'headset_id must be provided for active session, session_id must be provided for close session.'
#         )
#
#     _params['status'] = status
#
#     _session = {
#         'id': SessionID.CREATE_SESSION,
#         'jsonrpc': '2.0',
#         'method': _method,
#         'params': _params,
#     }
#
#     return _session
