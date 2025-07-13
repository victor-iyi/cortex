"""Type aliases for the Cortex API."""

from collections.abc import Mapping
from typing import Any, Literal, TypedDict

from cortex.api.response import HeadsetObject, MarkerObject, SubjectObject

# +---------------------------------------------------------------------------+
# |                             Request Objects
# +---------------------------------------------------------------------------+

# A dict with fields "from" and "to".
Interval = TypedDict('Interval', {'from': str | int, 'to': str | int})


class Attribute(TypedDict):
    """Demographic attribute."""

    name: str
    """The naem of the attribute."""

    value: str
    """The value of the attribute."""


class RecordQuery(TypedDict, total=False):
    """Record query parameters."""

    licenseId: str
    """Filter the records by their license."""

    applicationId: str
    """Filter the records by their application ID."""

    keyword: str
    """Filter the records by title, description or subject name."""

    startDatetime: Interval
    """An object with fields "from" and "to" to filter the records
    by their start date time.
    """

    modifiedDatetime: Interval
    """An object with fields "from" and "to" to filter the records
    by their modification date time.
    """

    duration: Interval
    """An object with fields "from" and "to" to filter the records
    by their duration.
    """


class Setting(TypedDict):
    """Headset setting."""

    mode: Literal['EPOC', 'EPOCPLUS']
    """In "EPOC" mode, the EEG resolution is 14 bits.

    In "EPOCPLUS" mode, the EEG resolutions are 16 bits.
    """

    eegRate: Literal[128, 256]
    """The EEG sample rate, in hertz.

    If the mode is "EPOC", then the EEG rate must be 128.

    If the mode is "EPOCPLUS", then the EEG rate can be 128 or 256.
    """

    memsRate: Literal[0, 32, 64, 128]
    """The motion sample rate, in hertz.

    If the mode is "EPOC", then the motion rate must be 0.

    If the mode is "EPOCPLUS", then the motion rate can be 0, 32, 64, or 128.
    """


class SubjectQuery(TypedDict, total=False):
    """Query parameters."""

    uuid: str
    """Get a subject by its id."""

    subjectName: str
    """Filter the subjects by name."""

    sex: Literal['M', 'F', 'U']
    """Filter the subjects by their gender."""

    countryCode: str
    """Filter the subjects by their country code."""

    dateOfBirth: Interval
    """An object with fields "from" and "to" to filter
    the subjects by their date of birth.
    """

    keyword: Mapping[str, str | list[str]]
    """An object with the fields as the keyword to
    search and values are the list of fields to search.

    The list of fields to search can contain
    "subjectName", "lastName", "email".
    """


type ConnectionType = Literal['bluetooth', 'usb cable', 'dongle']
type ExportFormat = Literal['EDF', 'EDFPLUS', 'BDFPLUS', 'CSV']

# Request type aliases.
type BaseRequest = Mapping[str, str | int | Mapping[str, str]]

# Auth
type AuthorizeRequest = Mapping[str, str | int | Mapping[str, str | int]]

# FacialExpression
type FacialExpressionRequest = Mapping[str, str | int | Mapping[str, str | int]]

# Headset
type ConnectHeadsetRequest = Mapping[str, str | int | Mapping[str, str | Mapping[str, str]]]
type UpdateHeadsetRequest = Mapping[str, str | int | Mapping[str, str | Setting]]
type SyncWithClockRequest = Mapping[str, str | int | Mapping[str, str | float]]
type SubscriptionRequest = Mapping[str, str | int | Mapping[str, str | list[str]]]

# Markers
type MarkerRequest = Mapping[str, str | int | Mapping[str, str | int | Mapping[str, Any]]]

# MentalCommand
type MentalCommandActionRequest = Mapping[str, str | int | Mapping[str, str | list[str]]]

