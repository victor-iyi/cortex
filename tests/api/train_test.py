"""Test for train module."""

from collections.abc import Callable
from typing import Any, Final, TypeAlias

import pytest

from cortex.api.train import training, trained_signature_actions, training_time
from cortex.api.id import TrainingID


# Constants.
AUTH_TOKEN: Final[str] = 'xxx'
SESSION_ID: Final[str] = 'f3a35fd0-9163-4cc4-ab30-4ed224369f91'
PROFILE_NAME: Final[str] = 'cortex-v2-example'

# Type aliases.
APIRequest: TypeAlias = Callable[..., dict[str, Any]]


def test_training(api_request: APIRequest) -> None:
    """Test training."""
    assert training(AUTH_TOKEN, SESSION_ID, 'facialExpression', 'start', 'smile') == api_request(
        id=TrainingID.TRAINING,
        method='training',
        params={
            'cortexToken': AUTH_TOKEN,
            'session': SESSION_ID,
            'detection': 'facialExpression',
            'status': 'start',
            'action': 'smile',
        },
    )

    for status in ['start', 'accept', 'reject', 'reset', 'erase']:
        assert training(AUTH_TOKEN, SESSION_ID, 'facialExpression', status, 'smile') == api_request(
            id=TrainingID.TRAINING,
            method='training',
            params={
                'cortexToken': AUTH_TOKEN,
                'session': SESSION_ID,
                'detection': 'facialExpression',
                'status': status,
                'action': 'smile',
            },
        )

    for status in ['start', 'accept', 'reject', 'reset', 'erase']:
        assert training(AUTH_TOKEN, SESSION_ID, 'mentalCommand', status, 'push') == api_request(
            id=TrainingID.TRAINING,
            method='training',
            params={
                'cortexToken': AUTH_TOKEN,
                'session': SESSION_ID,
                'detection': 'mentalCommand',
                'status': status,
                'action': 'push',
            },
        )
    with pytest.raises(AssertionError):
        # AssertionError: detection must be either "facialExpression" or "mentalCommand".
        training(AUTH_TOKEN, SESSION_ID, 'invalid', 'start', 'smile')
        # AssertionError: status must be one of "start", "accept", "reject", "reset", "erase".
        training(AUTH_TOKEN, SESSION_ID, 'facialExpression', 'invalid', 'smile')


def test_trained_signature_actions(api_request: APIRequest) -> None:
    """Test trained_signature_actions."""
    assert trained_signature_actions(AUTH_TOKEN, 'facialExpression', profile_name=PROFILE_NAME) == api_request(
        id=TrainingID.SIGNATURE_ACTIONS,
        method='getTrainedSignatureActions',
        params={'cortexToken': AUTH_TOKEN, 'detection': 'facialExpression', 'profile': PROFILE_NAME},
    )

    assert trained_signature_actions(AUTH_TOKEN, 'facialExpression', session_id=SESSION_ID) == api_request(
        id=TrainingID.SIGNATURE_ACTIONS,
        method='getTrainedSignatureActions',
        params={'cortexToken': AUTH_TOKEN, 'detection': 'facialExpression', 'session': SESSION_ID},
    )

    with pytest.raises(AssertionError):
        # AssertionError: detection must be either "facialExpression" or "mentalCommand".
        trained_signature_actions(AUTH_TOKEN, 'invalid')

    with pytest.raises(ValueError):
        # AssertionError: Either profile_name or session_id must be provided, not both at the same time.
        trained_signature_actions(AUTH_TOKEN, 'facialExpression')
        trained_signature_actions(AUTH_TOKEN, 'facialExpression', profile_name='profile', session_id=SESSION_ID)


def test_training_time(api_request: APIRequest) -> None:
    """Test training_time."""
    assert training_time(AUTH_TOKEN, 'facialExpression', SESSION_ID) == api_request(
        id=TrainingID.TRAINING_TIME,
        method='getTrainingTime',
        params={'cortexToken': AUTH_TOKEN, 'detection': 'facialExpression', 'session': SESSION_ID},
    )

    assert training_time(AUTH_TOKEN, 'mentalCommand', SESSION_ID) == api_request(
        id=TrainingID.TRAINING_TIME,
        method='getTrainingTime',
        params={'cortexToken': AUTH_TOKEN, 'detection': 'mentalCommand', 'session': SESSION_ID},
    )

    with pytest.raises(AssertionError):
        # AssertionError: detection must be either "facialExpression" or "mentalCommand".
        training_time(AUTH_TOKEN, 'invalid', SESSION_ID)
