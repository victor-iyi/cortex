"""Test for the mental_command module."""

from collections.abc import Callable

from typing import Any, Final, TypeAlias

from cortex.api.mental_command import active_action, brain_map, get_skill_rating, training_threshold, action_sensitivity
from cortex.api.id import MentalCommandID

import pytest

# Constants.
AUTH_TOKEN: Final[str] = '<AUTH-TOKEN>'
PROFILE_NAME: Final[str] = '<PROFILE-NAME>'
SESSION_ID: Final[str] = '<SESSION-ID>'

# Type aliases.
ResponseTemplate: TypeAlias = Callable[..., dict[str, Any]]


def test_get_active_action(response_template: ResponseTemplate) -> None:
    """Test getting the active mental command action."""
    actions = ['neutral', 'push', 'pull']

    assert active_action(AUTH_TOKEN, 'get', profile_name=PROFILE_NAME) == response_template(
        id=MentalCommandID.GET_ACTIVE_ACTION,
        method='mentalCommandActiveAction',
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'profile': PROFILE_NAME},
    )

    assert active_action(AUTH_TOKEN, 'get', session_id=SESSION_ID) == response_template(
        id=MentalCommandID.GET_ACTIVE_ACTION,
        method='mentalCommandActiveAction',
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'session': SESSION_ID},
    )

    with pytest.raises(AssertionError, match='status must be either "set" or "get".'):
        active_action(AUTH_TOKEN, 'invalid', profile_name=PROFILE_NAME)

    with pytest.raises(
        ValueError, match='Either profile_name or session_id must be provided, not both at the same time.'
    ):
        active_action(AUTH_TOKEN, 'get')
        active_action(AUTH_TOKEN, 'get', profile_name=PROFILE_NAME, session_id=SESSION_ID)

    assert active_action(AUTH_TOKEN, 'get', profile_name=PROFILE_NAME, actions=actions) == response_template(
        id=MentalCommandID.GET_ACTIVE_ACTION,
        method='mentalCommandActiveAction',
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'profile': PROFILE_NAME},
    )


def test_set_active_action(response_template: ResponseTemplate) -> None:
    """Test setting the active mental command action."""
    actions = ['neutral', 'push', 'pull']

    assert active_action(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME) == response_template(
        id=MentalCommandID.SET_ACTIVE_ACTION,
        method='mentalCommandActiveAction',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'profile': PROFILE_NAME},
    )

    assert active_action(AUTH_TOKEN, 'set', session_id=SESSION_ID) == response_template(
        id=MentalCommandID.SET_ACTIVE_ACTION,
        method='mentalCommandActiveAction',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'session': SESSION_ID},
    )

    with pytest.raises(AssertionError, match='status must be either "set" or "get".'):
        active_action(AUTH_TOKEN, 'invalid', profile_name=PROFILE_NAME)

    with pytest.raises(
        ValueError, match='Either profile_name or session_id must be provided, not both at the same time.'
    ):
        active_action(AUTH_TOKEN, 'set')
        active_action(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME, session_id=SESSION_ID)

    with pytest.raises(ValueError, match='You can have at most 4 actions.'):
        active_action(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME, actions=['neutral', 'push', 'pull', 'lift', 'drop'])

    assert active_action(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME, actions=actions) == response_template(
        id=MentalCommandID.SET_ACTIVE_ACTION,
        method='mentalCommandActiveAction',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'profile': PROFILE_NAME, 'actions': actions},
    )
    assert active_action(AUTH_TOKEN, 'set', session_id=SESSION_ID, actions=actions) == response_template(
        id=MentalCommandID.SET_ACTIVE_ACTION,
        method='mentalCommandActiveAction',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'session': SESSION_ID, 'actions': actions},
    )


def test_brain_map(response_template: ResponseTemplate) -> None:
    """Test mapping the profile name to the corresponding mental command brain."""
    assert brain_map(AUTH_TOKEN, profile_name=PROFILE_NAME) == response_template(
        id=MentalCommandID.BRAIN_MAP,
        method='mentalCommandBrainMap',
        params={'cortexToken': AUTH_TOKEN, 'profile': PROFILE_NAME},
    )

    assert brain_map(AUTH_TOKEN, session_id=SESSION_ID) == response_template(
        id=MentalCommandID.BRAIN_MAP,
        method='mentalCommandBrainMap',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID},
    )

    with pytest.raises(
        AssertionError, match='Either profile_name or session_id must be provided, not both at the same time.'
    ):
        brain_map(AUTH_TOKEN)

        brain_map(AUTH_TOKEN, profile_name=PROFILE_NAME, session_id=SESSION_ID)


def test_getting_skill_rating(response_template: ResponseTemplate) -> None:
    """Test getting the skill rating."""
    assert get_skill_rating(AUTH_TOKEN, profile_name=PROFILE_NAME) == response_template(
        id=MentalCommandID.SKILL_RATING,
        method='mentalCommandGetSkillRating',
        params={'cortexToken': AUTH_TOKEN, 'profile': PROFILE_NAME},
    )

    assert get_skill_rating(AUTH_TOKEN, session_id=SESSION_ID) == response_template(
        id=MentalCommandID.SKILL_RATING,
        method='mentalCommandGetSkillRating',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID},
    )

    with pytest.raises(
        AssertionError, match='Either profile_name or session_id must be provided, not both at the same time.'
    ):
        get_skill_rating(AUTH_TOKEN)

        get_skill_rating(AUTH_TOKEN, profile_name=PROFILE_NAME, session_id=SESSION_ID)

    assert get_skill_rating(AUTH_TOKEN, session_id=SESSION_ID, action='push') == response_template(
        id=MentalCommandID.SKILL_RATING,
        method='mentalCommandGetSkillRating',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID, 'action': 'push'},
    )
    assert get_skill_rating(AUTH_TOKEN, profile_name=PROFILE_NAME, action='pull') == response_template(
        id=MentalCommandID.SKILL_RATING,
        method='mentalCommandGetSkillRating',
        params={'cortexToken': AUTH_TOKEN, 'profile': PROFILE_NAME, 'action': 'pull'},
    )


