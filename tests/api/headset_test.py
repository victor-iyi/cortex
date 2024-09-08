"""Tests for the headset module."""

import pytest

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
AUTH_TOKEN: Final[str] = '<AUTH-TOKEN>'
HEADSET_ID: Final[str] = '<HEADSET-ID>'
SESSION_ID: Final[str] = '<SESSION-ID>'
EPOC_FLEX_ID: Final[str] = 'EPOCFLEX-1234123'
MAPPINGS: dict[str, str] = {'CMS': 'F3', 'DRL': 'F5', 'LA': 'AF3', 'LB': 'AF7', 'RA': 'P8'}

# Type aliases
ResponseTemplate: TypeAlias = Callable[..., dict[str, Any]]


def test_connect_headset(response_template: ResponseTemplate) -> None:
    """Test connecting to a headset."""
    assert make_connection('connect') == response_template(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'connect'}
    )

    assert make_connection('connect', headset_id=EPOC_FLEX_ID) == response_template(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'connect', 'headset': EPOC_FLEX_ID}
    )
    assert make_connection('connect', headset_id=EPOC_FLEX_ID, mappings=MAPPINGS) == response_template(
        id=HeadsetID.CONNECT,
        method='controlDevice',
        params={'command': 'connect', 'headset': EPOC_FLEX_ID, 'mappings': MAPPINGS},
    )
    assert make_connection(
        'connect', headset_id=EPOC_FLEX_ID, mappings=MAPPINGS, connection_type='bluetooth'
    ) == response_template(
        id=HeadsetID.CONNECT,
        method='controlDevice',
        params={'command': 'connect', 'headset': EPOC_FLEX_ID, 'mappings': MAPPINGS, 'connectionType': 'bluetooth'},
    )

    assert make_connection('connect', headset_id=HEADSET_ID) == response_template(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'connect', 'headset': HEADSET_ID}
    )
    assert make_connection('connect', headset_id=HEADSET_ID, mappings=MAPPINGS) == response_template(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'connect', 'headset': HEADSET_ID}
    )

    assert make_connection('connect', connection_type='dongle') == response_template(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'connect', 'connectionType': 'dongle'}
    )

    assert make_connection(
        'connect', headset_id=HEADSET_ID, mappings=MAPPINGS, connection_type='usb cable'
    ) == response_template(
        id=HeadsetID.CONNECT,
        method='controlDevice',
        params={'command': 'connect', 'headset': HEADSET_ID, 'connectionType': 'usb cable'},
    )


