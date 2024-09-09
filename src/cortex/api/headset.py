"""## Headsets_.

After you finish the authentication_ process, your application should start headset scanning to search for EMOTIV
headsets, using the method controlDevice_ with "refresh" command, then use the method queryHeadsets_ to get the
discovered headsets.

If the headset is not connected to Cortex yet, then you must call controlDevice_ with "connect" command.

.. _Headsets: https://emotiv.gitbook.io/cortex-api/headset
.. _authentication: https://emotiv.gitbook.io/cortex-api/authentication
.. _controlDevice: https://emotiv.gitbook.io/cortex-api/headset/controldevice
.. _queryHeadsets: https://emotiv.gitbook.io/cortex-api/headset/queryheadsets

"""

# mypy: disable-error-code=assignment

from typing import Literal

from cortex.api.id import HeadsetID
from cortex.api.types import (
    BaseRequest,
    ConnectHeadsetRequest,
    ConnectionType,
    Setting,
    SubscriptionRequest,
    SyncWithClockRequest,
    UpdateHeadsetRequest,
)


def make_connection(
    command: Literal['connect', 'disconnect', 'refresh'],
    *,
    headset_id: str | None = None,
    mappings: dict[str, str] | None = None,
    connection_type: ConnectionType | None = None,
) -> ConnectHeadsetRequest:
    """Connect, refresh, or disconnect from the headset.

    Read More:
        [controlDevice](https://emotiv.gitbook.io/cortex-api/headset/controldevice)

    Args:
        command (Literal['connect', 'disconnect', 'refresh']): The command.

    Keyword Args:
        headset_id (str, optional): The headset ID.
        mappings (dict[str, str], optional): The mappings (Only if you want to connect Epoc Flex headset).
        connection_type (ConnectionType, optinoal): The connection type.
            Connection type can be one of "bluetooth", "dongle" or "usb cable".

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

    if headset_id is not None and command != 'refresh':
        _params['headset'] = headset_id

    # Provide mappings only if headset is EPOC FLEX and command is connect.
    if (
        headset_id is not None
        and headset_id.upper().startswith('EPOCFLEX')
        and mappings is not None
        and command == 'connect'
    ):
        _params['mappings'] = mappings

    # Omit connection_type if command is 'refresh'.
    if connection_type is not None and command != 'refresh':
        _params['connectionType'] = connection_type

    _request = {'id': _id, 'jsonrpc': '2.0', 'method': 'controlDevice', 'params': _params}

    return _request


def query_headset(headset_id: str | None = None, *, include_flex_mappings: bool = False) -> BaseRequest:
    """Query the headset.

    Notes:
        You can query a specific headset by its id, or you can specify a wildcard
        for partial matching.

    Read More:
        [queryHeadsets](https://emotiv.gitbook.io/cortex-api/headset/queryheadsets)

    Args:
        headset_id (str, optional): The headset ID or wildcard.

    Keyword Args:
        include_flex_mappings (bool, optional): Include the mappings of EPOCFLEX headset.

    Returns:
        BaseRequest: The headset query status.

    """
    _params = {}
    if headset_id is not None:
        _params['id'] = headset_id

    if include_flex_mappings:
        _params['includeFlexMappings'] = include_flex_mappings

    _query = {'id': HeadsetID.QUERY_HEADSET, 'jsonrpc': '2.0', 'method': 'queryHeadsets', 'params': _params}

    return _query


def update_headset(auth: str, headset_id: str, settings: Setting) -> UpdateHeadsetRequest:
    """Update the headset settings.

    Read More:
        [updateHeadset](https://emotiv.gitbook.io/cortex-api/headset/updateheadset)

    Args:
        auth (str): The Cortex authentication token.
        headset_id (str): The headset ID.
        settings (Setting): The settings to update.

    Returns:
        UpdateHeadsetRequest: The headset update status.

    """
    if settings['mode'] == 'EPOC' and settings['eegRate'] != 128:
        raise ValueError('EPOC headset only supports 128Hz EEG rate.')

    if settings['mode'] == 'EPOC' and settings['memsRate'] != 0:
        raise ValueError('EPOC headset only supports 0Hz MEMS rate.')

    if settings['mode'] == 'EPOCPLUS' and settings['eegRate'] not in (128, 256):
        raise ValueError('EPOCPLUS headset only supports 128Hz or 256Hz EEG rate.')

    if settings['mode'] == 'EPOCPLUS' and settings['memsRate'] not in (0, 32, 64, 128):
        raise ValueError('EPOCPLUS headset only supports 0Hz, 32Hz, 64Hz, or 128Hz MEMS rate.')

    _request = {
        'id': HeadsetID.UPDATE_HEADSET,
        'jsonrpc': '2.0',
        'method': 'updateHeadset',
        'params': {'cortexToken': auth, 'headset': headset_id, 'setting': settings},
    }

    return _request


def update_custom_info(auth: str, headset_id: str, headband_position: Literal['back', 'top']) -> BaseRequest:
    """Update the headset custom information.

    Read More:
        [updateCustomInfo](https://emotiv.gitbook.io/cortex-api/headset/updatecustominfo)

    Args:
        auth (str): The Cortex authentication token.
        headset_id (str): The headset ID.
        headband_position (Literal['back', 'top']): The headband position.

    Returns:
        BaseRequest: The headset custom information status.

    """
    if headband_position not in ('back', 'top'):
        raise ValueError('headband_position must be either "back" or "top".')

    _request = {
        'id': HeadsetID.UPDATE_CUSTOM_INFO,
        'jsonrpc': '2.0',
        'method': 'updateHeadsetCustomInfo',
        'params': {'cortexToken': auth, 'headsetId': headset_id, 'headbandPosition': headband_position},
    }

    return _request


def sync_with_clock(headset_id: str, monotonic_time: float, system_time: float) -> SyncWithClockRequest:
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
        'params': {'headset': headset_id, 'monotonicTime': monotonic_time, 'systemTime': system_time},
    }

    return _request


def subscription(
    auth: str, session_id: str, streams: list[str], method: Literal['subscribe', 'unsubscribe']
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
        'params': {'cortexToken': auth, 'session': session_id, 'streams': streams},
    }

    return _request
