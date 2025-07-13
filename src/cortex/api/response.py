"""Response objects for the Cortex API."""

from collections.abc import Mapping
from typing import Literal, TypedDict


class AssesObject(TypedDict):
    """The information about the auth access."""

    accessGranted: bool
    """`True`, if the user has already approved your application

    `False`, if the user declined your application, or didn't approve it yet
    """

    message: str
    """The message to show to the user when asking for approval."""


class AuthorizeObject(TypedDict):
    """The information about the authorization."""

    cortexToken: str
    """The Cortex token of the user."""

    warning: Mapping[str, str | int]
    """Contains a message and the URL to accept the EULA."""


class CortexInfoObject(TypedDict):
    """The information about the Cortex API."""

    buildDate: str
    """The date and time the Cortex binary was built (ISO datetime)."""

    buildNumber: str
    """The interval build number."""

    version: str
    """The version of Cortex. It should have the format `2.y.z`"""


class FlexMapping(TypedDict):
    """The mapping of the EEG channels of an EPOC Flex device."""

    mappings: Mapping[str, str]
    """Describe which EEG channel is mapped to which physical connector
    of EPOC Flex device. The keys are the names of the connectors, the
    values are the names of the EEG channels.

    Example: {"CMS": "TP8", "DRL": "P6", "RM": "TP10", "RN": "P4", "RO": "P8"}
    """


class UserLoginObject(TypedDict):
    """The information about the user login."""

    username: str
    """The EmotiveID of the user."""

    currentOSUId: str
    """The ID of current OS account."""

    currentOSUsername: str
    """The name of the currentOSUId."""

    loggedInOSUId: str
    """The ID of the OS account used to login to Emotiv Launcher."""

    loggedInOSUsername: str
    """The name of the loggedInOSUId."""

    lastLoginTime: str
    """When the user logged in the last time (ISO datetime)."""


class LicenseAgreementObject(TypedDict):
    """The information about the license agreement."""

    accepted: bool
    """True if the user has accepted the license agreement."""

    licenseUrl: str
    """The URL to the license agreement."""


class _DeviceInfo(TypedDict):
    """The information about the device."""

    deviceLimit: int
    devicesPerSeat: int
    sessionLimit: Mapping[str, int | None]


class LicenseObject(TypedDict):
    """The information about the license."""

    applications: list[str]
    billingFrom: str
    billingTo: str
    deviceInfo: _DeviceInfo
    expired: bool
    extenderLimit: int
    hardLimitTime: str
    isCommercial: bool
    licneseId: str
    licenseName: str
    localQuota: int
    maxDebit: int | None
    scopes: list[str]
    seatCount: int
    sessionCount: int
    softLimitTime: str
    totalDebit: int
    totalRegisteredDevices: int
    validFrom: str
    validTo: str


class LicneseInfoObject(TypedDict):
    """The information about the license."""

    isOnline: bool
    """`True`, if Cortex was able to get the license information from the EMOTIV cloud

    `False`, if Cortex got the license information for its local cache
    """

    license: LicenseObject
    """An object containing all the information about the current license."""


class UserInfoObject(TypedDict):
    """The information about the user."""

    username: str
    """The EmotivID of the user."""

    firstName: str
    """The first name of the user."""

    lastName: str
    """The last name of the user."""

    licenseAgreement: LicenseAgreementObject
    """An object that contain information about the EULA agreement"""


class FESignatureTypeObject(TypedDict):
    """The information about the facial expression signature type."""

    currentSig: str
    """The current signature used by the profile. Can be "universal" or "trained"."""

    availableSigs: list[str]
    """The signatures you can use with the profile.

    The "universal" one is always available, but the "trained" one requires some training.
    """


