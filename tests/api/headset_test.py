"""Tests for the headset module."""

import pytest
import time

from collections.abc import Callable
from typing import Any, Final, TypeAlias

from cortex.api.headset import (
    make_connection,
    query_headset,
    update_headset,
    update_custom_info,
    sync_with_clock,
    subscription,
)
from cortex.api.types import Setting
from cortex.api.id import HeadsetID


# Constants
AUTH_TOKEN: Final[str] = 'xxx'
SESSION_ID: Final[str] = 'f3a35fd0-9163-4cc4-ab30-4ed224369f91'
HEADSET_ID: Final[str] = 'INSIGHT-12341234'
EPOC_FLEX_ID: Final[str] = 'EPOCFLEX-1234123'
MAPPINGS: dict[str, str] = {'CMS': 'F3', 'DRL': 'F5', 'LA': 'AF3', 'LB': 'AF7', 'RA': 'P8'}

# Type aliases
APIRequest: TypeAlias = Callable[..., dict[str, Any]]


def test_connect_headset(api_request: APIRequest) -> None:
    """Test connecting to a headset."""
    assert make_connection('connect') == api_request(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'connect'}
    )

    assert make_connection('connect', headset_id=EPOC_FLEX_ID) == api_request(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'connect', 'headset': EPOC_FLEX_ID}
    )
    assert make_connection('connect', headset_id=EPOC_FLEX_ID, mappings=MAPPINGS) == api_request(
        id=HeadsetID.CONNECT,
        method='controlDevice',
        params={'command': 'connect', 'headset': EPOC_FLEX_ID, 'mappings': MAPPINGS},
    )
    assert make_connection(
        'connect', headset_id=EPOC_FLEX_ID, mappings=MAPPINGS, connection_type='bluetooth'
    ) == api_request(
        id=HeadsetID.CONNECT,
        method='controlDevice',
        params={'command': 'connect', 'headset': EPOC_FLEX_ID, 'mappings': MAPPINGS, 'connectionType': 'bluetooth'},
    )

    assert make_connection('connect', headset_id=HEADSET_ID) == api_request(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'connect', 'headset': HEADSET_ID}
    )
    assert make_connection('connect', headset_id=HEADSET_ID, mappings=MAPPINGS) == api_request(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'connect', 'headset': HEADSET_ID}
    )

    assert make_connection('connect', connection_type='dongle') == api_request(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'connect', 'connectionType': 'dongle'}
    )

    assert make_connection(
        'connect', headset_id=HEADSET_ID, mappings=MAPPINGS, connection_type='usb cable'
    ) == api_request(
        id=HeadsetID.CONNECT,
        method='controlDevice',
        params={'command': 'connect', 'headset': HEADSET_ID, 'connectionType': 'usb cable'},
    )

    with pytest.raises(ValueError, match='command must be either "connect", "disconnect", or "refresh".'):
        make_connection('invalid')


