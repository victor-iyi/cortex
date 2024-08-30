"""Headset API.

This module contains the Headset class, which is used to interact with the Emotiv headset.

"""

# mypy: disable-error-code=has-type

import time as m_time
from collections.abc import Callable, Mapping
from typing import Any

from cortex.api.events import (
    ErrorEvent,
    MarkerEvent,
    MentalCommandEvent,
    NewDataEvent,
    ProfileEvent,
    RecordEvent,
    SessionEvent,
    WarningEvent,
)
from cortex.api.handler import stream_data
from cortex.api.id import AuthID, HeadsetID, MarkersID, MentalCommandID, ProfileID, RecordsID, SessionID
from cortex.consts import WarningCode
from cortex.cortex import Cortex
from cortex.logging import logger


class Headset(Cortex):
    """The Headset class.

    This class is used to interact with the Emotiv headset.

    """

    _events_: list[str] = [
        *ErrorEvent.get_events(),
        *MarkerEvent.get_events(),
        *MentalCommandEvent.get_events(),
        *NewDataEvent.get_events(),
        *ProfileEvent.get_events(),
        *RecordEvent.get_events(),
        *SessionEvent.get_events(),
        *WarningEvent.get_events(),
    ]

    def __init__(self, *args: str, **kwargs: bool | str | int) -> None:
        """Initialize the Headset class."""
        super().__init__(*args, **kwargs)
        self._headset_list: list[dict[str, Any]] | None = None

    def extract_data_labels(self, stream_name: str, stream_cols: list[str]) -> None:
        """Extract data labels from a data stream.

        Args:
            stream_name (str): The name of the stream.
            stream_cols (list[str]): The list of columns that are part of this stream.

        Read More:
            [subscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/subscribe)

        """
        labels = {}
        labels['streamName'] = stream_name

        data_labels = []
        if stream_name == 'eeg':
            # remove MARKERS
            data_labels = stream_cols[:-1]
        elif stream_name == 'dev':
            # get cq header column except battery, signal and battery percent
            data_labels = stream_cols[2]  # type: ignore[assignment]
        else:
            data_labels = stream_cols

        labels['labels'] = data_labels  # type: ignore[assignment]
        logger.debug(labels)
        self.emit('new_data_labels', data=labels)

    def handle_error(self, response: Mapping[str, Any]) -> None:
        """Handle the error response.

        Args:
            response (Mapping[str, Any]): The error response to handle.

        """
        request_id = response['id']

        logger.error(f'handle_error: Request ID: {request_id}')
        logger.debug(response)

        self.emit('inform_error', error_data=response['error'])

    def handle_warning(self, response: Mapping[str, Any]) -> None:
        """Handle the warning response.

        Args:
            response (Mapping[str, Any]): The warning response to handle.

        """
        logger.debug('Handling warning response.')
        logger.debug(response)

        code = response['code']
        message = response['message']

        if code == WarningCode.ACCESS_RIGHT_GRANTED:
            # Call authorize again.
            logger.warning('Authorizing again...')
            self.authorize()
        elif code == WarningCode.HEADSET_CONNECTED:
            # Query headset again, then create session.
            logger.warning('Querying headset again...')
            self.query_headset()
        elif code == WarningCode.CORTEX_AUTO_UNLOAD_PROFILE:
            # Unload the profile.
            logger.warning('Setting profile name to empty...')
            self.profile_name = ''
        elif code == WarningCode.CORTEX_STOP_ALL_STREAMS:
            logger.debug(message.get('behavior'))

            session_id = message['sessionId']
            if session_id == self.session_id:
                logger.warning('Stopping all streams...')
                self.emit('warn_cortex_stop_all_sub', data=session_id)
                self.session_id = ''

    def handle_stream_data(self, data: Mapping[str, Any]) -> None:
        """Handle the stream data.

        Args:
            data (Mapping[str, Any]): The data to handle.

        """
        _stream_maps = {
            'com': 'new_com_data',
            'fac': 'new_fe_data',
            'eeg': 'new_eeg_data',
            'mot': 'new_mot_data',
            'dev': 'new_dev_data',
            'met': 'new_met_data',
            'pow': 'new_pow_data',
            'sys': 'new_sys_data',
        }
        for stream, event in _stream_maps.items():
            if data.get(stream) is not None:
                self.emit(event, stream_data(data, stream))
                break
        else:
            logger.warning(f'Unknown data: {data}')

    def handle_result(self, response: Mapping[str, Any]) -> None:
        """Handle the result response.

        Args:
            response (Mapping[str, Any]): The result response to handle.

        """
        logger.debug('Handling result response.')
        logger.debug(response)

        req_id = response['id']
        result = response['result']

        _handler_map = {
            # Auth.
            AuthID.HAS_ACCESS_RIGHT: self._handle_has_access_right,
            AuthID.REQUEST_ACCESS: self._handle_request_access,
            AuthID.AUTHORIZE: self._handle_authorize,
            # Headset.
            HeadsetID.DISCONNECT: self._handle_disconnect_headset,
            HeadsetID.QUERY_HEADSET: self._handle_query_headset,
            HeadsetID.SUBSCRIBE: self._handle_sub_request,
            HeadsetID.UNSUBSCRIBE: self._handle_unsub_request,
            # Profile.
            ProfileID.QUERY: self._handle_query_profile,
            ProfileID.SETUP: self._handle_setup_profile,
            ProfileID.CURRENT: self._handle_get_current_profile,
            # Record.
            RecordsID.CREATE: self._handle_create_record,
            RecordsID.STOP: self._handle_stop_record,
            RecordsID.EXPORT: self._handle_export_record,
            # Session.
            SessionID.CREATE: self._handle_create_session,
            # Marker.
            MarkersID.INJECT: self._handle_inject_marker,
            # Mental Command.
            MentalCommandID.ACTION_SENSITIVITY: self._handle_mental_command_action_sensitive,
            MentalCommandID.BRAIN_MAP: self._handle_mental_command_brain_map,
            MentalCommandID.TRAINING_THRESHOLD: self._handle_mental_command_training_threshold,
        }

        _handler: Callable[[dict[str, Any] | list[dict[str, Any]]], None] = _handler_map.get(  # type: ignore[assignment]
            req_id, self._handle_default
        )
        _handler(result)

    def _handle_has_access_right(self, result: dict[str, Any]) -> None:
        access_granted = result['accessGranted']
        if access_granted:
            self.authorize()
        else:
            self.request_access()

    def _handle_request_access(self, result: dict[str, Any]) -> None:
        access_granted = result['accessGranted']
        if access_granted:
            self.authorize()
        else:
            msg = result['message']
            logger.warning(msg)

    def _handle_authorize(self, result: dict[str, Any]) -> None:
        logger.info('Authorize successful.')
        self._auth = result['cortexToken']
        self.query_headset()

    def _handle_query_headset(self, results: list[dict[str, Any]]) -> None:
        self._headset_list = results
        found_headset = False
        headset_status = ''

        for headset in self._headset_list:
            hs_id = headset['id']
            status = headset['status']
            connected_by = headset['connectedBy']

            logger.info(f'Headset ID: {hs_id}, Status: {status}, Connected by: {connected_by}')

            if not self.headset_id and self.headset_id == hs_id:
                found_headset = True
                headset_status = status

        if len(self._headset_list) == 0:
            logger.warning('No headset available. Please turn on a headset.')
        elif not self.headset_id:
            self.headset_id: str = self._headset_list[0]['id']
            self.query_headset()
        elif found_headset:
            self._handle_headset_found(headset_status)
        else:
            logger.warning(f'Cannot find the headset {self.headset_id}. Please make sure the ID is correct.')

    def _handle_headset_found(self, status: str) -> None:
        if status == 'connected':
            self.create_session()
        elif status == 'discovered':
            self.connect()
        elif status == 'connecting':
            m_time.sleep(3)
            self.query_headset()
        else:
            logger.warning(f'Invalid connection status: {status}')

    def _handle_create_session(self, result: dict[str, Any]) -> None:
        self.session_id = result['id']
        logger.info(f'Session created: {self.session_id}')
        self.emit('create_session_done', data=self.session_id)

    def _handle_sub_request(self, result: dict[str, Any]) -> None:
        for stream in result['success']:
            stream_name = stream['streamName']
            stream_labels = stream['cols']
            logger.info(f'Subscribed to {stream_name} with labels {stream_labels}')
            if stream_name not in ('com', 'fac'):
                self.extract_data_labels(stream_name, stream_labels)

        for stream in result['failure']:
            stream_name = stream['streamName']
            stream_msg = stream['message']
            logger.error(f'The data stream {stream_name} failed to subscribe: {stream_msg}')

    def _handle_unsub_request(self, result: dict[str, Any]) -> None:
        for stream in result['success']:
            stream_name = stream['streamName']
            logger.info(f'Unsubscribed from {stream_name} successfully.')

        for stream in result['failure']:
            stream_name = stream['streamName']
            stream_msg = stream['message']
            logger.error(f'The data stream {stream_name} failed to unsubscribe: {stream_msg}')

    def _handle_query_profile(self, results: list[dict[str, Any]]) -> None:
        profile_list = [headset['name'] for headset in results]
        self.emit('query_profile_done', data=profile_list)

    def _handle_setup_profile(self, result: dict[str, Any]) -> None:
        action = result['action']
        if action == 'create':
            profile_name = result['name']
            if profile_name == self.profile_name:
                self.setup_profile('load', profile_name=profile_name)
        elif action == 'load':
            logger.info('Profile loaded successfully.')
            self.emit('load_unload_profile_done', isLoaded=True)
        elif action == 'unload':
            logger.info('Profile unloaded successfully.')
            self.emit('load_unload_profile_done', isLoaded=False)
        elif action == 'save':
            logger.info('Profile saved successfully.')
            self.emit('save_profile_done')

    def _handle_get_current_profile(self, result: dict[str, Any]) -> None:
        name = result.get('name')
        if not name:
            logger.warning(f'No profile loaded with {self.headset_id}')
            self.setup_profile('load', profile_name=self.profile_name)
        else:
            loaded_by_this_app = result.get('loadedByThisApp')
            logger.info(f'Profile loaded: {name}, Loaded by this app: {loaded_by_this_app}')
            if name != self.profile_name:
                logger.warning(f'Profile {name} is loaded for headset {self.headset_id}')
            elif loaded_by_this_app:
                self.emit('load_unload_profile_done', isLoaded=True)
            else:
                self.setup_profile('unload', profile_name=self.profile_name)

    def _handle_disconnect_headset(self, _result: dict[str, Any]) -> None:
        logger.info(f'Headset {self.headset_id} disconnected.')
        self.headset_id = ''

    def _handle_create_record(self, result: dict[str, Any]) -> None:
        self.record_id = result['record']['uuid']
        self.emit('create_record_done', data=result['record'])

    def _handle_stop_record(self, result: dict[str, Any]) -> None:
        self.emit('stop_record_done', data=result['record'])

    def _handle_export_record(self, result: dict[str, Any]) -> None:
        success_exports = [record['recordId'] for record in result['success']]
        for record in result['failure']:
            record_id = record['recordId']
            message = record['message']
            logger.error(f'Export failed for record {record_id}: {message}')
        self.emit('export_record_done', data=success_exports)

    def _handle_inject_marker(self, result: dict[str, Any]) -> None:
        self.emit('inject_marker_done', data=result['marker'])

    def _handle_mental_command_active_action(self, result: dict[str, Any]) -> None:
        self.emit('get_mc_active_action_done', data=result)

    def _handle_mental_command_training_threshold(self, result: dict[str, Any]) -> None:
        self.emit('mc_training_threshold_done', data=result)

    def _handle_mental_command_brain_map(self, result: dict[str, Any]) -> None:
        self.emit('mc_brain_map_done', data=result)

    def _handle_mental_command_action_sensitive(self, result: dict[str, Any]) -> None:
        self.emit('mc_action_sensitivity_done', data=result)

    def _handle_default(self, result: dict[str, Any]) -> None:
        logger.error('No handling for the result of response.')
        logger.debug(result)
