from collections.abc import Mapping
from typing import Any, Literal, TypeAlias, TypedDict

# A dict with fields "from" and "to".
Interval = TypedDict('Interval', {'from': str, 'to': str})


class Attribute(TypedDict):
    """Demographic attribute."""

    # The naem of the attribute.
    name: str

    # The value of the attribute.
    value: str


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


class SubjectQuery(TypedDict, total=False):
    """Query parameters."""

    # Get a subject by its id.
    uuid: str

    # Filter the subjects by name.
    subjectName: str

    # Filter the subjects by their gender.
    sex: Literal['M', 'F', 'U']

    # Filter the subjects by their country code.
    countryCode: str

    # An object with fields "from" and "to" to filter
    # the subjects by their date of birth.
    dateOfBirth: Interval

    # An object with the fields as the keyword to
    # search and values are the list of fields to search.
    # The list of fields to search can contain
    # "subjectName", "lastName", "email".
    keyword: Mapping[str, str]


# Request type aliases.
BaseRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str]]

# Auth
AuthorizeRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | int]]

# FacialExpression
FacialExpressionRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | int]]

# Headset
ConnectHeadsetRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | Mapping[str, str]]]
UpdateHeadsetRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | Setting]]
SyncWithClockRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | float]]
SubscriptionRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | list[str]]]

# Markers
MarkerRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | int | Mapping[str, Any]]]

# MentalCommand
MentalCommandActionRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | list[str]]]

# Records
CreateRecordRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | int | list[str]]]
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

# Subject
SubjectRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | list[Attribute]]]
QuerySubjectRequest: TypeAlias = Mapping[
    str, str | int | Mapping[str, str | SubjectQuery | int | list[Mapping[str, str]]]
]

# Train
TrainingRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | int]]