class SettingsObject(TypedDict):
    """The configuration of the EEG and motion data of a headset."""

    mode: Literal['EPOC', 'EPOCPLUS', 'EPOCFLEX']
    """Can be "EPOC", "EPOCPLUS", or "EPOCFLEX"."""

    eegRate: int
    """The EEG sample rate, in hertz."""

    eegRes: int
    """The EEG resolution, in bits."""

    memsRate: int
    """The motion data sample rate, in hertz."""

    memsRes: int
    """The motion data resolution, in bits."""


class HeadsetObject(TypedDict, total=False):
    """The information about a headset."""

    id: str
    """The id of this headset."""

    status: Literal['discovered', 'connecting', 'connected']
    """Can be "discovered", "connecting", or "connected"."""

    connectedBy: Literal['bluetooth', 'dongle', 'usb cable', 'extender']
    """Can be "bluetooth", "dongle", "usb cable", or "extender"."""

    fireware: str
    """The version of the headset firmware."""

    motionSensors: list[str]
    """The names of the motion sensors of this headset."""

    sensors: list[str]
    """The names of the EEG sensors of this headset. Use the international
    10-20 system.
    """

    settings: SettingsObject
    """An object containing the configuration of the EEG and motion data of this headset."""

    flexMappings: FlexMapping
    """If the headset is an EPOC Flex, then this field is an object containing
    information about the mapping of the EEG channels.
    """

    headbandPosition: Literal['back', 'top']
    """If the headset is an EPOC X, then this field tells you the position of the
    headband of this headset. Can be "back" or "top". If the headset is not
    EPOC X, then this field is null.
    """

    customName: str
    """The custom name of the headset. The user can set it in EMOTIV App."""


class QueryProfileObject(TypedDict):
    """The information about the query profile."""

    uuid: str
    """The unique ID of this profile."""

    name: str
    """The name of the profile."""

    readOnly: bool
    """If a headset is created before v3.6.5, the profile will become read-only when upgrading to v3.6.5"""

    eegChannels: list[str]
    """The list of EEG channels of a headset with which this profile can be loaded.

    For example, if eegChannels of a profile is ["AF3","T7","Pz","T8","AF4"],
    this profile can be loaded for Insight headset.
    """


class SessionObject(TypedDict):
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


class MarkerObject(TypedDict, total=False):
    """The information about a marker."""

    uuid: str
    """The id of the marker."""

    type: Literal['interval', 'instance']
    """Can be "interval" or "instance"."""

    value: str | int
    """The value you set in `injectMarker`."""

    label: str
    """The label of the marker."""

    port: str
    """The port of the marker, i.e. where the marker comes from.

    Examples: "Software", "Serial", etc...
    """

    startDatetime: str
    """The timestamp you set in `injectMarker`. (ISO date time)."""

    endDatetime: str
    """The timestamp you set in `updateMarker`. (ISO date time).

    If you didn't call this method, then `endDatetime` is equal to `startDatetime`.
    """

    extras: Mapping[str, str]
    """Can be any extra information you want to associate with this marker."""


class DemographicAttribute(TypedDict):
    """A demographic attribute of a subject."""

    name: str
    """The name of the attribute."""

    value: str
    """The value of the attribute."""


class SubjectObject(TypedDict, total=False):
    """The information about a subject."""

    subjectName: str
    """The name of the subject."""

    dateOfBirth: str
    """The date of birth of the subject. The format is "YYYY-MM-DD", e.g. "1980-12-25"."""

    sex: Literal['M', 'F', 'U']
    """Can be "M", "F", or "U". These letters stands for male, female, unknown respectively."""

    experimentCount: int
    """Experiment count."""

    countryCode: str
    """The Alpha-2 ISO code of the country the subject lives in."""

    countryName: str
    """The name of the country the subject lives in."""

    state: str
    """The state the subject lives in."""

    city: str
    """The city the subject lives in."""

    attributes: list[DemographicAttribute]
    """A list of demographic attribute objects."""


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
    If the record was created without a subject name, then the field "subjectName" contains the EmotivID of the user.
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