def test_refresh_headset(api_request: APIRequest) -> None:
    """Test refreshing a headset."""
    assert make_connection('refresh') == api_request(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'}
    )
    assert make_connection('refresh', headset_id=HEADSET_ID) == api_request(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'}
    )

    # Provide mappings only if headset is EPOC FLEX and command is connect.
    assert make_connection('refresh', headset_id=HEADSET_ID, mappings=MAPPINGS) == api_request(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'}
    )
    assert make_connection('refresh', headset_id=EPOC_FLEX_ID, mappings=MAPPINGS) == api_request(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'}
    )

    # Omit connection_type if command is 'refresh'.
    assert make_connection('refresh', connection_type='dongle') == api_request(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'}
    )
    assert make_connection(
        'refresh', headset_id=HEADSET_ID, mappings=MAPPINGS, connection_type='bluetooth'
    ) == api_request(id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'})

    assert make_connection(
        'refresh', headset_id=EPOC_FLEX_ID, mappings=MAPPINGS, connection_type='dongle'
    ) == api_request(id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'})

    with pytest.raises(ValueError, match='command must be either "connect", "disconnect", or "refresh".'):
        make_connection('invalid')


def test_disconnect_headset(api_request: APIRequest) -> None:
    """Test disconnecting to a headset."""
    assert make_connection('disconnect') == api_request(
        id=HeadsetID.DISCONNECT, method='controlDevice', params={'command': 'disconnect'}
    )

    assert make_connection('disconnect', headset_id=EPOC_FLEX_ID) == api_request(
        id=HeadsetID.DISCONNECT, method='controlDevice', params={'command': 'disconnect', 'headset': EPOC_FLEX_ID}
    )
    assert make_connection('disconnect', headset_id=EPOC_FLEX_ID, mappings=MAPPINGS) == api_request(
        id=HeadsetID.DISCONNECT, method='controlDevice', params={'command': 'disconnect', 'headset': EPOC_FLEX_ID}
    )
    assert make_connection(
        'disconnect', headset_id=EPOC_FLEX_ID, mappings=MAPPINGS, connection_type='bluetooth'
    ) == api_request(
        id=HeadsetID.DISCONNECT,
        method='controlDevice',
        params={'command': 'disconnect', 'headset': EPOC_FLEX_ID, 'connectionType': 'bluetooth'},
    )

    assert make_connection('disconnect', headset_id=HEADSET_ID) == api_request(
        id=HeadsetID.DISCONNECT, method='controlDevice', params={'command': 'disconnect', 'headset': HEADSET_ID}
    )
    assert make_connection('disconnect', headset_id=HEADSET_ID, mappings=MAPPINGS) == api_request(
        id=HeadsetID.DISCONNECT, method='controlDevice', params={'command': 'disconnect', 'headset': HEADSET_ID}
    )

    assert make_connection('disconnect', connection_type='dongle') == api_request(
        id=HeadsetID.DISCONNECT, method='controlDevice', params={'command': 'disconnect', 'connectionType': 'dongle'}
    )

    assert make_connection(
        'disconnect', headset_id=HEADSET_ID, mappings=MAPPINGS, connection_type='usb cable'
    ) == api_request(
        id=HeadsetID.DISCONNECT,
        method='controlDevice',
        params={'command': 'disconnect', 'headset': HEADSET_ID, 'connectionType': 'usb cable'},
    )

    with pytest.raises(ValueError, match='command must be either "connect", "disconnect", or "refresh".'):
        make_connection('invalid')


def test_query_headsets(api_request: APIRequest) -> None:
    """Test querying headsets."""
    assert query_headset() == api_request(id=HeadsetID.QUERY_HEADSET, method='queryHeadsets', params={})
    assert query_headset(HEADSET_ID) == api_request(
        id=HeadsetID.QUERY_HEADSET, method='queryHeadsets', params={'id': HEADSET_ID}
    )
    assert query_headset(include_flex_mappings=True) == api_request(
        id=HeadsetID.QUERY_HEADSET, method='queryHeadsets', params={'includeFlexMappings': True}
    )
    assert query_headset(HEADSET_ID, include_flex_mappings=True) == api_request(
        id=HeadsetID.QUERY_HEADSET, method='queryHeadsets', params={'id': HEADSET_ID, 'includeFlexMappings': True}
    )


def test_update_headset(api_request: APIRequest) -> None:
    """Test updating a headset."""
    assert update_headset(AUTH_TOKEN, HEADSET_ID, Setting(mode='EPOC', eegRate=128, memsRate=0)) == api_request(
        id=HeadsetID.UPDATE_HEADSET,
        method='updateHeadset',
        params={
            'cortexToken': AUTH_TOKEN,
            'headset': HEADSET_ID,
            'setting': Setting(mode='EPOC', eegRate=128, memsRate=0),
        },
    )

    with pytest.raises(ValueError):
        # EPOC headset only supports 128Hz EEG rate.
        update_headset(AUTH_TOKEN, HEADSET_ID, Setting(mode='EPOC', eegRate=256, memsRate=0))

        # EPOC headset only supports 0Hz MEMS rate.
        update_headset(AUTH_TOKEN, HEADSET_ID, Setting(mode='EPOC', eegRate=128, memsRate=32))

    assert update_headset(AUTH_TOKEN, HEADSET_ID, Setting(mode='EPOCPLUS', eegRate=128, memsRate=32)) == api_request(
        id=HeadsetID.UPDATE_HEADSET,
        method='updateHeadset',
        params={
            'cortexToken': AUTH_TOKEN,
            'headset': HEADSET_ID,
            'setting': Setting(mode='EPOCPLUS', eegRate=128, memsRate=32),
        },
    )

    assert update_headset(AUTH_TOKEN, HEADSET_ID, Setting(mode='EPOCPLUS', eegRate=256, memsRate=128)) == api_request(
        id=HeadsetID.UPDATE_HEADSET,
        method='updateHeadset',
        params={
            'cortexToken': AUTH_TOKEN,
            'headset': HEADSET_ID,
            'setting': Setting(mode='EPOCPLUS', eegRate=256, memsRate=128),
        },
    )

    with pytest.raises(ValueError):
        # EPOCPLUS headset only supports 0Hz, 32Hz, 64Hz, or 128Hz MEMS rate.
        update_headset(AUTH_TOKEN, HEADSET_ID, Setting(mode='EPOCPLUS', eegRate=256, memsRate=16))

        # EPOCPLUS headset only supports 128Hz or 256Hz EEG rate.
        update_headset(AUTH_TOKEN, HEADSET_ID, Setting(mode='EPOCPLUS', eegRate=64, memsRate=128))


def test_update_custom_info(api_request: APIRequest) -> None:
    """Test updating custom information of a headset."""
    assert update_custom_info(AUTH_TOKEN, HEADSET_ID, 'back') == api_request(
        id=HeadsetID.UPDATE_CUSTOM_INFO,
        method='updateHeadsetCustomInfo',
        params={'cortexToken': AUTH_TOKEN, 'headsetId': HEADSET_ID, 'headbandPosition': 'back'},
    )
    assert update_custom_info(AUTH_TOKEN, HEADSET_ID, 'top') == api_request(
        id=HeadsetID.UPDATE_CUSTOM_INFO,
        method='updateHeadsetCustomInfo',
        params={'cortexToken': AUTH_TOKEN, 'headsetId': HEADSET_ID, 'headbandPosition': 'top'},
    )

    # headband_position must be either "back" or "top".
    with pytest.raises(ValueError, match='headband_position must be either "back" or "top".'):
        update_custom_info(AUTH_TOKEN, HEADSET_ID, 'front')


def test_sync_with_clock(api_request: APIRequest) -> None:
    """Update syncing with the headset clock."""
    monotonic_time: float = time.monotonic()
    system_time: float = time.time()

    assert sync_with_clock(HEADSET_ID, monotonic_time, system_time) == api_request(
        id=HeadsetID.SYNC_WITH_CLOCK,
        method='syncWithHeadsetClock',
        params={'headset': HEADSET_ID, 'monotonicTime': monotonic_time, 'systemTime': system_time},
    )


def test_subscription(api_request: APIRequest) -> None:
    """Test subscribing to a headset."""
    streams: list[str] = ['eeg', 'mot', 'met', 'fac']

    # Subscribe.
    assert subscription(AUTH_TOKEN, SESSION_ID, streams, 'subscribe') == api_request(
        id=HeadsetID.SUBSCRIBE,
        method='subscribe',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID, 'streams': streams},
    )

    # Unsubscribe.
    assert subscription(AUTH_TOKEN, SESSION_ID, streams, 'unsubscribe') == api_request(
        id=HeadsetID.UNSUBSCRIBE,
        method='unsubscribe',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID, 'streams': streams},
    )

    with pytest.raises(ValueError, match='method must be either "subscribe" or "unsubscribe".'):
        subscription(AUTH_TOKEN, SESSION_ID, streams, 'invalid')
