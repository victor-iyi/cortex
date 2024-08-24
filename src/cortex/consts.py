from enum import IntEnum
from pathlib import Path

# An Emotiv self-signed certificate is used to establish a secure connection to Cortex.
CERTS_DIR: Path = Path(__file__).resolve().parent.parent.parent / 'certificates'
CA_CERTS: Path = CERTS_DIR / 'rootCA.pem'


class ErrorCode(IntEnum):
    """Error codes."""

    ERR_PROFILE_ACCESS_DENIED = -32046


class WarningCode(IntEnum):
    """Warning codes."""

    CORTEX_STOP_ALL_STREAMS = 0
    CORTEX_CLOSE_SESSION = 1
    USER_LOGIN = 2
    USER_LOGOUT = 3
    ACCESS_RIGHT_GRANTED = 9
    ACCESS_RIGHT_REJECTED = 10
    PROFILE_LOADED = 13
    PROFILE_UNLOADED = 14
    CORTEX_AUTO_UNLOAD_PROFILE = 15
    EULA_ACCEPTED = 17
    DISKSPACE_LOW = 19
    DISKSPACE_CRITICAL = 20
    HEADSET_CANNOT_CONNECT_TIMEOUT = 102
    HEADSET_DISCONNECTED_TIMEOUT = 103
    HEADSET_CONNECTED = 104
    HEADSET_CANNOT_WORK_WITH_BTLE = 112
    HEADSET_CANNOT_CONNECT_DISABLE_MOTION = 113
