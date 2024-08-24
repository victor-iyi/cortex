from enum import IntEnum
from typing import Literal


class HeadsetID(IntEnum):
    """Headset request IDs."""

    QUERY_HEADSET = 1
    CONNECT = 2
    SUBSCRIBE = 6
    DISCONNECT = 10
    UNSUBSCRIBE = 24
    CONNECTION_TIMEOUT = 102
    DISCONNECTED_TIMEOUT = 103
    CONNECTED = 104
    CANNOT_WORK_WITH_BTLE = 112
    CANNOT_CONNECT_DISABLE_MOTION = 113


def query_headset() -> dict[str, str | int | dict[str, str]]:
    """Query the headset.

    Notes:
        You can query a specific headset by its id, or you can specify a wildcard
        for partial matching.

    Read More:
        [queryHeadsets](https://emotiv.gitbook.io/cortex-api/headset/queryheadsets)

    Returns:
        dict[str, str | int]: The headset query status.

    """
    _query: dict[str, str | int | dict[str, str]] = {
        'id': HeadsetID.QUERY_HEADSET,
        'jsonrpc': '2.0',
        'method': 'queryHeadsets',
        'params': {},
    }

    return _query


def make_connection(
    headset_id: str,
    *,
    connect: bool = False,
    disconnect: bool = False,
) -> dict[str, str | int | dict[str, str]]:
    """Connect or disconnect from the headset.

    Read More:
        [controlDevice](https://emotiv.gitbook.io/cortex-api/headset/controldevice)

    Args:
        headset_id (str): The headset ID.

    Keyword Args:
        connect (bool, optional): Connect to the headset.
        disconnect (bool, optional): Disconnect from the headset.

    Returns:
        dict[str, str | int, dict[str, str]]: The headset connection status.

    """
    assert connect ^ disconnect, 'Either connect or disconnect must be True.'

    _request: dict[str, str | int | dict[str, str]] = {
        'id': HeadsetID.CONNECT if connect else HeadsetID.DISCONNECT,
        'jsonrpc': '2.0',
        'method': 'controlDevice',
        'params': {
            'command': 'connect' if connect else 'disconnect',
            'headset': headset_id,
        },
    }

    return _request


def subscription(
    auth: str,
    session_id: str,
    streams: list[str],
    *,
    method: Literal['subscribe', 'unsubscribe'] = 'subscribe',
) -> dict[str, str | int | dict[str, str | list[str]]]:
    """Subscribe or unsubscribe from the headset.

    Read More:
        [subscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/subscribe)
        [unsubscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/unsubscribe)

    Args:
        auth (str): The Cortex authentication token.
        session_id (str): The session ID.
        streams (list[str]): The streams you want to subscribe or unsubscribe to.

    Keyword Args:
        method (Literal['subscribe', 'unsubscribe'], optional):
            The subscription method.

    Returns:
        dict[str, str | int, dict[str, str | list[str]]]: The subscription
            status request.

    """
    assert method in ['subscribe', 'unsubscribe'], 'method must be either "subscribe" or "unsubscribe".'

    _request: dict[str, str | int | dict[str, str | list[str]]] = {
        'id': HeadsetID.SUBSCRIBE if method == 'subscribe' else HeadsetID.UNSUBSCRIBE,
        'jsonrpc': '2.0',
        'method': method,
        'params': {
            'cortexToken': auth,
            'session': session_id,
            'streams': streams,
        },
    }

    return _request
