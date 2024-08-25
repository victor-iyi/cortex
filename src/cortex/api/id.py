from enum import IntEnum


class AuthID(IntEnum):
    """Authentication request IDs."""

    CORTEX_INFO = 1
    USER_LOGIN = 2
    REQUEST_ACCESS = 3
    HAS_ACCESS_RIGHT = 4
    AUTHORIZE = 5
    GEN_NEW_TOKEN = 6
    USER_INFO = 7
    LICENSE_INFO = 8


class HeadsetID(IntEnum):
    """Headset request IDs."""

    QUERY_HEADSET = 9
    UPDATE_HEADSET = 10
    UPDATE_CUSTOM_INFO = 11
    SYNC_WITH_CLOCK = 12
    CONNECT = 13
    DISCONNECT = 14
    SUBSCRIBE = 15
    UNSUBSCRIBE = 16


class SessionID(IntEnum):
    """Session request IDs."""

    CREATE = 17
    UPDATE = 18
    QUERY = 19


class RecordsID(IntEnum):
    """Records request IDs."""

    CREATE = 20
    STOP = 21
    UPDATE = 22
    DELETE = 23
    EXPORT = 24
    QUERY = 25
    INFO = 26
    CONFIG_OPT_OUT = 27
    DOWNLOAD_DATA = 28


class MarkersID(IntEnum):
    """Markers request IDs."""

    INJECT = 29
    UPDATE = 30


class SubjectsID(IntEnum):
    """Subjects request IDs."""

    CREATE = 31
    UPDATE = 32
    DELETE = 33
    QUERY = 34
    DEMO_ATTR = 35


class ProfileID(IntEnum):
    """Profile request IDs."""

    QUERY = 36
    CURRENT = 37
    SETUP = 38
    GUEST = 39
    DETECTION_INFO = 40


class TrainingID(IntEnum):
    """Training request IDs."""

    TRAINING = 41
    SIGNATURE_ACTIONS = 42
    TRAINING_TIME = 43


class FacialExpressionID(IntEnum):
    """Facial expression request IDs."""

    SIGNATURE_TYPE = 44
    THRESHOLD = 45


class MentalCommandID(IntEnum):
    """Mental command request IDs."""

    SET_ACTIVE_ACTION = 46
    GET_ACTIVE_ACTION = 47
    BRAIN_MAP = 48
    SKILL_RATING = 49
    TRAINING_THRESHOLD = 50
    ACTION_SENSITIVITY = 51
