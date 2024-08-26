"""## [Headsets]

After you finish the [authentication] process, your application should
start headset scanning to search for EMOTIV headsets, using the method
[controlDevice] with "refresh" command, then use the method
[queryHeadsets] to get the discovered headsets.

If the headset is not connected to Cortex yet, then you must call
[controlDevice] with "connect" command.

[Headsets]:
https://emotiv.gitbook.io/cortex-api/headset

[authentication]: https://emotiv.gitbook.io/cortex-api/authentication

[controlDevice]:
https://emotiv.gitbook.io/cortex-api/headset/controldevice

[queryHeadsets]:
https://emotiv.gitbook.io/cortex-api/headset/queryheadsets

"""

# mypy: disable-error-code=assignment

from typing import Literal, Mapping, TypeAlias, TypedDict
from cortex.api.id import HeadsetID


class Setting(TypedDict, total=False):
    """Headset setting."""

    # In "EPOC" mode, the EEG resolution is 14 bits.
    # In "EPOCPLUS" mode, the EEG resolutions are 16 bits.
    mode: Literal['EPOC', 'EPOCPLUS']

    # The EEG sample rate, in hertz.
    # If the mode is "EPOC", then the EEG rate must be 128.
    # If the mode is "EPOCPLUS", then the EEG rate can be 128 or 256.
    eegRate: Literal[128, 256]

    # The motion sample rate, in hertz.
    # If the mode is "EPOC", then the motion rate must be 0.
    # If the mode is "EPOCPLUS", then the motion rate can be 0, 32, 64, or 128.
    memsRate: Literal[0, 32, 64, 128]


# Return type aliases.
ConnectHeadsetRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | Mapping[str, str]]]
QueryHeadsetRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str]]
UpdateHeadsetRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | Setting]]
UpdateCustomInfoRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str]]
SyncWithClockRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | float]]
SubscriptionRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | list[str]]]


def make_connection(
    command: Literal['connect', 'disconnect', 'refresh'],
    *,
    headset_id: str | None = None,
    mappings: dict[str, str] | None = None,
    connection_type: str | None = None,
) -> ConnectHeadsetRequest:
    """Connect, refresh, or disconnect from the headset.

    Read More:
        [controlDevice](https://emotiv.gitbook.io/cortex-api/headset/controldevice)

    Args:
        command (Literal['connect', 'disconnect', 'refresh']): The command.

    Keyword Args:
        headset_id (str, optional): The headset ID.
        mappings (dict[str, str], optional): The mappings.
        connection_type (str, optional): The connection type.

    Returns:
        ConnectHeadsetRequest: The headset connection status.

    """
    _params = {'command': command}

    if command in ('connect', 'refresh'):
        _id = HeadsetID.CONNECT
    elif command == 'disconnect':
        _id = HeadsetID.DISCONNECT
    else:
        raise ValueError('command must be either "connect", "disconnect", or "refresh".')

    if headset_id is not None:
        _params['headset'] = headset_id

    if mappings is not None:
        _params['mappings'] = mappings

    if connection_type is not None:
        _params['connectionType'] = connection_type

    _request = {
        'id': _id,
        'jsonrpc': '2.0',
        'method': 'controlDevice',
        'params': _params,
    }

    return _request


def query_headset(headset_id: str | None = None) -> QueryHeadsetRequest:
    """Query the headset.

    Notes:
        You can query a specific headset by its id, or you can specify a wildcard
        for partial matching.

    Read More:
        [queryHeadsets](https://emotiv.gitbook.io/cortex-api/headset/queryheadsets)

    Returns:
        QueryHeadsetRequest: The headset query status.

    """
    if headset_id is not None:
        _params = {'id': headset_id}
    else:
        _params = {}
    _query: dict[str, str | int | dict[str, str]] = {
        'id': HeadsetID.QUERY_HEADSET,
        'jsonrpc': '2.0',
        'method': 'queryHeadsets',
        'params': _params,
    }

    return _query


def update_headset(
    auth: str,
    headset_id: str,
    settings: Setting,
) -> UpdateHeadsetRequest:
    """Update the headset settings.

    Read More:
        [updateHeadset](https://emotiv.gitbook.io/cortex-api/headset/updateheadset)

    Args:
        auth (str): The Cortex authentication token.
        headset_id (str): The headset ID.
        settings (dict[str, str | int]): The settings to update.

    Returns:
        UpdateHeadsetRequest: The headset update status.

    """
    _request = {
        'id': HeadsetID.UPDATE_HEADSET,
        'jsonrpc': '2.0',
        'method': 'updateHeadset',
        'params': {
            'cortexToken': auth,
            'headsetId': headset_id,
            'setting': settings,
        },
    }

    return _request


def update_custom_info(
    auth: str,
    headset_id: str,
    headband_position: Literal['back', 'top'],
) -> UpdateCustomInfoRequest:
    """Update the headset custom information.

    Read More:
        [updateCustomInfo](https://emotiv.gitbook.io/cortex-api/headset/updatecustominfo)

    Args:
        auth (str): The Cortex authentication token.
        headset_id (str): The headset ID.
        headband_position (Literal['back', 'top']): The headband position.

    Returns:
        UpdateCustomInfoRequest: The headset custom information status.

    """
    _request = {
        'id': HeadsetID.UPDATE_CUSTOM_INFO,
        'jsonrpc': '2.0',
        'method': 'updateHeadsetCustomInfo',
        'params': {
            'cortexToken': auth,
            'headsetId': headset_id,
            'headbandPosition': headband_position,
        },
    }

    return _request


def sync_with_clock(
    headset_id: str,
    monotonic_time: float,
    system_time: float,
) -> SyncWithClockRequest:
    """Sync the headset with the system clock.

    Read More:
        [syncWithClock](https://emotiv.gitbook.io/cortex-api/headset/syncwithclock)

    Args:
        headset_id (str): The headset ID.
        monotonic_time (float): The monotonic time.
        system_time (float): The system time.

    Returns:
        SyncWithClockRequest: The headset sync status.

    """
    _request = {
        'id': HeadsetID.SYNC_WITH_CLOCK,
        'jsonrpc': '2.0',
        'method': 'syncWithHeadsetClock',
        'params': {
            'headset': headset_id,
            'monotonicTime': monotonic_time,
            'systemTime': system_time,
        },
    }

    return _request


def subscription(
    auth: str,
    session_id: str,
    streams: list[str],
    method: Literal['subscribe', 'unsubscribe'],
) -> SubscriptionRequest:
    """Subscribe or unsubscribe from the headset.

    Read More:
        [subscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/subscribe)
        [unsubscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/unsubscribe)

    Args:
        auth (str): The Cortex authentication token.
        session_id (str): The session ID.
        streams (list[str]): The streams you want to subscribe or unsubscribe to.
        method (Literal['subscribe', 'unsubscribe'], optional):
            The subscription method.

    Returns:
        SubscriptionRequest: The subscription status request.

    """
    assert method in ['subscribe', 'unsubscribe'], 'method must be either "subscribe" or "unsubscribe".'

    _request = {
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
