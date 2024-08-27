"""## [Profile]

A profile is a persistent object that stores training data for the
facial expression and mental command detections. A profile belongs to a
user and is synchronized to the EMOTIV cloud.

You can use [queryProfile] to list the profiles of the current user. Use
[setupProfile] to manage the profiles, and also to load or unload a
profile for a headset. You can use [training] to add training data to a
profile.

[Profile]:
https://emotiv.gitbook.io/cortex-api/bci#profile

[queryProfile]: https://emotiv.gitbook.io/cortex-api/bci/queryprofile

[setupProfile]:
https://emotiv.gitbook.io/cortex-api/bci/setupprofile

[training]: https://emotiv.gitbook.io/cortex-api/bci/training

"""

from typing import Literal, Mapping, TypeAlias

from cortex.api.id import ProfileID

# Return type aliases.
ProfileRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str]]


def query_profile(auth: str) -> ProfileRequest:
    """Query the list of all training profile.

    Read More:
        [queryProfile](https://emotiv.gitbook.io/cortex-api/bci/queryprofile)

    Returns:
        ProfileRequest: The query profile request.

    """
    _query = {
        'id': ProfileID.QUERY,
        'jsonrpc': '2.0',
        'method': 'queryProfile',
        'params': {
            'cortexToken': auth,
        },
    }

    return _query


def current_profile(
    auth: str,
    headset_id: str,
) -> ProfileRequest:
    """Get the current training profile that is loaded for a specific headset.

    Args:
        auth (str): The Cortex authentication token.
        headset_id (str): The headset ID.

    Read More:
        [getCurrentProfile](https://emotiv.gitbook.io/cortex-api/bci/getcurrentprofile)

    Returns:
        ProfileRequest: The current profile status.

    """
    _profile = {
        'id': ProfileID.CURRENT,
        'jsonrpc': '2.0',
        'method': 'getCurrentProfile',
        'params': {
            'cortexToken': auth,
            'headset': headset_id,
        },
    }

    return _profile


def setup_profile(
    auth: str,
    status: Literal['create', 'load', 'unload', 'save', 'rename', 'delete'],
    profile_name: str,
    *,
    headset_id: str | None = None,
    new_profile_name: str | None = None,
) -> ProfileRequest:
    """Setup a training profile.

    Args:
        auth (str): The Cortex authentication token.
        status (Literal['create', 'load', 'unload', 'save', 'rename', 'delete']): The profile status.
        profile_name (str): The profile name.

    Keyword Args:
        headset_id (str, optional): The headset ID.
        new_profile_name (str, optional): The new profile name.

    Read More:
        [setupProfile](https://emotiv.gitbook.io/cortex-api/bci/setupprofile)

    Returns:
        ProfileRequest: The profile setup status.

    """
    assert status in [
        'create',
        'load',
        'unload',
        'save',
        'rename',
        'delete',
    ], 'Status must be one of create, load, unload, save, rename, delete.'

    _params = {
        'cortexToken': auth,
        'status': status,
        'profile': profile_name,
    }

    if headset_id is not None and status in ('create', 'load', 'unload', 'save'):
        _params['headset'] = headset_id

    if new_profile_name is not None and status == 'rename':
        _params['newProfileName'] = new_profile_name

    _profile = {
        'id': ProfileID.SETUP,
        'jsonrpc': '2.0',
        'method': 'setupProfile',
        'params': _params,
    }

    return _profile


def load_guest(auth: str, headset_id: str) -> ProfileRequest:
    """Loads an empty profile for a headset.

    Args:
        auth (str): The Cortex authentication token.
        headset_id (str): The headset ID.

    Read More:
        [loadGuestProfile](https://emotiv.gitbook.io/cortex-api/bci/loadguestprofile)

    Returns:
        ProfileRequest: The guest profile status.

    """

    _guest = {
        'id': ProfileID.GUEST,
        'jsonrpc': '2.0',
        'method': 'loadGuestProfile',
        'params': {
            'cortexToken': auth,
            'headset': headset_id,
        },
    }

    return _guest


def detection_info(
    detection: Literal['mentalCommand', 'facialExpression'],
) -> ProfileRequest:
    """Get the information about mental command or facial expression training.

    Args:
        detection (Literal['mentalCommand', 'facialExpression']): The detection type.

    Read More:
        [getDetectionInfo](https://emotiv.gitbook.io/cortex-api/bci/getdetectioninfo)

    Returns:
        ProfileRequest: The detection information.

    """
    _detection = {
        'id': ProfileID.DETECTION_INFO,
        'jsonrpc': '2.0',
        'method': 'getDetectionInfo',
        'params': {
            'detection': detection,
        },
    }

    return _detection