def test_refresh_headset(response_template: ResponseTemplate) -> None:
    """Test refreshing a headset."""
    assert make_connection('refresh') == response_template(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'}
    )
    assert make_connection('refresh', headset_id=HEADSET_ID) == response_template(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'}
    )

    # Provide mappings only if headset is EPOC FLEX and command is connect.
    assert make_connection('refresh', headset_id=HEADSET_ID, mappings=MAPPINGS) == response_template(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'}
    )
    assert make_connection('refresh', headset_id=EPOC_FLEX_ID, mappings=MAPPINGS) == response_template(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'}
    )

    # Omit connection_type if command is 'refresh'.
    assert make_connection('refresh', connection_type='dongle') == response_template(
        id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'}
    )
    assert make_connection(
        'refresh', headset_id=HEADSET_ID, mappings=MAPPINGS, connection_type='bluetooth'
    ) == response_template(id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'})

    assert make_connection(
        'refresh', headset_id=EPOC_FLEX_ID, mappings=MAPPINGS, connection_type='dongle'
    ) == response_template(id=HeadsetID.CONNECT, method='controlDevice', params={'command': 'refresh'})


def test_disconnect_headset(response_template: ResponseTemplate) -> None:
    """Test disconnecting to a headset."""
    assert make_connection('disconnect') == response_template(
        id=HeadsetID.DISCONNECT, method='controlDevice', params={'command': 'disconnect'}
    )

    assert make_connection('disconnect', headset_id=EPOC_FLEX_ID) == response_template(
        id=HeadsetID.DISCONNECT, method='controlDevice', params={'command': 'disconnect', 'headset': EPOC_FLEX_ID}
    )
    assert make_connection('disconnect', headset_id=EPOC_FLEX_ID, mappings=MAPPINGS) == response_template(
        id=HeadsetID.DISCONNECT, method='controlDevice', params={'command': 'disconnect', 'headset': EPOC_FLEX_ID}
    )
    assert make_connection(
        'disconnect', headset_id=EPOC_FLEX_ID, mappings=MAPPINGS, connection_type='bluetooth'
    ) == response_template(
        id=HeadsetID.DISCONNECT,
        method='controlDevice',
        params={'command': 'disconnect', 'headset': EPOC_FLEX_ID, 'connectionType': 'bluetooth'},
    )

    assert make_connection('disconnect', headset_id=HEADSET_ID) == response_template(
        id=HeadsetID.DISCONNECT, method='controlDevice', params={'command': 'disconnect', 'headset': HEADSET_ID}
    )
    assert make_connection('disconnect', headset_id=HEADSET_ID, mappings=MAPPINGS) == response_template(
        id=HeadsetID.DISCONNECT, method='controlDevice', params={'command': 'disconnect', 'headset': HEADSET_ID}
    )

    assert make_connection('disconnect', connection_type='dongle') == response_template(
        id=HeadsetID.DISCONNECT, method='controlDevice', params={'command': 'disconnect', 'connectionType': 'dongle'}
    )

    assert make_connection(
        'disconnect', headset_id=HEADSET_ID, mappings=MAPPINGS, connection_type='usb cable'
    ) == response_template(
        id=HeadsetID.DISCONNECT,
        method='controlDevice',
        params={'command': 'disconnect', 'headset': HEADSET_ID, 'connectionType': 'usb cable'},
    )


def test_query_headsets(response_template: ResponseTemplate) -> None:
    """Test querying headsets."""
    assert query_headset() == response_template(id=HeadsetID.QUERY_HEADSET, method='queryHeadsets', params={})
    assert query_headset(HEADSET_ID) == response_template(
        id=HeadsetID.QUERY_HEADSET, method='queryHeadsets', params={'id': HEADSET_ID}
    )
    assert query_headset(include_flex_mappings=True) == response_template(
        id=HeadsetID.QUERY_HEADSET, method='queryHeadsets', params={'includeFlexMappings': True}
    )
    assert query_headset(HEADSET_ID, include_flex_mappings=True) == response_template(
        id=HeadsetID.QUERY_HEADSET, method='queryHeadsets', params={'id': HEADSET_ID, 'includeFlexMappings': True}
    )


def test_update_headset(response_template: ResponseTemplate) -> None:
    """Test updating a headset."""
    assert update_headset(AUTH_TOKEN, HEADSET_ID, Setting(mode='EPOC', eegRate=128, memsRate=0)) == response_template(
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

    assert update_headset(
        AUTH_TOKEN, HEADSET_ID, Setting(mode='EPOCPLUS', eegRate=128, memsRate=32)
    ) == response_template(
        id=HeadsetID.UPDATE_HEADSET,
        method='updateHeadset',
        params={
            'cortexToken': AUTH_TOKEN,
            'headset': HEADSET_ID,
            'setting': Setting(mode='EPOCPLUS', eegRate=128, memsRate=32),
        },
    )

    assert update_headset(
        AUTH_TOKEN, HEADSET_ID, Setting(mode='EPOCPLUS', eegRate=256, memsRate=128)
    ) == response_template(
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


def test_update_custom_info(response_template: ResponseTemplate) -> None:
    """Test updating custom information of a headset."""
    assert update_custom_info(AUTH_TOKEN, HEADSET_ID, 'back') == response_template(
        id=HeadsetID.UPDATE_CUSTOM_INFO,
        method='updateHeadsetCustomInfo',
        params={'cortexToken': AUTH_TOKEN, 'headsetId': HEADSET_ID, 'headbandPosition': 'back'},
    )
    assert update_custom_info(AUTH_TOKEN, HEADSET_ID, 'top') == response_template(
        id=HeadsetID.UPDATE_CUSTOM_INFO,
        method='updateHeadsetCustomInfo',
        params={'cortexToken': AUTH_TOKEN, 'headsetId': HEADSET_ID, 'headbandPosition': 'top'},
    )

    # headband_position must be either "back" or "top".
    with pytest.raises(ValueError):
        update_custom_info(AUTH_TOKEN, HEADSET_ID, 'front')


def test_sync_with_clock(response_template: ResponseTemplate) -> None:
    """Update syncing with the headset clock."""
    monotonic_time: float = 1234567890.123
    system_time: float = 1234567890.456

    assert sync_with_clock(HEADSET_ID, monotonic_time, system_time) == response_template(
        id=HeadsetID.SYNC_WITH_CLOCK,
        method='syncWithHeadsetClock',
        params={'headset': HEADSET_ID, 'monotonicTime': monotonic_time, 'systemTime': system_time},
    )


def test_subscription(response_template: ResponseTemplate) -> None:
    """Test subscribing to a headset."""
    streams: list[str] = ['eeg', 'mot', 'met', 'fac']

    # Subscribe.
    assert subscription(AUTH_TOKEN, SESSION_ID, streams, 'subscribe') == response_template(
        id=HeadsetID.SUBSCRIBE,
        method='subscribe',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID, 'streams': streams},
    )

    # Unsubscribe.
    assert subscription(AUTH_TOKEN, SESSION_ID, streams, 'unsubscribe') == response_template(
        id=HeadsetID.UNSUBSCRIBE,
        method='unsubscribe',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID, 'streams': streams},
    )
