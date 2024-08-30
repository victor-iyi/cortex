"""Headset API.

This module contains the Headset class, which is used to interact with the Emotiv headset.

"""

import json
from pathlib import Path
from typing import Any, Literal

from cortex.api.markers import inject_marker, update_marker
from cortex.api.mental_command import action_sensitivity, active_action, brain_map, training_threshold
from cortex.api.profile import current_profile, query_profile, setup_profile
from cortex.api.record import (
    config_opt_out,
    create_record,
    delete_record,
    download_record_data,
    export_record,
    query_records,
    record_infos,
    stop_record,
    update_record,
)
from cortex.api.train import trained_signature_actions, training, training_time
from cortex.api.types import RecordQuery
from cortex.cortex import Cortex
from cortex.logging import logger


class Headset(Cortex):
    """The Headset class.

    This class is used to interact with the Emotiv headset.

    """

    def __init__(self, *args: str, **kwargs: bool | str | int) -> None:
        """Initialize the Headset class."""
        super().__init__(*args, **kwargs)

    def query_profile(self) -> None:
        """Query the profile."""
        logger.info('--- Querying the profile ---')

        _query = query_profile(auth=self.auth)

        logger.debug(_query)

        self.ws.send(json.dumps(_query, indent=4))

    def get_current_profile(self) -> None:
        """Get the current profile."""
        logger.info('--- Getting the current profile ---')

        if not self.headset_id:
            raise ValueError('No headset ID. Please connect to the headset first.')

        _profile = current_profile(auth=self.auth, headset_id=self.headset_id)

        logger.debug(_profile)

        self.ws.send(json.dumps(_profile, indent=4))

    def setup_profile(
        self,
        status: Literal['create', 'load', 'unload', 'save', 'rename', 'delete'],
        profile_name: str,
        *,
        new_profile_name: str | None = None,
    ) -> None:
        """Setup a profile.

        Args:
            status (Literal['create', 'load', 'unload', 'save', 'rename', 'delete']): The status of the profile.
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

        _profile = setup_profile(
            auth=self.auth,
            status=status,
            profile_name=profile_name,
            headset_id=self.headset_id,
            new_profile_name=new_profile_name,
        )

        logger.debug(_profile)

        self.ws.send(json.dumps(_profile, indent=4))

    def create_record(self, title: str, **kwargs: str | list[str] | int) -> None:  # noqa: D417
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

        _record = create_record(auth=self.auth, session_id=self.session_id, title=title, **kwargs)

        logger.debug(_record)

        self.ws.send(json.dumps(_record, indent=4))

    def stop_record(self) -> None:
        """Stop the record."""
        logger.info('--- Stopping the record ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _record = stop_record(auth=self.auth, session_id=self.session_id)

        logger.debug(_record)

        self.ws.send(json.dumps(_record, indent=4))

    def update_record(self, record_id: str, **kwargs: str | list[str]) -> None:  # noqa: D417
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

        _record = update_record(auth=self.auth, record_id=record_id, **kwargs)

        logger.debug(_record)

        self.ws.send(json.dumps(_record, indent=4))

    def delete_record(self, records: list[str]) -> None:
        """Delete one or more records.

        Args:
            records (list[str]): The record IDs.

        """
        logger.info('--- Deleting records ---')

        _record = delete_record(auth=self.auth, records=records)

        logger.debug(_record)

        self.ws.send(json.dumps(_record, indent=4))

    def export_record(  # noqa: D417
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

        _export = export_record(
            auth=self.auth,
            record_ids=record_ids,
            folder=str(folder),
            stream_types=stream_types,
            format=format,
            **kwargs,
        )

        logger.debug(_export)

        self.ws.send(json.dumps(_export, indent=4))

    def query_records(  # noqa: D417
        self, query: RecordQuery, order_by: list[dict[str, Literal['ASC', 'DESC']]], **kwargs: int | bool
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

        _query = query_records(auth=self.auth, query=query, order_by=order_by, **kwargs)

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

        _config = config_opt_out(auth=self.auth, status='set', new_opt_out=opt_out)

        logger.debug(_config)

        self.ws.send(json.dumps(_config, indent=4))

    def get_config_opt_out(self) -> None:
        """Get the config opt out."""
        logger.info('--- Getting the config opt out ---')

        _config = config_opt_out(auth=self.auth, status='get')

        logger.debug(_config)

        self.ws.send(json.dumps(_config, indent=4))

    def download_record_data(self, record_ids: list[str]) -> None:
        """Download the record data.

        Args:
            record_ids (list[str]): The record IDs.

        """
        logger.info('--- Downloading record data ---')

        _download = download_record_data(auth=self.auth, record_ids=record_ids)

        logger.debug(_download)

        self.ws.send(json.dumps(_download, indent=4))

    def inject_marker(self, time: int, value: str | int, label: str, **kwargs: str | Any) -> None:  # noqa: D417
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
            auth=self.auth, session_id=self.session_id, time=time, value=value, label=label, **kwargs
        )

        logger.debug(_marker)

        self.ws.send(json.dumps(_marker, indent=4))

    def update_marker(self, marker_id: str, time: int, **kwargs: str | Any) -> None:  # noqa: D417
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

        _marker = update_marker(auth=self.auth, session_id=self.session_id, marker_id=marker_id, time=time, **kwargs)

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
            auth=self.auth, session_id=self.session_id, detection=detection, status=status, action=action
        )

        logger.debug(_training)

        self.ws.send(json.dumps(_training, indent=4))

    def training_signature_action(self, detection: Literal['mentalCommand', 'facialExpression'], **kwargs: str) -> None:  # noqa: D417
        """Get the list of trained actions of a profile.

        Args:
            detection (Literal['mentalCommand', 'facialExpression']): The detection type.

        Keyword Args:
            profile_name (str): The profile name.
            session_id (str): The session ID.

        """
        logger.info('--- Getting the list of trained actions ---')

        _training = trained_signature_actions(auth=self.auth, detection=detection, **kwargs)

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

        _training = training_time(auth=self.auth, session_id=self.session_id, detection=detection)

        logger.debug(_training)

        self.ws.send(json.dumps(_training, indent=4))

    def get_mental_command_action_sensitive(self, profile_name: str) -> None:
        """Get the mental command action sensitivity.

        Args:
            profile_name (str): The profile name.

        """
        logger.info('--- Getting mental command action sensitivity ---')

        _sensitivity = action_sensitivity(auth=self.auth, profile_name=profile_name, status='get')

        logger.debug(_sensitivity)

        self.ws.send(json.dumps(_sensitivity, indent=4))

    def set_mental_command_action_sensitive(self, profile_name: str, values: list[int]) -> None:
        """Set the mental command action sensitivity.

        Args:
            profile_name (str): The profile name.
            values (list[int]): The sensitivity values.

        """
        logger.info('--- Setting mental command action sensitivity ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _sensitivity = action_sensitivity(
            auth=self.auth, profile_name=profile_name, session_id=self.session_id, values=values, status='set'
        )

        logger.debug(_sensitivity)

        self.ws.send(json.dumps(_sensitivity, indent=4))

    def get_mental_command_active_action(self, profile_name: str) -> None:
        """Get the active mental command action.

        Args:
            profile_name (str): The profile name.

        """
        logger.info('--- Getting mental command active action ---')

        _action = active_action(auth=self.auth, status='get', profile_name=profile_name)

        logger.debug(_action)

        self.ws.send(json.dumps(_action, indent=4))

    def set_mental_command_active_action(self, actions: list[str]) -> None:
        """Set the active mental command action.

        Args:
            actions (list[str]): The actions.

        """
        logger.info('--- Setting mental command active action ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _action = active_action(auth=self.auth, status='set', session_id=self.session_id, actions=actions)

        logger.debug(_action)

        self.ws.send(json.dumps(_action, indent=4))

    def get_mental_command_brain_map(self, profile_name: str) -> None:
        """Get the mental command brain map.

        Args:
            profile_name (str): The profile name.

        """
        logger.info('--- Getting mental command brain map ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _brain_map = brain_map(auth=self.auth, session_id=self.session_id, profile_name=profile_name)

        logger.debug(_brain_map)

        self.ws.send(json.dumps(_brain_map, indent=4))

    def get_mental_command_training_threshold(self, profile_name: str) -> None:
        """Get the mental command training threshold.

        Args:
            profile_name (str): The profile name.

        """
        logger.info('--- Getting mental command training threshold ---')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        _threshold = training_threshold(auth=self.auth, profile_name=profile_name, session_id=self.session_id)

        logger.debug(_threshold)

        self.ws.send(json.dumps(_threshold, indent=4))
