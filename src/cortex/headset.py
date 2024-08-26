import json
from typing import Literal

from cortex.api.headset import (
    make_connection,
    query_headset,
    subscription,
)
from cortex.api.mental_command import (
    action_sensitivity,
    active_action,
    brain_map,
    training_threshold,
)
from cortex.api.profile import (
    current_profile,
    query_profile,
    setup_profile,
)
from cortex.cortex import Cortex
from cortex.logging import logger


class Headset(Cortex):
    def __init__(self, *args: str, **kwargs: bool | str) -> None:
        super().__init__(*args, **kwargs)

    def connect(
        self,
        mappings: dict[str, str] | None = None,
        connection_type: str | None = None,
    ) -> None:
        """Connect to the headset."""
        logger.info('--- Connecting to the headset ---')

        connection = make_connection(
            command='connect',
            headset_id=self.headset_id,
            mappings=mappings,
            connection_type=connection_type,
        )

        # If debug mode is enabled, print the connection.
        logger.debug('Connecting to the headset.')
        logger.debug(connection)

        self._ws.send(json.dumps(connection, indent=4))

    def disconnect(
        self,
        mappings: dict[str, str] | None = None,
        connection_type: str | None = None,
    ) -> None:
        """Disconnect from the headset."""
        logger.info('--- Disconnecting from the headset ---')

        connection = make_connection(
            command='disconnect',
            headset_id=self.headset_id,
            mappings=mappings,
            connection_type=connection_type,
        )

        # If debug mode is enabled, print the connection.
        logger.debug('Disconnecting from the headset.')
        logger.debug(connection)

        self._ws.send(json.dumps(connection, indent=4))

    def query_headset(self) -> None:
        """Query the headset."""
        logger.info('--- Querying the headset ---')

        _query_headset = query_headset(headset_id=self.headset_id)

        # If debug mode is enabled, print the query.
        logger.debug('Querying the headset.')
        logger.debug(query_headset)

        self._ws.send(json.dumps(_query_headset, indent=4))

    def subscribe(self, streams: list[str]) -> None:
        """Subscribe to one or more data stream.

        Args:
            streams (list[str]): The data streams to subscribe to.

        Read More:
            [subscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/subscribe)

        """
        logger.info('--- Subscribing to the headset ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _request = subscription(
            auth=self._auth,
            session_id=self.session_id,
            streams=streams,
            method='subscribe',
        )

        # If debug mode is enabled, print the subscription request.
        logger.debug('Subscribe request:')
        logger.debug(_request)

        self._ws.send(json.dumps(_request, indent=4))

    def unsubscribe(self, streams: list[str]) -> None:
        """Unsubscribe from one or more data stream.

        Args:
            streams (list[str]): The data streams to unsubscribe from.

        Read More:
            [unsubscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/unsubscribe)

        """
        logger.info('--- Unsubscribing from the headset ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _request = subscription(
            auth=self._auth,
            session_id=self.session_id,
            streams=streams,
            method='unsubscribe',
        )

        # If debug mode is enabled, print the subscription request.
        logger.debug('Unsubscribe request:')
        logger.debug(_request)

        self._ws.send(json.dumps(_request, indent=4))

    def query_profile(self) -> None:
        """Query the profile."""
        logger.info('--- Querying the profile ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        query = query_profile(auth=self._auth)

        # If debug mode is enabled, print the query.
        logger.debug('Querying the profile.')
        logger.debug(query)

        self._ws.send(json.dumps(query, indent=4))

    def get_current_profile(self) -> None:
        """Get the current profile."""
        logger.info('--- Getting the current profile ---')

        if not self._auth and not self.headset_id:
            raise ValueError('No authentication token or headset ID. Please connect to Cortex first.')

        current = current_profile(
            auth=self._auth,
            headset_id=self.headset_id,
        )

        # If debug mode is enabled, print the current profile.
        logger.debug('Getting the current profile.')
        logger.debug(current)

        self._ws.send(json.dumps(current, indent=4))

    def setup_profile(
        self,
        status: Literal['create', 'load', 'unload', 'save', 'rename', 'delete'],
        profile_name: str,
        *,
        new_profile_name: str | None = None,
    ) -> None:
        """Setup a profile.

        Args:
            status (Literal['create', 'load', 'unload', 'save', 'rename', 'delete']):
                The status of the profile.
            profile_name (str): The profile name.

        Keyword Args:
            new_profile_name (str, optional): The new profile name.
                Only if the status is "rename".

        """
        logger.info('--- Setting up the profile ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex')

        setup = setup_profile(
            auth=self._auth,
            status=status,
            profile_name=profile_name,
            headset_id=self.headset_id,
            new_profile_name=new_profile_name,
        )

        # If debug mode is enabled, print the setup.
        logger.debug('Setting up the profile.')
        logger.debug(setup)

        self._ws.send(json.dumps(setup, indent=4))

    def get_mental_command_action_sensitive(self, profile_name: str) -> None:
        """Get the mental command action sensitivity."""
        logger.info('--- Getting mental command action sensitivity ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        sensitivity = action_sensitivity(
            auth=self._auth,
            profile_name=profile_name,
            status='get',
        )

        # If debug mode is enabled, print the sensitivity.
        logger.debug('Getting mental command action sensitivity.')
        logger.debug(sensitivity)

        self._ws.send(json.dumps(sensitivity, indent=4))

    def set_mental_command_action_sensitive(
        self,
        profile_name: str,
        values: list[int],
    ) -> None:
        """Set the mental command action sensitivity."""
        logger.info('--- Setting mental command action sensitivity ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        sensitivity = action_sensitivity(
            auth=self._auth,
            profile_name=profile_name,
            session_id=self.session_id,
            values=values,
            status='set',
        )

        # If debug mode is enabled, print the sensitivity.
        logger.debug('Setting mental command action sensitivity.')
        logger.debug(sensitivity)

        self._ws.send(json.dumps(sensitivity, indent=4))

    def get_mental_command_active_action(self, profile_name: str) -> None:
        """Get the active mental command action."""
        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        active = active_action(
            auth=self._auth,
            status='get',
            profile_name=profile_name,
        )

        # If debug mode is enabled, print the active action.
        logger.debug('Getting mental command active action.')
        logger.debug(active)

        self._ws.send(json.dumps(active, indent=4))

    def set_mental_command_active_action(
        self,
        actions: list[str],
    ) -> None:
        """Set the active mental command action."""
        logger.info('--- Setting mental command active action ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        active = active_action(
            auth=self._auth,
            status='set',
            session_id=self.session_id,
            actions=actions,
        )

        # If debug mode is enabled, print the active action.
        logger.debug('Setting mental command active action.')
        logger.debug(active)

        self._ws.send(json.dumps(active, indent=4))

    def get_mental_command_brain_map(self, profile_name: str) -> None:
        """Get the mental command brain map."""
        logger.info('--- Getting mental command brain map ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        brain = brain_map(
            auth=self._auth,
            session_id=self.session_id,
            profile_name=profile_name,
        )

        # If debug mode is enabled, print the brain map.
        logger.debug('Getting mental command brain map.')
        logger.debug(brain)

        self._ws.send(json.dumps(brain, indent=4))

    def get_mental_command_training_threshold(self, profile_name: str) -> None:
        """Get the mental command training threshold."""
        logger.info('--- Getting mental command training threshold ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        threshold = training_threshold(
            auth=self._auth,
            profile_name=profile_name,
            session_id=self.session_id,
        )

        # If debug mode is enabled, print the training threshold.
        logger.debug('Getting mental command training threshold.')
        logger.debug(threshold)

        self._ws.send(json.dumps(threshold, indent=4))
