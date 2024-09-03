"""Subscribe to data stream like: EEG, motion, performance metrics and band power.

Getting Started:
    - Please reference https://emotiv.gitbook.io/cortex-api/ for more information.
    - Connect your headset with dongle or bluetooth. You can see the headset via Emotiv Launcher.
    - Please make sure the client_id and client_secret are set and correct before starting.
    - In case you borrow license from others, you need to add `license = 'xxx-yyy-zzz' as init parameter.

Result:
    - The data labels will be retrieved at `on_new_data_labels`.
    - The data will be retrieved at `on_new_[dataStream]_data`.

"""
# pylint: disable=unused-argument
# noqa: E501

from typing import Any

from cortex import Headset, logger


class Subscribe:
    """Subscribe to data stream like: EEG, motion, performance metrics and band power.

    Attributes:
        streams (list[str]): The data streams to subscribe to.
        headset (Headset): The headset object to connect to the BCI API.

    Methods:
        start(streams: list[str], headset_id: str = '') -> None:
            Start subscribing to the data streams.
        subscribe(streams: list[str]) -> None:
            Subscribe to the data streams.
        unsubscribe(streams: list[str]) -> None:
            Unsubscribe from the data streams.

    Callback Methods:
        on_new_data_labels(*args: Any, **kwargs: Any) -> None:
            Handle the new data labels of subscribed data.
        on_new_eeg_data(*args: Any, **kwargs: Any) -> None:
            Handle the new EEG data.
        on_new_mot_data(*args: Any, **kwargs: Any) -> None:
            Handle the new motion data.
        on_new_met_data(*args: Any, **kwargs: Any) -> None:
            Handle the new performance metrics data.
        on_new_pow_data(*args: Any, **kwargs: Any) -> None:
            Handle the new band power data.
        on_create_session_done(*args: Any, **kwargs: Any) -> None:
            Handle the creation of a session.
        on_inform_error(*args: Any, **kwargs: Any) -> None:
            Handle the error information.
    """

    def __init__(self, client_id: str, client_secret: str, **kwargs: Any) -> None:
        """Initialize the Subscribe class."""
        self._headset = Headset(client_id, client_secret, **kwargs)

        self._headset.bind(create_session_done=self.on_create_session_done)
        self._headset.bind(inform_error=self.on_inform_error)
        self._headset.bind(new_data_labels=self.on_new_data_labels)
        self._headset.bind(new_eeg_data=self.on_new_eeg_data)
        self._headset.bind(new_mot_data=self.on_new_mot_data)
        self._headset.bind(new_met_data=self.on_new_met_data)
        self._headset.bind(new_pow_data=self.on_new_pow_data)

        self.streams: list[str] = []

    def start(self, streams: list[str], headset_id: str = '') -> None:
        """Start subscribing to the data streams.

        To start subscribing to the data streams, follow these workflow steps:
            1. Check access right -> authorize -> connect headset -> create session.
            2. Subscribe to the data streams.
            'eeg': EEG
            'motion': Motion
            'dev': Device information
            'met': Performance metrics
            'pow': Band power
            'eq': EEG Quality

        Args:
            streams (list[str]): The data streams to subscribe to.
            headset_id (str, optional): The headset ID you want to work with.
                If the headset id is empty, the first headset in the list will be set
                as wanted headset. Defaults to ''.

        """
        self.streams = streams

        if headset_id != '':
            self._headset.set_headset(headset_id)

        self._headset.open()

    def subscribe(self, streams: list[str]) -> None:
        """Subscribe to the data streams.

        Args:
            streams (list[str]): The data streams to subscribe to.

        """
        self._headset.subscribe(streams)

    def unsubscribe(self, streams: list[str]) -> None:
        """Unsubscribe from the data streams.

        Args:
            streams (list[str]): The data streams to unsubscribe from.

        """
        self._headset.unsubscribe(streams)

    # +-----------------------------------------------------------------------+
    # |                           Callback Methods                            |
    # +-----------------------------------------------------------------------+

    def on_new_data_labels(self, *args: Any, **kwargs: Any) -> None:
        """Handle the new data labels of subscribed data.

        Example:
        ```
            eeg: ['COUNTER', 'INTERPOLATED', 'AF3', 'T7', 'Pz', 'T8', 'AF4', 'RAW_CQ', 'MARKER_HARDWARE']
            motion: ['COUNTER_MEMS', 'INTERPOLATED_MEMS', 'Q0', 'Q1', 'Q2', 'Q3', 'ACCX', 'ACCY', 'ACCZ',
                     'MAGX', 'MAGY', 'MAGZ']
            dev: ['AF3', 'T7', 'Pz', 'T8', 'AF4', 'OVERALL']
            met: ['eng.isActive', 'eng', 'exc.isActive', 'exc', 'lex', 'str.isActive', 'str', 'rel.isActive', 'rel',
                  'int.isActive', 'int', 'foc.isActive', 'foc']
            pow: ['AF3/theta', 'AF3/alpha', 'AF3/betaL', 'AF3/betaH', 'AF3/gamma', 'T7/theta',
                  'T7/alpha', 'T7/betaL', 'T7/betaH', 'T7/gamma', 'Pz/theta', 'Pz/alpha', 'Pz/betaL', 'Pz/betaH',
                  'Pz/gamma', 'T8/theta', 'T8/alpha', 'T8/betaL', 'T8/betaH', 'T8/gamma', 'AF4/theta', 'AF4/alpha',
                  'AF4/betaL', 'AF4/betaH', 'AF4/gamma']
        ```

        Args:
            *args (Any): Variable length argument list.
            **kwargs (Any): Arbitrary keyword arguments.

        """
        data = kwargs.get('data', {})
        name = data['streamName']
        labels = data['labels']
        logger.debug(f'New data labels for {name}: {labels}')

    def on_new_eeg_data(self, *args: Any, **kwargs: Any) -> None:
        """Handle the new EEG data.

        Example:
            ```
            {'eeg': [99, 0, 4291.76, 4371.795, 4078.461, 4036.41, 4231.794, 0.0, 0], 'time': 1621410000.5166}
            ```

        Args:
            *args (Any): Variable length argument list.
            **kwargs (Any): Arbitrary keyword arguments.

        """
        data = kwargs.get('data', {})
        eeg = data['eeg']
        logger.debug(f'New EEG data: {eeg}')

    def on_new_mot_data(self, *args: Any, **kwargs: Any) -> None:
        """Handle the new motion data.

        Example:
            ```
            {'motion': [33, 0, 0.493859, 0.40625, 0.46875, -0.609375, 0.968765, 0.187503, -0.250004, -76.563667,
                        -19.584995, 38.281834], 'time': 1621410000.5166}
            ```
        Args:
            *args (Any): Variable length argument list.
            **kwargs (Any): Arbitrary keyword arguments.

        """
        data = kwargs.get('data', {})
        logger.debug(f'New motion data: {data}')

    def on_new_met_data(self, *args: Any, **kwargs: Any) -> None:
        """Handle the new performance metrics data.

        Example:
            ```
            {'met': [True, 0.5, True, 0.5, 0.0, True, 0.5, True, 0.5, True, 0.5, True, 0.5], 'time': 1627459390.4229}
            ```
        Args:
            *args (Any): Variable length argument list.
            **kwargs (Any): Arbitrary keyword arguments.

        """
        data = kwargs.get('data', {})
        logger.debug(f'New performance metrics data: {data}')

    def on_new_pow_data(self, *args: Any, **kwargs: Any) -> None:
        """Handle the new band power data.

        Example:
            ```
            {'pow': [5.251, 4.691, 3.195, 1.193, 0.282, 0.636, 0.929, 0.833, 0.347, 0.337, 7.863, 3.122, 2.243,
                     0.787, 0.496, 5.723, 2.87, 3.099, 0.91, 0.516, 5.783, 4.818, 2.393, 1.278, 0.213],
             'time': 1627459390.1729}
            ```

        Args:
            *args (Any): Variable length argument list.
            **kwargs (Any): Arbitrary keyword arguments.

        """
        data = kwargs.get('data', {})
        logger.debug(f'New band power data: {data}')

    def on_create_session_done(self, *args: Any, **kwargs: Any) -> None:
        """Handle the creation of a session."""
        # Subscribe to the data streams.
        self.subscribe(self.streams)

    def on_inform_error(self, *args: Any, **kwargs: Any) -> None:
        """Handle the error information."""
        error_data = kwargs.get('error_data')
        logger.error(error_data)

    @property
    def headset(self) -> Headset:
        """The headset object to connect to the BCI API."""
        return self._headset


def main() -> None:
    """Start subscribing to the data streams."""
    client_id = 'your-client-id'
    client_secret = 'your-client-secret'

    subscribe = Subscribe(client_id, client_secret)

    # Start subscribing to the data streams.
    streams = ['eeg', 'motion', 'met', 'pow']
    subscribe.start(streams)


if __name__ == '__main__':
    main()