# Records
type CreateRecordRequest = Mapping[str, str | int | Mapping[str, str | int | list[str]]]
type UpdateRecordRequest = Mapping[str, str | int | Mapping[str, str | list[str]]]
type DeleteRecordRequest = Mapping[str, str | int | Mapping[str, list[str]]]
type ExportRecordRequest = Mapping[str, str | int | Mapping[str, str | int | list[str] | bool]]
type QueryRecordRequest = Mapping[
    str, str | int | Mapping[str, str | RecordQuery | int | bool | list[Mapping[str, str]]]
]
type RecordInfoRequest = Mapping[str, str | int | Mapping[str, list[str]]]
type ConfigOptOutRequest = Mapping[str, str | int | Mapping[str, str | bool]]
type DownloadRecordDataRequest = Mapping[str, str | int | Mapping[str, list[str]]]

# Subject
type SubjectRequest = Mapping[str, str | int | Mapping[str, str | list[Attribute]]]
type QuerySubjectRequest = Mapping[str, str | int | Mapping[str, str | SubjectQuery | int | list[Mapping[str, str]]]]

# Train
type TrainingRequest = Mapping[str, str | int | Mapping[str, str | int]]


# +---------------------------------------------------------------------------+
# |                             Response Objects
# +---------------------------------------------------------------------------+


class SessionObject(TypedDict, total=False):
    """The information about a session."""

    id: str
    """The id of this session."""

    status: Literal['opened', 'activated', 'closed']
    """Can be "opened", "activated", or "closed"."""

    owner: str
    """The EmotivID of the user."""

    license: str
    """The id of the license used by this session. Or
    an empty string if the session wasn't activated.
    """

    appId: str
    """The application id of your Cortex app."""

    started: str
    """When this session was created. (ISO datetime)"""

    stopped: str
    """When this session was closed. (ISO datetime)"""

    streams: list[str]
    """The data streams you subscribed to.

    See [subscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/subscribe).
    """

    recordIds: list[str]
    """The ids of all the records created by this session.

    See [createRecord](https://emotiv.gitbook.io/cortex-api/records/createrecord).
    """

    recording: bool
    """True if a record is currently in progress for this session. False otherwise."""

    headset: HeadsetObject
    """The [headset object]. It contains information about the headset linked to this session.

    [headset object]: https://emotiv.gitbook.io/cortex-api/headset/headset-object
    """


class RecordsObject(TypedDict, total=False):
    """The information about a record."""

    uuid: str
    """The id of this record."""

    ownerId: str
    """The id of the user this record belongs to. It is a GUID, it is not the EmotivID of the user."""

    applicationId: str
    """The id of the application that created this record."""

    applicationVersion: str
    """The version of the application that created this record."""

    title: str
    """The title of the record."""

    description: str
    """The description of the record."""

    tags: list[str]
    """The tags associated with this record."""

    experimentId: int
    """The experiment id associated with this record."""

    startTime: str
    """When this record was created. (ISO datetime)"""

    endTime: str
    """When this record was stopped. (ISO datetime)"""

    licenseId: str
    """The id of the license used by this record."""

    licneseScope: list[str]
    """List of the data streams the license has access to.

    The scope "eeg" gives access to the raw EEG data.
    The scope "pm" gives access to the 2 hertz performance metrics.
    """

    subject: SubjectObject
    """This object has a single field "subjectName".
    It is the subject name used to create this record.

    You can use querySubjects to get more information about the subject.
    If the record was created without a subject name, then the field "subjectName"
    contains the EmotivID of the user.
    """

    localOnly: bool
    """If true then this record will not be uploaded to the EMOTIV cloud.
    If false then it will be uploaded.
    """

    headsetPosition: Literal['back', 'top']
    """If the headset is an EPOC X, then this field tells you the position of the
    headband of this headset during this record. Can be "back" or "top".
    If the headset is not an EPOC X, then this field is null.
    """

    markers: list[MarkerObject] | None
    """The markers added to this record."""
