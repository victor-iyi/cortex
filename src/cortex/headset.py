import json
from pathlib import Path
from typing import Any, Literal

from cortex.api.headset import make_connection, query_headset, subscription
from cortex.api.markers import inject_marker, update_marker
from cortex.api.mental_command import (
    action_sensitivity,
    active_action,
    brain_map,
    training_threshold,
)
from cortex.api.record import (
    create_record,
    stop_record,
    update_record,
    delete_record,
    export_record,
    query_records,
    record_infos,
    config_opt_out,
    download_record_data,
)
from cortex.api.profile import current_profile, query_profile, setup_profile
from cortex.api.train import training, training_time, trained_signature_actions
from cortex.api.types import RecordQuery
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

        self.ws.send(json.dumps(connection, indent=4))

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

        self.ws.send(json.dumps(connection, indent=4))

    def query_headset(self) -> None:
        """Query the headset."""
        logger.info('--- Querying the headset ---')

        _query_headset = query_headset(headset_id=self.headset_id)

        # If debug mode is enabled, print the query.
        logger.debug('Querying the headset.')
        logger.debug(query_headset)

        self.ws.send(json.dumps(_query_headset, indent=4))

    def subscribe(self, streams: list[str]) -> None:
        """Subscribe to one or more data stream.

        Args:
            streams (list[str]): The data streams to subscribe to.

        Read More:
            [subscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/subscribe)

        """
        logger.info('--- Subscribing to the headset ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _request = subscription(
            auth=self.auth,
            session_id=self.session_id,
            streams=streams,
            method='subscribe',
        )

        # If debug mode is enabled, print the subscription request.
        logger.debug('Subscribe request:')
        logger.debug(_request)

        self.ws.send(json.dumps(_request, indent=4))

    def unsubscribe(self, streams: list[str]) -> None:
        """Unsubscribe from one or more data stream.

        Args:
            streams (list[str]): The data streams to unsubscribe from.

        Read More:
            [unsubscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/unsubscribe)

        """
        logger.info('--- Unsubscribing from the headset ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _request = subscription(
            auth=self.auth,
            session_id=self.session_id,
            streams=streams,
            method='unsubscribe',
        )

        # If debug mode is enabled, print the subscription request.
        logger.debug('Unsubscribe request:')
        logger.debug(_request)

        self.ws.send(json.dumps(_request, indent=4))

    def query_profile(self) -> None:
        """Query the profile."""
        logger.info('--- Querying the profile ---')

        query = query_profile(auth=self._auth)

        # If debug mode is enabled, print the query.
        logger.debug('Querying the profile.')
        logger.debug(query)

        self.ws.send(json.dumps(query, indent=4))

    def get_current_profile(self) -> None:
        """Get the current profile."""
        logger.info('--- Getting the current profile ---')

        if not self.headset_id:
            raise ValueError('No headset ID. Please connect to the headset first.')

        current = current_profile(auth=self.auth, headset_id=self.headset_id)

        # If debug mode is enabled, print the current profile.
        logger.debug('Getting the current profile.')
        logger.debug(current)

        self.ws.send(json.dumps(current, indent=4))

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
        logger.info(f'--- {status.title()} the profile: {profile_name} ---')

        # Update self.profile_name if the status is 'create' or 'rename'.
        if status == 'create':
            self.profile_name = profile_name
        elif status == 'rename' and new_profile_name is not None:
            self.profile_name = new_profile_name

        setup = setup_profile(
            auth=self.auth,
            status=status,
            profile_name=profile_name,
            headset_id=self.headset_id,
            new_profile_name=new_profile_name,
        )

        # If debug mode is enabled, print the setup.
        logger.debug('Setting up the profile.')
        logger.debug(setup)

        self.ws.send(json.dumps(setup, indent=4))

    def create_record(self, title: str, **kwargs: str | list[str] | int) -> None:
        """Create a record.

        Args:
            title (str): The title of the record.

        Keyword Args:
            description (str): The description of the record.
            subject_name (str): The name of the subject.
            tags (list[str]): The tags of the record.
            experiment_id (int): The experiment ID.

        """
        if len(title) == 0:
            logger.warning('Empty record title. Please fill the record title.')
            # close socket.
            self.close()
            return

        logger.info(f'--- Creating a record: {title} ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        record = create_record(
            auth=self.auth,
            session_id=self.session_id,
            title=title,
            **kwargs,
        )

        # If debug mode is enabled, print the record.
        logger.debug('Creating a record.')
        logger.debug(record)

        self.ws.send(json.dumps(record, indent=4))

    def stop_record(self) -> None:
        """Stop the record."""
        logger.info('--- Stopping the record ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        record = stop_record(auth=self.auth, session_id=self.session_id)

        # If debug mode is enabled, print the record.
        logger.debug('Stopping the record.')
        logger.debug(record)

        self.ws.send(json.dumps(record, indent=4))

    def update_record(self, record_id: str, **kwargs: str | list[str]) -> None:
        """Update a record.

        Args:
            record_id (str): The record ID.

        Keyword Args:
            title (str): The title of the record.
            description (str): The description of the record.
            tags (list[str]): The tags of the record.

        """
        logger.info(f'--- Updating a record {record_id} ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        record = update_record(
            auth=self.auth,
            record_id=record_id,
            **kwargs,
        )

        # If debug mode is enabled, print the record.
        logger.debug('Updating a record.')
        logger.debug(record)

        self.ws.send(json.dumps(record, indent=4))

    def delete_record(self, records: list[str]) -> None:
        """Delete one or more records.

        Args:
            records (list[str]): The record IDs.

        """
        logger.info('--- Deleting records ---')

        record = delete_record(auth=self.auth, records=records)

        # If debug mode is enabled, print the record.
        logger.debug(f'Deleting records {records}.')
        logger.debug(record)

        self.ws.send(json.dumps(record, indent=4))

    def export_record(
        self,
        record_ids: list[str],
        folder: str | Path,
        stream_types: list[str],
        # pylint: disable-next=redefined-builtin,implicit-str-concat
        format: Literal['EDF' 'EDFPLUS', 'BDFPLUS', 'CSV'],
        **kwargs: str | list[str] | bool,
    ) -> None:
        """Export one or more records.

        Args:
            record_ids (list[str]): The record IDs.
            folder (str | Path): The folder to save the records.
            stream_types (list[str]): The stream types.
            format (Literal['EDF' 'EDFPLUS', 'BDFPLUS', 'CSV']): The format.

        Keyword Args:
            version (Literal['V1', 'V2']): The version of the CSV format.
                 If the format is "EDF", then you must omit this parameter.
                 If the format is "CSV", then this parameter must be "V1" or "V2".
            license_ids (list[str], optional): The default value is an empty list,
                 which means that you can only export the records created by your app.
            include_demographics (bool, optional): If `true` the the exported JSON
                 file will include the demographic data of the user.
            include_survey (bool, optional): If `true` the the exported JSON file
                 will include the survey data of the record.
            include_marker_extra_infos (bool, optional): If `true` the the markers of
                 the records will be exported to a CSV file.
            include_deprecated_pm (bool, optional): If `true` then deprecated performance
                 metrics (i.e. Focus) will be exported.

        """
        if len(str(folder)) == 0:
            logger.warning('Invalid folder path. Please set a writeable destination folder for exporting data.')
            # close socket.
            self.close()
            return

        logger.info('--- Exporting records ---')

        export = export_record(
            auth=self.auth,
            record_ids=record_ids,
            folder=str(folder),
            stream_types=stream_types,
            format=format,
            **kwargs,
        )

        # If debug mode is enabled, print the export.
        logger.debug(f'Exporting records to {folder}.')
        logger.debug(export)

        self.ws.send(json.dumps(export, indent=4))

    def query_records(
        self,
        query: RecordQuery,
        order_by: list[dict[str, Literal['ASC', 'DESC']]],
        **kwargs: int | bool,
    ) -> None:
        """Query records.

        Args:
            query (RecordQuery): The query parameters.
            order_by (list[dict[str, Literal['ASC', 'DESC']]]): The order by parameters.

        Keyword Args:
            limit (int): The maximum number of records to return.
            offset (int): The number of records to skip.
            include_markers (bool): If `true` the the markers of the records will be included.
            include_sync_status_info (bool): If `true` the the sync status of the records will be included.

        """
        logger.info('--- Querying records ---')

        _query = query_records(
            auth=self.auth,
            query=query,
            order_by=order_by,
            **kwargs,
        )

        # If debug mode is enabled, print the query.
        logger.debug('Querying records.')
        logger.debug(_query)

        self.ws.send(json.dumps(_query, indent=4))

    def get_record_info(self, record_ids: list[str]) -> None:
        """Get the record information.

        Args:
            record_ids (list[str]): The record IDs.

        """
        logger.info('--- Getting record information ---')

        record = record_infos(auth=self.auth, record_ids=record_ids)

        # If debug mode is enabled, print the record.
        logger.debug('Getting record information.')
        logger.debug(record)

        self.ws.send(json.dumps(record, indent=4))

    def set_config_opt_out(self, opt_out: bool) -> None:
        """Set the config opt out.

        Args:
            opt_out (bool): The opt out status.

        """
        logger.info('--- Setting the config opt out ---')

        _config = config_opt_out(
            auth=self.auth,
            status='set',
            new_opt_out=opt_out,
        )

        # If debug mode is enabled, print the config.
        logger.debug('Setting the config opt out.')
        logger.debug(_config)

        self.ws.send(json.dumps(_config, indent=4))

    def get_config_opt_out(self) -> None:
        """Get the config opt out."""
        logger.info('--- Getting the config opt out ---')

        _config = config_opt_out(auth=self.auth, status='get')

        # If debug mode is enabled, print the config.
        logger.debug('Getting the config opt out.')
        logger.debug(_config)

        self.ws.send(json.dumps(_config, indent=4))

    def download_record_data(self, record_ids: list[str]) -> None:
        """Download the record data.

        Args:
            record_ids (list[str]): The record IDs.

        """
        logger.info('--- Downloading record data ---')

        _download = download_record_data(auth=self.auth, record_ids=record_ids)

        # If debug mode is enabled, print the download.
        logger.debug('Downloading record data.')
        logger.debug(_download)

        self.ws.send(json.dumps(_download, indent=4))

    def inject_marker(self, time: int, value: str | int, label: str, **kwargs: str | Any) -> None:
        """Inject a marker.

        Args:
            time (int): The time in milliseconds.
            value (str | int): The marker value.
            label (str): The marker label.

        Keyword Args:
            port (str): The marker port.
            extras (Mapping[str, Any]): Additional parameters.

        """
        logger.info('--- Injecting a marker ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _marker = inject_marker(
            auth=self.auth,
            session_id=self.session_id,
            time=time,
            value=value,
            label=label,
            **kwargs,
        )

        # If debug mode is enabled, print the marker.
        logger.debug('Injecting a marker.')
        logger.debug(_marker)

        self.ws.send(json.dumps(_marker, indent=4))

    def update_marker(self, marker_id: str, time: int, **kwargs: str | Any) -> None:
        """Update a marker.

        Args:
            marker_id (str): The marker ID.
            time (int): The time in milliseconds.

        Keyword Args:
            value (str | int): The marker value.
            label (str): The marker label.
            port (str): The marker port.
            extras (Mapping[str, Any]): Additional parameters.

        """
        logger.info('--- Updating a marker ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _marker = update_marker(
            auth=self.auth,
            session_id=self.session_id,
            marker_id=marker_id,
            time=time,
            **kwargs,
        )

        # If debug mode is enabled, print the marker.
        logger.debug('Updating a marker.')
        logger.debug(_marker)

        self.ws.send(json.dumps(_marker, indent=4))

    def train_request(
        self,
        detection: Literal['mentalCommand', 'facialExpression'],
        status: Literal['start', 'accept', 'reject', 'reset', 'erase'],
        action: str,
    ) -> None:
        """Send a training request.

        Args:
            detection (Literal['mentalCommand', 'facialExpression']): The detection type.
            status (Literal['start', 'accept', 'reject', 'reset', 'erase']): The status.
            action (str): The action to train.

        """
        logger.info('--- Sending a training request ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _training = training(
            auth=self.auth,
            session_id=self.session_id,
            detection=detection,
            status=status,
            action=action,
        )

        # If debug mode is enabled, print the training.
        logger.debug('Sending a training request.')
        logger.debug(_training)

        self.ws.send(json.dumps(_training, indent=4))

    def training_signature_action(
        self,
        detection: Literal['mentalCommand', 'facialExpression'],
        **kwargs: str,
    ) -> None:
        """Get the list of trained actions of a profile.

        Args:
            detection (Literal['mentalCommand', 'facialExpression']): The detection type.

        Keyword Args:
            profile_name (str): The profile name.
            session_id (str): The session ID.

        """
        logger.info('--- Getting the list of trained actions ---')

        _training = trained_signature_actions(
            auth=self.auth,
            detection=detection,
            **kwargs,
        )

        # If debug mode is enabled, print the training.
        logger.debug('Getting the list of trained actions.')
        logger.debug(_training)

        self.ws.send(json.dumps(_training, indent=4))

    def training_time(self, detection: Literal['mentalCommand', 'facialExpression']) -> None:
        """Get the training time.

        Args:
            detection (Literal['mentalCommand', 'facialExpression']): The detection type.

        """
        logger.info('--- Getting the training time ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _training = training_time(
            auth=self.auth,
            session_id=self.session_id,
            detection=detection,
        )

        # If debug mode is enabled, print the training.
        logger.debug('Getting the training time.')
        logger.debug(_training)

        self.ws.send(json.dumps(_training, indent=4))

    def get_mental_command_action_sensitive(self, profile_name: str) -> None:
        """Get the mental command action sensitivity."""
        logger.info('--- Getting mental command action sensitivity ---')

        sensitivity = action_sensitivity(
            auth=self.auth,
            profile_name=profile_name,
            status='get',
        )

        # If debug mode is enabled, print the sensitivity.
        logger.debug('Getting mental command action sensitivity.')
        logger.debug(sensitivity)

        self.ws.send(json.dumps(sensitivity, indent=4))

    def set_mental_command_action_sensitive(
        self,
        profile_name: str,
        values: list[int],
    ) -> None:
        """Set the mental command action sensitivity."""
        logger.info('--- Setting mental command action sensitivity ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        sensitivity = action_sensitivity(
            auth=self.auth,
            profile_name=profile_name,
            session_id=self.session_id,
            values=values,
            status='set',
        )

        # If debug mode is enabled, print the sensitivity.
        logger.debug('Setting mental command action sensitivity.')
        logger.debug(sensitivity)

        self.ws.send(json.dumps(sensitivity, indent=4))

    def get_mental_command_active_action(self, profile_name: str) -> None:
        """Get the active mental command action."""
        logger.info('--- Getting mental command active action ---')

        active = active_action(
            auth=self.auth,
            status='get',
            profile_name=profile_name,
        )

        # If debug mode is enabled, print the active action.
        logger.debug('Getting mental command active action.')
        logger.debug(active)

        self.ws.send(json.dumps(active, indent=4))

    def set_mental_command_active_action(self, actions: list[str]) -> None:
        """Set the active mental command action."""
        logger.info('--- Setting mental command active action ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        active = active_action(
            auth=self.auth,
            status='set',
            session_id=self.session_id,
            actions=actions,
        )

        # If debug mode is enabled, print the active action.
        logger.debug('Setting mental command active action.')
        logger.debug(active)

        self.ws.send(json.dumps(active, indent=4))

    def get_mental_command_brain_map(self, profile_name: str) -> None:
        """Get the mental command brain map."""
        logger.info('--- Getting mental command brain map ---')

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

        self.ws.send(json.dumps(brain, indent=4))

    def get_mental_command_training_threshold(self, profile_name: str) -> None:
        """Get the mental command training threshold."""
        logger.info('--- Getting mental command training threshold ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        threshold = training_threshold(
            auth=self.auth,
            profile_name=profile_name,
            session_id=self.session_id,
        )

        # If debug mode is enabled, print the training threshold.
        logger.debug('Getting mental command training threshold.')
        logger.debug(threshold)

        self.ws.send(json.dumps(threshold, indent=4))
