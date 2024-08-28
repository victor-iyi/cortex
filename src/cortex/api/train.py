"""## [Training workflow]

The training works that same for the mental command detection and the facial
expression detection. However, they don't use the same actions, events or controls.
So you should call [getDetectionInfo] to know what actions, controls and events
you can use for each detection.

Before you start a training, you must [subscribe] to the data stream "sys" to
receive the training events from Cortex. Then you can follow these steps:

    1. Start the training by calling [training] with the action you want to train
    and the **control "start"**.
    2. On the "sys" stream, you receive the **event "started"**.
    3. After a few seconds, you receive one of these two events:
        1. **Event "succeeded"**, the training is a success.
        Now you must accept it or reject it.
        2. **Event "failed"**, the data collected during the training is of poor
        quality, you must start over from the beginning.
    4. Call [training] with the **control "accept"** to add the training to the
    profile. Or you can use the **control "reject"** to reject this training,
    and then you must start over from the beginning.
    5. Cortex sends the **event "completed"** to confirm that the training was
    successfully completed.
    6. You should [save the profile] to persist this training. If you unload the
    profile without saving, then the training is lost.

After step 2, but before step 3, you can send the **control "reset"** to cancel the training.

[Training workflow]: https://emotiv.gitbook.io/cortex-api/bci#training-workflow
[getDetectionInfo]: https://emotiv.gitbook.io/cortex-api/bci/getdetectioninfo
[subscribe]: https://emotiv.gitbook.io/cortex-api/data-subscription/subscribe
[training]: https://emotiv.gitbook.io/cortex-api/bci/training
[save the profile]: https://emotiv.gitbook.io/cortex-api/bci/setupprofile

"""

from typing import Literal

from cortex.api.id import TrainingID
from cortex.api.types import TrainingRequest


def training(
    auth: str,
    session_id: str,
    detection: Literal['mentalCommand', 'facialExpression'],
    status: Literal['start', 'accept', 'reject', 'reset', 'erase'],
    action: str,
) -> TrainingRequest:
    """Train the mental command or facial expression.

    Args:
        auth (str): The Cortex authentication token.
        session_id (str): The session ID.
        detection (Literal['mentalCommand', 'facialExpression']): The detection type.
        status (Literal['start', 'accept', 'reject', 'reset', 'erase']): The training status.
            'start': Start new training for specified action.
            'accept': Accept a successful training and add it to the profile.
            'reject': Reject a successful training and do not add it to the profile.
            'reset': Cancel current training.
            'erase': Erase all training data from specified action.
        action (str): The action to train.

    Read More:
        [train](https://emotiv.gitbook.io/cortex-api/bci/train)

    Returns:
        TrainingRequest: The training status.

    """

    assert detection in [
        'mentalCommand',
        'facialExpression',
    ], 'detection must be either "mentalCommand" or "facialExpression".'

    assert status in [
        'start',
        'accept',
        'reject',
        'reset',
        'erase',
    ], 'status must be either "start", "accept", "reject", "reset", or "erase".'

    _training = {
        'id': TrainingID.TRAINING,
        'jsonrpc': '2.0',
        'method': 'training',
        'params': {
            'cortexToken': auth,
            'session': session_id,
            'detection': detection,
            'status': status,
            'action': action,
        },
    }

    return _training


def trained_signature_actions(
    auth: str,
    detection: Literal['mentalCommand', 'facialExpression'],
    *,
    profile_name: str | None = None,
    session_id: str | None = None,
) -> TrainingRequest:
    """Get the list of trained actions of a profile.

    Args:
        auth (str): The Cortex authentication token.
        detection (Literal['mentalCommand', 'facialExpression']): The detection type.

    Keyword Args:
        profile_name (str, optional): The profile name.
        session_id (str, optional): The session ID.

    Read More:
        [getTrainedSignatureActions](https://emotiv.gitbook.io/cortex-api/advanced-bci/gettrainedsignatureactions)

    Returns:
        TrainingRequest: The trained signature actions.

    """

    assert detection in [
        'mentalCommand',
        'facialExpression',
    ], 'detection must be either "mentalCommand" or "facialExpression".'

    _params = {
        'cortexToken': auth,
        'detection': detection,
    }
    if profile_name is not None:
        _params['profile'] = profile_name
    elif session_id is not None:
        _params['session'] = session_id
    else:
        raise ValueError('Either profile_name or session_id must be provided.')

    _trained = {
        'id': TrainingID.SIGNATURE_ACTIONS,
        'jsonrpc': '2.0',
        'method': 'getTrainedSignatureActions',
        'params': _params,
    }

    return _trained


def training_time(
    auth: str,
    detection: Literal['mentalCommand', 'facialExpression'],
    session_id: str,
) -> TrainingRequest:
    """Get the duration of a training.

    Args:
        auth (str): The Cortex authentication token.
        detection (Literal['mentalCommand', 'facialExpression']): The detection type.
        session_id (str): The session ID.

    Read More:
        [getTrainingTime](https://emotiv.gitbook.io/cortex-api/advanced-bci/gettrainingtime)

    Returns:
        TrainingRequest: The training time.

    """

    assert detection in [
        'mentalCommand',
        'facialExpression',
    ], 'detection must be either "mentalCommand" or "facialExpression".'

    _training_time = {
        'id': TrainingID.TRAINING_TIME,
        'jsonrpc': '2.0',
        'method': 'getTrainingTime',
        'params': {
            'cortexToken': auth,
            'detection': detection,
            'session': session_id,
        },
    }

    return _training_time
