"""Get and set sensitivity of mental command action in live mode.

Getting Started:
    - Please reference https://emotiv.gitbook.io/cortex-api/ for more information.
    - Connect your headset with dongle or bluetooth. You can see the headset via Emotiv Launcher.
    - Please make sure the client_id and client_secret are set and correct before starting.
    - The method `on_create_session_done`, `on_query_profile_done`, `on_load_unload_profile_done` will help
      handle crate and load a profile automatically. So you shouldn't modify them.
    - After the profile is loaded. We test some advanced BCI api such as: mentalCommandActiveAction,
      mentalCommandActionSensitivity.

Result:
    - You can run live mode with trained profile with the data below:
        ```
        {'action': 'push', 'power': 0.85, 'time': 1234567890.1234}
        {'action': 'pull', 'power': 0.55, 'time': 1234567890.1234}
        ```

"""
# pylint: disable=unused-argument

from typing import Any
from cortex import Headset, ErrorCode, logger


class LiveAdvance:
    """Get and set sensitivity of mental command action in live mode.

    Attributes:
        headset (Headset): The headset object to connect to the BCI API.
        profile_name (str): The profile name to be trained.
        export_folder (str): The folder to export the trained profile.

    Methods:
        start(profile_name: str, headset_id: str = '') -> None:
            Start training the mental command training.
        load_profile(profile_name: str) -> None:
            Load the profile to be trained.
        unload_profile(profile_name: str) -> None:
            Unload the profile after training.
        save_profile(profile_name: str) -> None:
            Save the profile after training.
        subscribe(streams: list[str]) -> None:
            Subscribe to the data streams.
        get_active_action(profile_name: str) -> None:
            Get the active action of the profile.
        get_sensitivity(profile_name: str) -> None:
            Get the sensitivity of the mental command actions.
        set_sensitivity(profile_name: str, values: list[str]) -> None:
            Set the sensitivity of the mental command actions.

    Callback Methods:
        on_create_session_done(*args: Any, **kwargs: Any) -> None:
            Callback method when the session is created.
        on_query_profile_done(*args: Any, **kwargs: Any) -> None:
            Callback method when the profile is queried.
        on_load_unload_profile_done(*args: Any, **kwargs: Any) -> None:
            Callback method when the profile is loaded or unloaded.
        on_save_profile_done(*args: Any, **kwargs: Any) -> None:
            Callback method when the profile is saved.
        on_new_com_data(*args: Any, **kwargs: Any) -> None:
            Callback method when new mental command data is received.
        on_get_mc_active_action_done(*args: Any, **kwargs: Any) -> None:
            Callback method when the active action of the profile is received.
        on_mc_action_sensitivity_done(*args: Any, **kwargs: Any) -> None:
            Callback method when the sensitivity of the mental command actions is received.
        on_inform_error(*args: Any, **kwargs: Any) -> None:
            Callback method when an error is received.

    """

    def __init__(self, client_id: str, client_secret: str, **kwargs: Any) -> None:
        """Initialize the LiveAdvance class."""
        self._headset = Headset(client_id, client_secret, **kwargs)

        self._headset.bind(create_session_done=self.on_create_session_done)
        self._headset.bind(query_profile_done=self.on_query_profile_done)
        self._headset.bind(load_unload_profile_done=self.on_load_unload_profile_done)
        self._headset.bind(save_profile_done=self.on_save_profile_done)
        self._headset.bind(new_com_data=self.on_new_com_data)
        self._headset.bind(get_mc_active_action_done=self.on_get_mc_active_action_done)
        self._headset.bind(mc_action_sensitivity_done=self.on_mc_action_sensitivity_done)
        self._headset.bind(inform_error=self.on_inform_error)

        self.profile_name: str = ''
        self.export_folder: str = '.'

    def start(self, profile_name: str, headset_id: str = '') -> None:
        """Start training the mental command training.

        To start the training process, follow these workflow steps:
            1. Check access right -> authorize -> connect headset -> create session.
            2. Query profile -> get current profile -> load/create profile.
            3. Get MC active action -> get MC sensitivity -> set new MC sensitivity -> save profile.
            4. Subscribe 'com' data to show live MC data.

        Args:
            profile_name (str): The profile name to be trained.
            headset_id (str, optional): The headset ID you want to work with.
                If the headset id is empty, the first headset in the list will be set
                as wanted headset. Defaults to ''.

        """
        if profile_name == '':
            raise ValueError('Profile name cannot be empty.')

        self.profile_name = profile_name
        self._headset.set_profile(profile_name)

        if headset_id != '':
            self._headset.set_headset(headset_id)

        self._headset.open()

    def load_profile(self, profile_name: str) -> None:
        """Load the profile to be trained.

        Args:
            profile_name (str): The profile name to be trained.

        """
        self._headset.setup_profile(status='load', profile_name=profile_name)

    def unload_profile(self, profile_name: str) -> None:
        """Unload the profile after training.

        Args:
            profile_name (str): The profile name to be unloaded.

        """
        self._headset.setup_profile(status='unload', profile_name=profile_name)

    def save_profile(self, profile_name: str) -> None:
        """Save the profile after training.

        Args:
            profile_name (str): The profile name to be saved.

        """
        self._headset.setup_profile(status='save', profile_name=profile_name)

    def subscribe(self, streams: list[str]) -> None:
        """Subscribe to the data streams.

        Args:
            streams (list[str]): The data streams to subscribe to.

        """
        self._headset.subscribe(streams)

    def get_active_action(self, profile_name: str) -> None:
        """Get the active action of the profile.

        Note:
            Maximum for mental command actions are activated. This doesn't include "neutral".

        Args:
            profile_name (str): The profile name to get the active action.

        """
        self._headset.get_mental_command_active_action(profile_name=profile_name)

    def get_sensitivity(self, profile_name: str) -> None:
        """Get the sensitivity of the mental command actions.

        Args:
            profile_name (str): The profile name to get the sensitivity.

        """
        self._headset.get_mental_command_action_sensitive(profile_name=profile_name)

    def set_sensitivity(self, profile_name: str, values: list[str]) -> None:
        """Set the sensitivity of the mental command actions.

        Note:
            The order of the values must follow the order of the active actions,
            as returned by get_mental_command_active_action.

        Example:
            ['neutral', 'push', 'pull', 'life', 'drop'] -> sensitivity [7, 8, 3, 6]
                <=> push: 7, pull: 8, life: 3, drop: 6
            ['neutral', 'push', 'pull'] -> sensitivity [7, 8, 5, 5]
                <=> push: 7, pull: 8, others resvered.

        Args:
            profile_name (str): The profile name to set the sensitivity.
            values (list[str]): The list of sensitivity values to set.

        """
        self._headset.set_mental_command_action_sensitive(profile_name=profile_name, values=values)

    # +-----------------------------------------------------------------------+
    # |                           Callback Methods                            |
    # +-----------------------------------------------------------------------+

    def on_create_session_done(self, *args: Any, **kwargs: Any) -> None:
        """Callback method when the session is created."""
        logger.debug('------- on_create_session_done -------')
        self._headset.query_profile()

    def on_query_profile_done(self, *args: Any, **kwargs: Any) -> None:
        """Callback method when the profile is queried."""
        logger.debug('------- on_query_profile_done -------')
        self.profile_lists = kwargs.get('data', [])
        if self.profile_name in self.profile_lists:
            # The profile exists.
            self._headset.get_current_profile()
        else:
            # Create profile.
            self._headset.setup_profile(status='create', profile_name=self.profile_name)

    def on_load_unload_profile_done(self, *args: Any, **kwargs: Any) -> None:
        """Callback method when the profile is loaded or unloaded."""
        logger.debug('------- on_load_unload_profile_done -------')
        is_loaded = kwargs.get('isLoaded', False)
        if is_loaded:
            # Subscribe sys stream to recieve Training Event.
            self._headset.subscribe(['sys'])
        else:
            logger.warning(f'Profile {self.profile_name} is not loaded.')
            self.profile_name = ''
            # Close socket.
            self._headset.close()

    def on_save_profile_done(self, *args: Any, **kwargs: Any) -> None:
        """Callback method when the profile is saved."""
        logger.debug('------- on_save_profile_done -------')
        logger.info(f'Profile {self.profile_name} is saved.')
        self.unload_profile(self.profile_name)

    def on_new_com_data(self, *args: Any, **kwargs: Any) -> None:
        """Callback method when new mental command data is received."""
        logger.debug(f'New mental command data: {kwargs.get("data", {})}')
        data = kwargs.get('data')
        logger.debug(data)

    def on_get_mc_active_action_done(self, *args: Any, **kwargs: Any) -> None:
        """Callback method when the active action of the profile is received."""
        logger.debug('------- on_get_mc_active_action_done -------')
        logger.debug(kwargs.get('data'))
        self.get_sensitivity(self.profile_name)

    def on_mc_action_sensitivity_done(self, *args: Any, **kwargs: Any) -> None:
        """Callback method when the sensitivity of the mental command actions is received."""
        logger.debug('------- on_mc_action_sensitivity_done -------')
        data = kwargs.get('data')
        logger.debug(data)

        if isinstance(data, list):
            # Set new sensitivity.
            self.set_sensitivity(self.profile_name, values=['7', '8', '3', '6'])
        else:
            # Set sensitivity done -> save profile.
            self.save_profile(self.profile_name)

    def on_inform_error(self, *args: Any, **kwargs: Any) -> None:
        """Callback method when an error is received."""
        error_data = kwargs.get('error_data')
        logger.debug(error_data)

        code = error_data['code']  # type: ignore[index]
        message = error_data['message']  # type: ignore[index]

        if code == ErrorCode.ERR_PROFILE_ACCESS_DENIED:
            logger.error(f'{message}. Disconnect headset to fix this issue for next use.')
            self._headset.disconnect()

    @property
    def headset(self) -> Headset:
        """The headset object to connect to the BCI API."""
        return self._headset


def main() -> None:
    """Start training the mental command training."""
    import os

    # Please fill your application client ID and client secret.
    client_id = os.getenv('EMOTIV_CLIENT_ID') or ''
    client_secret = os.getenv('EMOTIV_CLIENT_SECRET') or ''

    live_advance = LiveAdvance(client_id, client_secret)

    trained_profile_name = ''  # The profile name you want to train.
    live_advance.start(profile_name=trained_profile_name)


if __name__ == '__main__':
    main()
