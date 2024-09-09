"""Response objects for the Cortex API."""

from collections.abc import Mapping
from typing import Literal, TypedDict


class FlexMapping(TypedDict):
    """The mapping of the EEG channels of an EPOC Flex device."""

    # Describe which EEG channel is mapped to which physical connector
    # of EPOC Flex device. The keys are the names of the connectors, the
    # values are the names of the EEG channels.
    # Example: {"CMS": "TP8", "DRL": "P6", "RM": "TP10", "RN": "P4", "RO": "P8"}
    mappings: Mapping[str, str]


class SettingsObject(TypedDict, total=False):
    """The configuration of the EEG and motion data of a headset."""

    # Can be "EPOC", "EPOCPLUS", or "EPOCFLEX"
    mode: Literal['EPOC', 'EPOCPLUS', 'EPOCFLEX']

    # The EEG sample rate, in hertz.
    eegRate: int

    # The EEG resolution, in bits.
    eegRes: int

    # The motion data sample rate, in hertz.
    memsRate: int

    # The motion data resolution, in bits.
    memsRes: int


class HeadsetObject(TypedDict, total=False):
    """The information about a headset."""

    # The id of this headset.
    id: str

    # Can be "discovered", "connecting", or "connected".
    status: Literal['discovered', 'connecting', 'connected']

    # Can be "bluetooth", "dongle", "usb cable", or "extender".
    connectedBy: Literal['bluetooth', 'dongle', 'usb cable', 'extender']

    # The version of the headset firmware.
    fireware: str

    # The names of the motion sensors of this headset.
    motionSensors: list[str]

    # The names of the EEG sensors of this headset. Use the international
    # 10-20 system.
    sensors: list[str]

    # An object containing the configuration of the EEG and motion data of this headset.
    settings: SettingsObject

    # If the headset is an EPOC Flex, then this field is an object containing
    # information about the mapping of the EEG channels.
    flexMappings: FlexMapping

    # If the headset is an EPOC X, then this field tells you the position of the
    # headband of this headset. Can be "back" or "top". If the headset is not
    # EPOC X, then this field is null.
    headbandPosition: Literal['back', 'top']

    # The custom name of the headset. The user can set it in EMOTIV App.
    customName: str


class SessionObject(TypedDict, total=False):
    """The information about a session."""

    # The id of this session.
    id: str

    # Can be "opened", "activated", or "closed".
    status: Literal['opened', 'activated', 'closed']

    # The EmotivID of the user.
    owner: str

    # The id of the license used by this session. Or
    # an empty string if the session wasn't activated.
    license: str

    # The application id of your Cortex app.
    appId: str

    # When this session was created. (ISO datetime)
    started: str

    # When this session was closed. (ISO datetime)
    stopped: str

    # The data streams you subscribed to.
    # See [subscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/subscribe).
    streams: list[str]

    # The ids of all the records created by this session.
    # See [createRecord](https://emotiv.gitbook.io/cortex-api/records/createrecord).
    recordIds: list[str]

    # True if a record is currently in progress for this session. False otherwise.
    recording: bool

    # The [headset object]. It contains information about the headset linked to this session.
    # [headset object]: https://emotiv.gitbook.io/cortex-api/headset/headset-object
    headset: HeadsetObject


class MarkerObject(TypedDict, total=False):
    """The information about a marker."""

    # The id of the marker.
    uuid: str

    # Can be "interval" or "instance".
    type: Literal['interval', 'instance']

    # The value you set in `injectMarker`.
    value: str | int

    # The label of the marker.
    label: str

    # The port of the marker, i.e. where the marker comes from.
    # Examples: "Software", "Serial", etc...
    port: str

    # The timestamp you set in `injectMarker`. (ISO date time).
    startDatetime: str

    # The timestamp you set in `updateMarker`. (ISO date time).
    # I fyou didn't call this method, then `endDatetime` is equal to `startDatetime`.
    endDatetime: str

    # Can be any extra information you want to associate with this marker.
    extras: Mapping[str, str]


class DemographicAttribute(TypedDict):
    """A demographic attribute of a subject."""

    # The name of the attribute.
    name: str

    # The value of the attribute.
    value: str


class SubjectObject(TypedDict, total=False):
    """The information about a subject."""

    # The name of the subject
    subjectName: str

    # The date of birth of the subject. The format is "YYYY-MM-DD", e.g. "1980-12-25".
    dateOfBirth: str

    # Can be "M", "F", or "U". These letters stands for male, female, unknown respectively.
    sex: Literal['M', 'F', 'U']

    # Experiment count.
    experimentCount: int

    # The Alpha-2 ISO code of the country the subject lives in.
    countryCode: str

    # The name of the country the subject lives in.
    countryName: str

    # The state the subject lives in.
    state: str

    # The city the subject lives in.
    city: str

    # A list of demographic attribute objects.
    attributes: list[DemographicAttribute]


class RecordsObject(TypedDict, total=False):
    """The information about a record."""

    # The id of this record.
    uuid: str

    # The id of the user this record belongs to. It is a GUID, it is not the EmotivID of the user.
    ownerId: str

    # The id of the application that created this record.
    applicationId: str

    # The version of the application that created this record.
    applicationVersion: str

    # The title of the record.
    title: str

    # The description of the record.
    description: str

    # The tags associated with this record.
    tags: list[str]

    # The experiment id associated with this record.
    experimentId: int

    # When this record was created. (ISO datetime)
    startTime: str

    # When this record was stopped. (ISO datetime)
    endTime: str

    # The id of the license used by this record.
    licenseId: str

    # List of the data streams the license has access to.
    # The scope "eeg" gives access to the raw EEG data.
    # The scope "pm" gives access to the 2 hertz performance metrics.
    licneseScope: list[str]

    # This object has a single field "subjectName".
    # It is the subject name used to create this record.
    # You can use querySubjects to get more information about the subject.
    # If the record was created without a subject name, then the field "subjectName" contains the EmotivID of the user.
    subject: SubjectObject

    # If true then this record will not be uploaded to the EMOTIV cloud.
    # If false then it will be uploaded.
    localOnly: bool

    # If the headset is an EPOC X, then this field tells you the position of the
    # headband of this headset during this record. Can be "back" or "top".
    # If the headset is not an EPOC X, then this field is null.
    headsetPosition: Literal['back', 'top']

    # The markers added to this record.
    markers: list[MarkerObject] | None