def test_training_threshold(response_template: ResponseTemplate) -> None:
    """Test getting the training threshold."""
    assert training_threshold(AUTH_TOKEN, profile_name=PROFILE_NAME) == response_template(
        id=MentalCommandID.TRAINING_THRESHOLD,
        method='mentalCommandTrainingThreshold',
        params={'cortexToken': AUTH_TOKEN, 'profile': PROFILE_NAME},
    )

    assert training_threshold(AUTH_TOKEN, session_id=SESSION_ID) == response_template(
        id=MentalCommandID.TRAINING_THRESHOLD,
        method='mentalCommandTrainingThreshold',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID},
    )

    with pytest.raises(
        AssertionError, match='Either profile_name or session_id must be provided, not both at the same time.'
    ):
        training_threshold(AUTH_TOKEN)

        training_threshold(AUTH_TOKEN, profile_name=PROFILE_NAME, session_id=SESSION_ID)


def test_get_action_sensitivity(response_template: ResponseTemplate) -> None:
    """Test getting the action sensitivity."""
    values = [1, 2, 3, 4, 5]

    assert action_sensitivity(AUTH_TOKEN, 'get', profile_name=PROFILE_NAME) == response_template(
        id=MentalCommandID.ACTION_SENSITIVITY,
        method='mentalCommandActionSensitivity',
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'profile': PROFILE_NAME},
    )

    assert action_sensitivity(AUTH_TOKEN, 'get', session_id=SESSION_ID) == response_template(
        id=MentalCommandID.ACTION_SENSITIVITY,
        method='mentalCommandActionSensitivity',
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'session': SESSION_ID},
    )

    with pytest.raises(
        AssertionError, match='Either profile_name or session_id must be provided, not both at the same time.'
    ):
        action_sensitivity(AUTH_TOKEN, 'get')

        action_sensitivity(AUTH_TOKEN, 'get', profile_name=PROFILE_NAME, session_id=SESSION_ID)

    with pytest.raises(AssertionError, match='status must be either "set" or "get".'):
        action_sensitivity(AUTH_TOKEN, 'invalid', profile_name=PROFILE_NAME)
        action_sensitivity(AUTH_TOKEN, 'invalid', session_id=SESSION_ID)

    assert action_sensitivity(AUTH_TOKEN, 'get', profile_name=PROFILE_NAME, values=values) == response_template(
        id=MentalCommandID.ACTION_SENSITIVITY,
        method='mentalCommandActionSensitivity',
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'profile': PROFILE_NAME},
    )
    assert action_sensitivity(AUTH_TOKEN, 'get', session_id=SESSION_ID, values=values) == response_template(
        id=MentalCommandID.ACTION_SENSITIVITY,
        method='mentalCommandActionSensitivity',
        params={'cortexToken': AUTH_TOKEN, 'status': 'get', 'session': SESSION_ID},
    )


def test_set_action_sensitivity(response_template: ResponseTemplate) -> None:
    """Test setting the action sensitivity."""
    values = [1, 2, 3, 4, 5]

    assert action_sensitivity(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME) == response_template(
        id=MentalCommandID.ACTION_SENSITIVITY,
        method='mentalCommandActionSensitivity',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'profile': PROFILE_NAME},
    )

    assert action_sensitivity(AUTH_TOKEN, 'set', session_id=SESSION_ID) == response_template(
        id=MentalCommandID.ACTION_SENSITIVITY,
        method='mentalCommandActionSensitivity',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'session': SESSION_ID},
    )

    with pytest.raises(
        AssertionError, match='Either profile_name or session_id must be provided, not both at the same time.'
    ):
        action_sensitivity(AUTH_TOKEN, 'set')

        action_sensitivity(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME, session_id=SESSION_ID)

    with pytest.raises(AssertionError, match='status must be either "set" or "get".'):
        action_sensitivity(AUTH_TOKEN, 'invalid', profile_name=PROFILE_NAME)
        action_sensitivity(AUTH_TOKEN, 'invalid', session_id=SESSION_ID)

    assert action_sensitivity(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME, values=values) == response_template(
        id=MentalCommandID.ACTION_SENSITIVITY,
        method='mentalCommandActionSensitivity',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'profile': PROFILE_NAME, 'values': values},
    )
    assert action_sensitivity(AUTH_TOKEN, 'set', session_id=SESSION_ID, values=values) == response_template(
        id=MentalCommandID.ACTION_SENSITIVITY,
        method='mentalCommandActionSensitivity',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'session': SESSION_ID, 'values': values},
    )

    with pytest.raises(ValueError, match='values must be between 1 and 10.'):
        action_sensitivity(AUTH_TOKEN, 'set', profile_name=PROFILE_NAME, values=[5, 10, 15])
        action_sensitivity(AUTH_TOKEN, 'set', session_id=SESSION_ID, values=[5, 10, 15])
