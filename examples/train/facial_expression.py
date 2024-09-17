"""Use BCI AI to detect facial expressions.

Getting Started:
    - Please reference https://emotiv.gitbook.io/cortex-api/ for more information.
    - Connect your headset with dongle or bluetooth. You can see the headset via Emotiv Launcher.
    - Please make sure the client_id and client_secret are set and correct before starting.
    - The method `on_create_session_done`, `on_query_profile_done`, `on_load_unload_profile_done` will help
      handle crate and load a profile automatically. So you shouldn't modify them.
    - The method `on_new_sys_data` and `on_new_data_labels` will help handle the training event automatically.
      You can modify these methods to control the training process, such as: reject the training or use advanced
      BCI APIs.

Result:
    - Train facial expression action.

"""
# pylint: disable=unused-argument

from enum import StrEnum
from typing import Any, Literal

from cortex import ErrorCode, Headset, logger


class TrainEvent(StrEnum):
    """Training event for facial expression."""

    SUCCEEDED = 'FE_Succeeded'
    COMPLETED = 'FE_Completed'
    FAILED = 'FE_Failed'
    REJECTED = 'FE_Rejected'


class FacialExpressionTrainer:
    """Train the BCI API to detect facial expressions.

    Attributes:
        headset: The headset object to connect to the BCI API.
        action_idx (int): The index of the facial expression action.
        actions (list[str]): The list of facial expressions to be trained.
        profile_name (str): The profile name to be trained.
        profile_lists (list[str]): The list of profiles.

    Methods:
        start: Start training the BCI API.
        subscribe_data: Subscribe to the data streams.
        load_profile: Load the profile to be trained.
        unload_profile: Unload the profile after training.
        save_profile: Save the profile after training.
        train_fe_action: Train the facial expression action.

    Callback Methods:
        on_create_session_done: Callback method when the session is created.
        on_query_profile_done: Callback method when the profile is queried.
        on_load_unload_profile_done: Callback method when the profile is loaded or unloaded.
        on_save_profile_done: Callback method when the profile is saved.
        on_inform_error: Callback method when an error is received.
        on_new_sys_data: Callback method when new sys data is received.
        on_new_data_labels: Callback method when new data labels are received.

    """

    def __init__(self, client_id: str, client_secret: str, **kwargs: Any) -> None:
        """Initialize the facial expression training."""
        self._headset = Headset(client_id=client_id, client_secret=client_secret, debug_mode=True, **kwargs)

        # Bind callback methods.
        self._headset.bind(create_session_done=self.on_create_session_done)
        self._headset.bind(query_profile_done=self.on_query_profile_done)
        self._headset.bind(load_unload_profile_done=self.on_load_unload_profile_done)
        self._headset.bind(save_profile_done=self.on_save_profile_done)
        self._headset.bind(new_data_labels=self.on_new_data_labels)
        self._headset.bind(new_sys_data=self.on_new_sys_data)
        self._headset.bind(inform_error=self.on_inform_error)

        self.action_idx: int = 0
        self.actions: list[str] = []
        self.profile_name: str = ''
        self.profile_lists: list[str] = []

    def start(self, profile_name: str, actions: list[str], headset_id: str = '') -> None:
        """Start training the BCI API.

        The training process follows these workflow steps:
            1. Check access right -> authorize -> connect headset -> create session.
            2. Query profile -> get current profile -> load/create profile -> subscribe sys
            3. Start and accept FE action training in the action list one by one.

        Args:
            profile_name (str): The profile name to be trained.
            actions (list[str]): The list of facial expressions to be trained.
            headset_id (str, optional): The headset ID you want to work with.
                If the headset id is empty, the first headset in the list will be set
                as wanted headset. Defaults to ''.

        """
        if profile_name == '':
            raise ValueError('Profile name cannot be empty.')

        self.profile_name = profile_name
        self.actions = actions
        self.action_idx = 0

        self._headset.set_profile(profile_name)

        if headset_id != '':
            self._headset.set_headset(headset_id)

        self._headset.open()

    def subscribe_data(self, streams: list[str]) -> None:
        """Subscribe to the data streams.

        The data streams are:
            'com': Mental Command
            'fac': Facial Expression
            'sys': Training Event

        Args:
            streams (list[str]): The list of data streams to be subscribed.
                Example: ['sys', 'fac']

        """
        self._headset.subscribe(streams)

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

    def train_fe_action(self, status: Literal['accept', 'reject', 'start', 'erase', 'reset']) -> None:
        """Train the facial expression action.

        Args:
            status (Literal['accept', 'reject', 'start', 'erase', 'reset']): The status of the training.
                'accept': Accept the training.
                'reject': Reject the training.
                'start': Start the training.
                'erase': Erase the training.
                'reset': Reset the training.

        """
        if self.action_idx < len(self.actions):
            action = self.actions[self.action_idx]
            logger.debug(f'------- train_fe_action: {action}: {status} -------')
            self._headset.train_request(detection='facialExpression', action=action, status=status)
        else:
            # Save profile after training.
            self.save_profile(self.profile_name)
            self.action_idx = 0  # reset action index.

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

    def on_inform_error(self, *args: Any, **kwargs: Any) -> None:
        """Callback method when an error is received."""
        error_data = kwargs.get('error_data', {})
        logger.error(error_data)

        code = error_data['code']
        message = error_data['message']

        if code == ErrorCode.ERR_PROFILE_ACCESS_DENIED:
            logger.error(f'{message}. Disconnect headset to fix this issue for next use.')
            self._headset.disconnect()

    def on_new_sys_data(self, *args: Any, **kwargs: Any) -> None:
        """Callback method when new sys data is received."""
        logger.debug('------- on_new_sys_data -------')
        data = kwargs.get('data')
        train_event = data[1]  # type: ignore[index]
        action = self.actions[self.action_idx]
        logger.debug(f'------- on_new_sys_data: {action}: {train_event} -------')

        if train_event == TrainEvent.SUCCEEDED:
            # Train action successful. You can accept the training to complete or reject the training.
            self.train_fe_action('accept')
        elif train_event == TrainEvent.FAILED:
            self.train_fe_action('reject')
        elif train_event == TrainEvent.COMPLETED or train_event == TrainEvent.REJECTED:
            # Training complete. Move to next action.
            self.action_idx += 1
            self.train_fe_action('start')
        else:
            logger.warning(f'Unknown train event: {train_event}')

    def on_new_data_labels(self, *args: Any, **kwargs: Any) -> None:
        """Callback method when new data labels are received."""
        logger.debug('------- on_new_data_labels -------')
        data = kwargs.get('data')
        logger.debug(f'Data labels: {data}')
        if data['streamName'] == 'sys':  # type: ignore[index]
            # Subscribe sys event sucessful.
            # Start training.
            self.train_fe_action(status='start')

    @property
    def headset(self) -> Headset:
        """The headset object to connect to the BCI API."""
        return self._headset


def main() -> None:
    """Main function to start the training."""
    import os

    from dotenv import load_dotenv

    load_dotenv()

    # TODO: Please fill your application client ID and client secret.
    client_id = os.getenv('EMOTIV_CLIENT_ID') or '<your-client-id>'
    client_secret = os.getenv('EMOTIV_CLIENT_SECRET') or '<your-client-secret>'

    # Initialize training.
    trainer = FacialExpressionTrainer(client_id=client_id, client_secret=client_secret)

    # Name of training profile.
    profile_name = 'test'  # TODO: set your profile name. If the profile doesn't exist, it will be created.

    # List of actions to be trained.
    actions = ['neutral', 'surprise', 'smile']
    trainer.start(profile_name=profile_name, actions=actions)


if __name__ == '__main__':
    main()
