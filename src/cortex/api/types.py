from collections.abc import Mapping
from typing import TypedDict, TypeAlias


# A dict with fields "from" and "to".
Interval = TypedDict('Interval', {'from': str, 'to': str})


class RecordQuery(TypedDict, total=False):
    """Record query parameters."""

    # Filter the records by their license.
    licenseId: str

    # Filter the records by their application ID.
    applicationId: str

    # Filter the records by title, description or subject name.
    keyword: str

    # An object with fields "from" and "to" to filter the records
    # by their start date time.
    startDatetime: Interval

    # An object with fields "from" and "to" to filter the records
    # by their modification date time.
    modifiedDatetime: Interval

    # An object with fields "from" and "to" to filter the records
    # by their duration.
    duration: Interval


# Records.
CreateRecordRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | int | list[str]]]
StopRecordRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str]]
UpdateRecordRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | list[str]]]
DeleteRecordRequest: TypeAlias = Mapping[str, str | int | Mapping[str, list[str]]]
ExportRecordRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | int | list[str] | bool]]
QueryRecordRequest: TypeAlias = Mapping[
    str,
    str | int | Mapping[str, str | RecordQuery | int | bool | list[Mapping[str, str]]],
]
RecordInfoRequest: TypeAlias = Mapping[str, str | int | Mapping[str, list[str]]]
ConfigOptOutRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | bool]]
DownloadRecordDataRequest: TypeAlias = Mapping[str, str | int | Mapping[str, list[str]]]
