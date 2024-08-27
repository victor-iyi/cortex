"""## [Markers]

A marker is to mark a point in time, or a period of time, inside a [record].

Markers are always linked to a record, so you must start a record before you
add a marker. You can't add nor update a marker after the record is stopped.
You can associate some data to each marker, like a value and a label.

There are two types of markers:
    - An instance marker is to mark a point in time.
      You call [injectMarker] to create the marker at a specific timestamp.
    - An interval marker is to mark a period of time, with a beginning and an end.
      First you create an instance marker with [injectMarker].
      This sets the beginning of the interval. Then you call [updateMarker] to set
      the end of the interval, turning the instance marker into an interval marker.

[Markers]: https://emotiv.gitbook.io/cortex-api/markers
[record]: https://emotiv.gitbook.io/cortex-api/records
[injectMarker]: https://emotiv.gitbook.io/cortex-api/markers/injectmarker
[updateMarker]: https://emotiv.gitbook.io/cortex-api/markers/updatemarker

"""

from collections.abc import Mapping
from typing import Any, TypeAlias

from cortex.api.id import MarkersID

# Return type aliases.
MarkerRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | int | dict[str, Any]]]


def inject_marker(
    auth: str,
    session_id: str,
    time: int,
    value: str | int,
    label: str,
    *,
    port: str | None = None,
    extras: dict[str, Any] | None = None,
) -> MarkerRequest:
    """Inject a marker.

    Args:
        auth (str): The Cortex authentication token.
        session_id (str): The session ID.
        time (int): The time in milliseconds.
        value (str | int): The marker value.
        label (str): The marker label.

    Keyword Args:
        port (str, optional): The marker port.
        extras (dict[str, Any], optinoal): Additional parameters.

    Read More:
        [injectMarker](https://emotiv.gitbook.io/cortex-api/markers/injectmarker)

    Returns:
        MarkerRequest: The marker injection status.

    """
    _params = {
        'cortexToken': auth,
        'session': session_id,
        'time': time,
        'value': value,
        'label': label,
    }

    if port is not None:
        _params['port'] = port

    if extras is not None:
        _params['extras'] = extras

    _marker = {
        'id': MarkersID.INJECT,
        'jsonrpc': '2.0',
        'method': 'injectMarker',
        'params': _params,
    }

    return _marker


def update_marker(
    auth: str,
    session_id: str,
    marker_id: str,
    time: int,
    *,
    extras: dict[str, Any] | None = None,
) -> MarkerRequest:
    """Update a marker.

    Args:
        auth (str): The Cortex authentication token.
        session_id (str): The session ID.
        marker_id (str): The marker ID.
        time (int): The time in milliseconds.

    Keyword Args:
        extras (dict[str, Any], optional): Additional parameters.

    Read More:
        [updateMarker](https://emotiv.gitbook.io/cortex-api/markers/updatemarker)

    Returns:
        MarkerRequest: The marker update status.

    """
    _params = {
        'cortexToken': auth,
        'session': session_id,
        'markerId': marker_id,
        'time': time,
    }

    if extras is not None:
        _params['extras'] = extras

    _marker = {
        'id': MarkersID.UPDATE,
        'jsonrpc': '2.0',
        'method': 'updateMarker',
        'params': _params,
    }

    return _marker
