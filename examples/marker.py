"""Inject marker during a recording.

Getting Started:
    - Please reference https://emotiv.gitbook.io/cortex-api/ for more information.
    - Connect your headset with dongle or bluetooth. You can see the headset via Emotiv Launcher.
    - Please make sure the client_id and client_secret are set and correct before starting.
    - In case you borrow license from others, you need to add `license = 'xxx-yyy-zzz' as init parameter.
    - Check the `on_create_session_done` to see how to create a record.

Result:
    - Record data then inject marker each 3 seconds.
    - Export data file should contain the added markers.

"""
# pylint: disable=unused-argument

import threading
import time

from typing import Any

from cortex import Headset, logger


class Marker:
    """Inject marker during a recording.

    Attributes:
        headset (Headset): The headset object to connect to the BCI API.
        record_title (str): The title of the record.
        record_description (str): The description of the record.
        marker_idx (int): The index of the marker.
        marker_value (str): The value of the marker.
        marker_label (str): The label of the marker.
        number_markers (int): The number of markers to inject.
        record_export_folder (str): The folder to save the exported data.
        record_export_data_types (list[str]): The types of data streams to export.
        record_export_format (str): The format of the exported data.
        record_export_version (str): The version of the data to export.

    Methods:
        start(number_markers: int = 10, headset_id: str = '') -> None:
            Start injecting markers during a recording.
        create_record(record_title: str, **kwargs: Any) -> None:
            Create a record.
        stop_record() -> None:
            Stop the record.
        export_record(
            folder: str, stream_types: list[str], format: str, record_ids: list[str], version: str, **kwargs: Any
        ) -> None:
            Export the recording data.
        add_markers() -> None:
            Add a marker to the record.
        inject_marker(time: int, value: str, label: str, **kwargs: Any) -> None:
            Inject a marker to the record.
        update_marker(marker_id: str, time: int, **kwargs: Any) -> None:
            Update a marker.

    Callback Methods:
        on_create_session_done(*args: Any, **kwargs: Any) -> None:
            Handle the creation of a session.
        on_create_record_done(*args: Any, **kwargs: Any) -> None:
            Handle the creation of a record.
        on_stop_record_done(*args: Any, **kwargs: Any) -> None:
            Handle the stop of a record.
        on_inject_marker(*args: Any, **kwargs: Any) -> None:
            Handle the injection of a marker.
        on_warn_cortex_stop_all_sub(*args: Any, **kwargs: Any) -> None:
            Handle the warning to stop all subscriptions.
        on_export_record_done(*args: Any, **kwargs: Any) -> None:
            Handle the export of a record.
        on_inform_error(*args: Any, **kwargs: Any) -> None:
            Handle the error information.

    """

    def __init__(self, client_id: str, client_secret: str, **kwargs: Any) -> None:
        """Initialize the Marker class."""
        self._headset = Headset(client_id, client_secret, **kwargs)

        self._headset.bind(create_session_done=self.on_create_session_done)
        self._headset.bind(create_record_done=self.on_create_record_done)
        self._headset.bind(stop_record_done=self.on_stop_record_done)
        self._headset.bind(warn_cortex_stop_all_sub=self.on_warn_cortex_stop_all_sub)
        self._headset.bind(inject_marker_done=self.on_inject_marker_done)
        self._headset.bind(export_record_done=self.on_export_record_done)
        self._headset.bind(inform_error=self.on_inform_error)

        self.record_title: str = ''
        self.record_description: str = ''
        self.marker_idx = 0
        self.marker_value: str = ''
        self.marker_label: str = ''
        self.number_markers: int = 10
        self.export_folder: str = ''
        self.export_stream_types: list[str] = []
        self.export_record_ids: list[str] = []
        self.export_format: str = 'CSV'
        self.export_version: str = 'V2'

    def start(self, number_markers: int = 10, headset_id: str = '') -> None:
        """Start injecting markers during a recording.

        To start data recording and injecting marker, follow these workflow steps:
            1. Check access right -> authorize -> connect headset -> create session.
            2. Start record -> stop record > disconnect headset -> export record.

        Args:
            number_markers (int): The number of markers to inject.
            headset_id (str): The headset id to connect to.

        """
        self.number_markers = number_markers
        self.marker_idx = 0

        if headset_id != '':
            self._headset.set_headset(headset_id)

        self._headset.open()

    def create_record(self, record_title: str, **kwargs: Any) -> None:
        """Create a record.

        Args:
            record_title (str): The title of the record.
            **kwargs (Any): Additional arguments.

        """
        self.record_title = record_title

        self._headset.create_record(title=record_title, **kwargs)

    def stop_record(self) -> None:
        """Stop the record."""
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

        Read More:
            More detail at https://emotiv.gitbook.io/cortex-api/records/exportrecord

        """
        self._headset.export_record(record_ids, folder, stream_types, format, version=version, **kwargs)

    def add_markers(self) -> None:
        """Add a marker to the record."""
        logger.debug(f'Add marker: {self.number_markers} will be injected each second automatically.')

        for m in range(self.number_markers):
            marker_time = int(time.time() * 1000)
            logger.debug(f'Inject marker: {m + 1} at {marker_time}')

            marker_label = f'{self.marker_label}_{m + 1}'
            self.inject_marker(marker_time, self.marker_value, marker_label, port='python_app')

            # Add marker each 3 seconds.
            time.sleep(3)

    def inject_marker(self, time: int, value: str, label: str, **kwargs: Any) -> None:
        """Inject a marker to the record.

        Args:
            time (int): The time to inject the marker.
            value (str): The value of the marker.
            label (str): The label of the marker.
            **kwargs (Any): Additional arguments.

        Read More:
            More detail at https://emotiv.gitbook.io/cortex-api/markers/injectmarker

        """
        self._headset.inject_marker(time, value, label, **kwargs)

    def update_marker(self, marker_id: str, time: int, **kwargs: Any) -> None:
        """Update a marker.

        Args:
            marker_id (str): The id of the marker to update.
            time (int): The time to update the marker.
            **kwargs (Any): Additional arguments.

        Read More:
            More detail at https://emotiv.gitbook.io/cortex-api/markers/updatemarker

        """
        self._headset.update_marker(marker_id, time, **kwargs)

    # +-----------------------------------------------------------------------+
    # |                           Callback Methods                            |
    # +-----------------------------------------------------------------------+
    def on_create_session_done(self, *args: Any, **kwargs: Any) -> None:
        """Handle the creation of a session."""
        logger.debug('------------- create session done -------------')

        # Create a record.
        self._headset.create_record(title=self.record_title, descritption=self.record_description, **kwargs)

    def on_create_record_done(self, *args: Any, **kwargs: Any) -> None:
        """Handle the creation of a record."""
        logger.debug('------------- create record done -------------')

        data = kwargs.get('data')
        self.record_id = data['uuid']  # type: ignore[index]
        start_time = data['startTime']  # type: ignore[index]
        title = data['title']  # type: ignore[index]

        logger.debug(f'Start record ({self.record_id}): {title} at {start_time}')

        # Inject markers.
        th = threading.Thread(target=self.add_markers)
        th.start()

    def on_stop_record_done(self, *args: Any, **kwargs: Any) -> None:
        """Handle the stop of a record."""
        logger.debug('------------- stop record done -------------')

        data = kwargs.get('data')
        marker_id = data['uuid']  # type: ignore[index]
        start_time = data['startTime']  # type: ignore[index]
        marker_type = data['type']  # type: ignore[index]

        logger.debug(f'Stop record ({marker_id}): {marker_type} at {start_time}')
        self._headset.disconnect()

    def on_inject_marker_done(self, *args: Any, **kwargs: Any) -> None:
        """Handle the injection of a marker."""
        logger.debug('------------- inject marker -------------')

        data = kwargs.get('data')
        marker_id = data['uuid']  # type: ignore[index]
        start_time = data['startDatetime']  # type: ignore[index]
        marker_type = data['type']  # type: ignore[index]
        logger.debug(f'Inject marker ({marker_id}): {marker_type} at {start_time}')

        self.marker_idx += 1
        if self.marker_idx == self.number_markers:
            # Stop record.
            self.stop_record()

    def on_warn_cortex_stop_all_sub(self, *args: Any, **kwargs: Any) -> None:
        """Handle the warning to stop all subscriptions."""
        logger.debug('------------- stop all subscriptions -------------')
        time.sleep(3)

        # Export record.
        self.export_record(
            folder=self.export_folder,
            stream_types=self.export_stream_types,
            format=self.export_format,
            record_ids=self.export_record_ids,
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
    """Inject marker during a recording."""
    import os

    # TODO: Please fill your application client ID and client secret.
    client_id = os.getenv('EMOTIV_CLIENT_ID') or '<your-client-id>'
    client_secret = os.getenv('EMOTIV_CLIENT_SECRET') or '<your-client-secret>'

    marker = Marker(client_id=client_id, client_secret=client_secret, debug_mode=True)

    # Input params for `create_record`. Please see `on_create_session_done` for more detail.
    marker.record_title = ''  # required param and cannot be empty.
    marker.record_description = ''  # optional param.

    # Marker input for inject marker.
    marker.marker_value = 'test value'  # required param and cannot be empty.
    marker.marker_label = 'test label'  # required param and cannot be empty.

    # Input params for `export_record`. Please see `on_warn_cortex_stop_all_sub` for more detail.
    marker.export_folder = '.'  # required param and cannot be empty.
    marker.export_stream_types = ['EEG', 'MOTION', 'PM', 'BP']
    marker.export_format = 'CSV'
    marker.export_version = 'V2'

    marker_numbers = 10
    marker.start(marker_numbers)


if __name__ == '__main__':
    main()
