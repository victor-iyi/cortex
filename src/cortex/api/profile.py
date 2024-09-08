"""## Profile_.

A profile is a persistent object that stores training data for the facial expression and mental command detections. A
profile belongs to a user and is synchronized to the EMOTIV cloud.

You can use queryProfile_ to list the profiles of the current user. Use setupProfile_ to manage the profiles, and also
to load or unload a profile for a headset. You can use training_ to add training data to a profile.

.. _Profile: https://emotiv.gitbook.io/cortex-api/bci#profile
.. _queryProfile: https://emotiv.gitbook.io/cortex-api/bci/queryprofile
.. _setupProfile: https://emotiv.gitbook.io/cortex-api/bci/setupprofile
.. _training: https://emotiv.gitbook.io/cortex-api/bci/training

"""

from typing import Literal

from cortex.api.id import ProfileID
from cortex.api.types import BaseRequest


def query_profile(auth: str) -> BaseRequest:
    """Query the list of all training profile.

    Read More:
        [queryProfile](https://emotiv.gitbook.io/cortex-api/bci/queryprofile)

    Returns:
        BaseRequest: The query profile request.

    """
    _query = {'id': ProfileID.QUERY, 'jsonrpc': '2.0', 'method': 'queryProfile', 'params': {'cortexToken': auth}}

    return _query


def current_profile(auth: str, headset_id: str) -> BaseRequest:
    """Get the current training profile that is loaded for a specific headset.

    Args:
        auth (str): The Cortex authentication token.
        headset_id (str): The headset ID.

    Read More:
        [getCurrentProfile](https://emotiv.gitbook.io/cortex-api/bci/getcurrentprofile)

    Returns:
        BaseRequest: The current profile status.

    """
    _profile = {
        'id': ProfileID.CURRENT,
        'jsonrpc': '2.0',
        'method': 'getCurrentProfile',
        'params': {'cortexToken': auth, 'headset': headset_id},
    }

    return _profile


def setup_profile(
    auth: str,
    status: Literal['create', 'load', 'unload', 'save', 'rename', 'delete'],
    profile_name: str,
    *,
    headset_id: str | None = None,
    new_profile_name: str | None = None,
) -> BaseRequest:
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
        BaseRequest: The profile setup status.

    """
    assert status in [
        'create',
        'load',
        'unload',
        'save',
        'rename',
        'delete',
    ], 'status must be one of create, load, unload, save, rename, delete.'

    if status == 'rename' and new_profile_name is None:
        raise ValueError('new_profile_name must be provided when status is "rename".')

    if status in ('create', 'load', 'unload', 'save') and headset_id is None:
        raise ValueError('headset_id must be provided when status is "create", "load", "unload", or "save".')

    _params = {'cortexToken': auth, 'status': status, 'profile': profile_name}

    if headset_id is not None and status in ('create', 'load', 'unload', 'save'):
        _params['headset'] = headset_id

    if new_profile_name is not None and status == 'rename':
        _params['newProfileName'] = new_profile_name

    _profile = {'id': ProfileID.SETUP, 'jsonrpc': '2.0', 'method': 'setupProfile', 'params': _params}

    return _profile


def load_guest(auth: str, headset_id: str) -> BaseRequest:
    """Loads an empty profile for a headset.

    Args:
        auth (str): The Cortex authentication token.
        headset_id (str): The headset ID.

    Read More:
        [loadGuestProfile](https://emotiv.gitbook.io/cortex-api/bci/loadguestprofile)

    Returns:
        BaseRequest: The guest profile status.

    """
    _guest = {
        'id': ProfileID.GUEST,
        'jsonrpc': '2.0',
        'method': 'loadGuestProfile',
        'params': {'cortexToken': auth, 'headset': headset_id},
    }

    return _guest


def detection_info(detection: Literal['mentalCommand', 'facialExpression']) -> BaseRequest:
    """Get the information about mental command or facial expression training.

    Args:
        detection (Literal['mentalCommand', 'facialExpression']): The detection type.

    Read More:
        [getDetectionInfo](https://emotiv.gitbook.io/cortex-api/bci/getdetectioninfo)

    Returns:
        BaseRequest: The detection information.

    """
    assert detection in [
        'mentalCommand',
        'facialExpression',
    ], 'detection must be either "mentalCommand" or "facialExpression".'

    _detection = {
        'id': ProfileID.DETECTION_INFO,
        'jsonrpc': '2.0',
        'method': 'getDetectionInfo',
        'params': {'detection': detection},
    }

    return _detection
