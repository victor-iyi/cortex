"""Create record and export data to CSV or EDF file.

Getting Started:
    - Please reference https://emotiv.gitbook.io/cortex-api/ for more information.
    - Connect your headset with dongle or bluetooth. You can see the headset via Emotiv Launcher.
    - Please make sure the client_id and client_secret are set and correct before starting.
    - In case you borrow license from others, you need to add `license = 'xxx-yyy-zzz' as init parameter.
    - Check the `on_create_session_done` to see how to create a record.
    - Check the `on_warn_cortex_stop_all_sub` to see how to export record.

Result:
    - Record data.
    - Export recording data. The result should be CSV or EDF file.
    - The file will have data specified, like: eeg, motion, performance metric and band power.

"""
# pylint: disable=unused-argument

import time
from typing import Any

from cortex import Headset, logger


class Record:
    """Create record and export data to CSV or EDF file.

    Attributes:
        headset (Headset): The headset object to connect to the BCI API.
        record_duration (int): The duration of the recording in seconds.
        record_id (str): The id of the record.
        record_title (str): The title of the record.
        record_description (str): The description of the record.
        export_folder (str): The folder to save the exported data.
        export_format (str): The format of the exported data.
        export_version (str): The version of the exported data.
        export_stream_types (list[str]): The types of data streams to export.

    Methods:
        start(record_duration: int = 20, headset_id: str = '') -> None:
            Start recording data.
        create_record(record_title: str, **kwargs: Any) -> None:
            Create a record with the given title.
        stop_record() -> None:
            Stop recording data.
        export_record(
            folder: str, stream_types: list[str], format: str, record_ids: list[str], version: str, **kwargs: Any
        ) -> None:
            Export the recording data.
        wait(record_duration: int) -> None:
            Wait for the specified duration.

    Callback Methods:
        on_create_session_done(*args: Any, **kwargs: Any) -> None:
            Handle the creation of a session.
        on_create_record_done(*args: Any, **kwargs: Any) -> None:
            Handle the creation of a record.
        on_stop_record_done(*args: Any, **kwargs: Any) -> None:
            Handle the stop of a record.
        on_warn_cortex_stop_all_sub(*args: Any, **kwargs: Any) -> None:
            Handle the warning to stop all subscriptions.
        on_export_record_done(*args: Any, **kwargs: Any) -> None:
            Handle the export of a record.
        on_inform_error(*args: Any, **kwargs: Any) -> None:
            Handle the error information.

    """

    def __init__(self, client_id: str, client_secret: str, **kwargs: Any) -> None:
        """Initialize the Record class."""
        self._headset = Headset(client_id, client_secret, **kwargs)

        self._headset.bind(create_session_done=self.on_create_session_done)
        self._headset.bind(create_record_done=self.on_create_record_done)
        self._headset.bind(stop_record_done=self.on_stop_record_done)
        self._headset.bind(warn_cortex_stop_all_sub=self.on_warn_cortex_stop_all_sub)
        self._headset.bind(export_record_done=self.on_export_record_done)
        self._headset.bind(inform_error=self.on_inform_error)

        self.record_duration: int = 0
        self.record_ids: list[str] = []
        self.record_title: str = ''
        self.record_description: str = ''
        self.export_folder: str = '.'
        self.export_format: str = 'CSV'
        self.export_version: str = 'V2'
        self.export_stream_types: list[str] = []

    def start(self, record_duration: int = 20, headset_id: str = '') -> None:
        """Start recording data.

        To start data recording and exporting, follow these workflow steps:
            1. Check access right -> authorize -> connect headset -> create session.
            2. Start record -> stop record > disconnect headset -> export record.

        Args:
            record_duration (int): The duration of the recording in seconds.
            headset_id (str): The id of the headset to record data from.

        """
        self.record_duration = record_duration

        if headset_id != '':
            self._headset.set_headset(headset_id)

        self._headset.open()

    @staticmethod
    def custom_hook(args: Any) -> None:
        """Custom hook to handle the data received from the headset."""
        logger.info(f'Thread failed: {args.exc_value}')

    def create_record(self, record_title: str, **kwargs: Any) -> None:
        """Create a record with the given title.

        Args:
            record_title (str): The title of the record.
            **kwargs (Any): Additional arguments to pass to the create_record method.

        """
        self._headset.create_record(title=record_title, **kwargs)

    def stop_record(self) -> None:
        """Stop recording data."""
        self._headset.stop_record()

    def export_record(
        self, folder: str, stream_types: list[str], format: str, record_ids: list[str], version: str, **kwargs: Any
    ) -> None:
        """Export the recording data.

        Args:
            folder (str): The folder to save the exported data.
            stream_types (list[str]): The types of data streams to export.
            format (str): The format of the exported data.
            record_ids (str): The ids of the records to export.
            version (str): The version of the data to export.
            **kwargs (Any): Additional arguments to pass to the export_record method.

        """
        self._headset.export_record(record_ids, folder, stream_types, format, version=version, **kwargs)

    def wait(self, record_duration: int) -> None:
        """Wait for the specified duration.

        Args:
            record_duration (int): The duration to wait in seconds.

        """
        logger.debug('------------- start recording -------------')

        length = 0
        while length < record_duration:
            logger.debug(f'Recording data for {length}sec.')
            time.sleep(1)
            length += 1
        logger.debug('------------- stop recording -------------')

    # +-----------------------------------------------------------------------+
    # |                           Callback Methods                            |
    # +-----------------------------------------------------------------------+
    def on_create_session_done(self, *args: Any, **kwargs: Any) -> None:
        """Handle the creation of a session."""
        logger.debug('------------- create session done -------------')

        # Create a record.
        self._headset.create_record(title=self.record_title, descritption=self.record_description)

    def on_create_record_done(self, *args: Any, **kwargs: Any) -> None:
        """Handle the creation of a record."""
        logger.debug('------------- create record done -------------')

        data = kwargs.get('data')
        self.record_ids = data['uuid']  # type: ignore[index]
        start_time = data['startDatetime']  # type: ignore[index]
        title = data['title']  # type: ignore[index]

        logger.debug(f'Record created: {title} ({self.record_ids}) at {start_time}')

        self.wait(self.record_duration)

        # Start recording data.
        self.stop_record()

    def on_stop_record_done(self, *args: Any, **kwargs: Any) -> None:
        """Handle the stop of a record."""
        logger.debug('------------- stop record done -------------')

        data = kwargs.get('data')
        record_id = data['uuid']  # type: ignore[index]
        start_time = data['startDatetime']  # type: ignore[index]
        end_time = data['endDatetime']  # type: ignore[index]
        title = data['title']  # type: ignore[index]

        # Disconnect headset to export record.
        logger.debug(f'Record stopped: {title} ({record_id}) at {end_time} (started at {start_time})')
        self._headset.disconnect()

    def on_warn_cortex_stop_all_sub(self, *args: Any, **kwargs: Any) -> None:
        """Handle the warning to stop all subscriptions."""
        logger.debug('------------- stop all subscriptions -------------')

        # Export record.
        self.export_record(
            folder=self.export_folder,
            stream_types=self.export_stream_types,
            format=self.export_format,
            record_ids=self.record_ids,
            version=self.export_version,
        )

    def on_export_record_done(self, *args: Any, **kwargs: Any) -> None:
        """Handle the export of a record."""
        logger.debug('------------- export record done -------------')

        data = kwargs.get('data')
        logger.debug(data)

        self._headset.close()

    def on_inform_error(self, *args: Any, **kwargs: Any) -> None:
        """Handle the error information."""
        error_data = kwargs.get('data')
        logger.error(error_data)

    @property
    def headset(self) -> Headset:
        """The headset object to connect to the BCI API."""
        return self._headset


def main() -> None:
    """Main function to start the record."""
    import os

    # TODO: Please fill your application client ID and client secret.
    client_id = os.getenv('EMOTIV_CLIENT_ID') or '<your-client-id>'
    client_secret = os.getenv('EMOTIV_CLIENT_SECRET') or '<your-client-secret>'

    record = Record(client_id=client_id, client_secret=client_secret)

    # Input params for `create_record`. Please see `on_warn_cortex_stop_all_sub`.
    record.record_title = ''  # required param and cannot be empty.
    record.record_description = ''  # optional param.

    # Input params for `export_record`. Please see `on_warn_cortex_stop_all_sub`.
    record.export_folder = '.'  # your place to export (must have write permission).
    record.export_format = 'CSV'  # 'csv' or 'edf'.
    record.export_version = 'V2'  # version of the data.
    record.export_stream_types = ['EEG', 'MOTION', 'PM', 'BP']  # data types to export.

    record_duration = 10  # duration of the recording in seconds.
    record.start(record_duration)


if __name__ == '__main__':
    main()
