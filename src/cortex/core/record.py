from enum import IntEnum
from typing import Any, Literal


class RecordID(IntEnum):
    """Record request IDs."""

    CREATE_RECORD = 11
    STOP_RECORD = 12
    EXPORT_RECORD = 13


def create_record(
    auth: str,
    session_id: str,
    title: str,
    **kwargs: Any,
) -> dict[str, str | int | dict[str, str | Any]]:
    """Create a record.

    Args:
        auth (str): The Cortex authentication token.
        session_id (str): The session ID.
        title (str): The record title.

    Keyword Args:
        **kwargs (Any): Additional parameters.

    Returns:
        dict[str, str | int | dict[str, str | Any]]: The record creation status.

    """
    _record: dict[str, str | int | dict[str, str | Any]] = {
        'id': RecordID.CREATE_RECORD,
        'jsonrpc': '2.0',
        'method': 'createRecord',
        'params': {
            'cortexToken': auth,
            'session': session_id,
            'title': title,
            **kwargs,
        },
    }

    return _record


def stop_record(
    auth: str,
    session_id: str,
) -> dict[str, str | int | dict[str, str]]:
    """Stop the record.

    Args:
        auth (str): The Cortex authentication token.
        session_id (str): The session ID.

    Returns:
        dict[str, str | int | dict[str, str]]: The record stop status.

    """
    _record: dict[str, str | int | dict[str, str]] = {
        'id': RecordID.STOP_RECORD,
        'jsonrpc': '2.0',
        'method': 'stopRecord',
        'params': {
            'cortexToken': auth,
            'session': session_id,
        },
    }

    return _record


def export_record(
    auth: str,
    folder: str,
    stream_types: list[str],
    export_format: Literal['EDF', 'CSV'],
    record_ids: list[str],
    version: Literal['v1', 'v2'],
    **kwargs: Any,
) -> dict[str, str | int | dict[str, str | list[str] | Any]]:
    """Export a record.

    Args:
        auth (str): The Cortex authentication token.
        folder (str): The folder path.
        stream_types (list[str]): The stream types.
        export_format (Literal['EDF', 'CSV']): The export format.
        record_ids (list[str]): The record IDs.
        version (Literal['v1', 'v2']): The export version.

    Keyword Args:
        **kwargs (Any): Additional parameters.

    Returns:
        dict[str, str | int | dict[str, str | list[str] | Any]]: The record export status.

    """

    _params = {
        'cortexToken': auth,
        'folder': folder,
        'streamTypes': stream_types,
        'format': export_format,
        'recordIds': record_ids,
        **kwargs,
    }
    if export_format == 'CSV':
        _params['version'] = version

    _record: dict[str, str | int | dict[str, str | list[str] | Any]] = {
        'id': RecordID.EXPORT_RECORD,
        'jsonrpc': '2.0',
        'method': 'exportRecord',
        'params': _params,
    }

    return _record
