import json
import os
import ssl
import threading
import time
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import websocket
from pydispatch import Dispatcher

# define request id
QUERY_HEADSET_ID = 1
CONNECT_HEADSET_ID = 2
REQUEST_ACCESS_ID = 3
AUTHORIZE_ID = 4
CREATE_SESSION_ID = 5
SUB_REQUEST_ID = 6
SETUP_PROFILE_ID = 7
QUERY_PROFILE_ID = 8
TRAINING_ID = 9
DISCONNECT_HEADSET_ID = 10
CREATE_RECORD_REQUEST_ID = 11
STOP_RECORD_REQUEST_ID = 12
EXPORT_RECORD_ID = 13
INJECT_MARKER_REQUEST_ID = 14
SENSITIVITY_REQUEST_ID = 15
MENTAL_COMMAND_ACTIVE_ACTION_ID = 16
MENTAL_COMMAND_BRAIN_MAP_ID = 17
MENTAL_COMMAND_TRAINING_THRESHOLD = 18
SET_MENTAL_COMMAND_ACTIVE_ACTION_ID = 19
HAS_ACCESS_RIGHT_ID = 20
GET_CURRENT_PROFILE_ID = 21
GET_CORTEX_INFO_ID = 22
UPDATE_MARKER_REQUEST_ID = 23
UNSUB_REQUEST_ID = 24

# define error_code
ERR_PROFILE_ACCESS_DENIED = -32046

# define warning code
CORTEX_STOP_ALL_STREAMS = 0
CORTEX_CLOSE_SESSION = 1
USER_LOGIN = 2
USER_LOGOUT = 3
ACCESS_RIGHT_GRANTED = 9
ACCESS_RIGHT_REJECTED = 10
PROFILE_LOADED = 13
PROFILE_UNLOADED = 14
CORTEX_AUTO_UNLOAD_PROFILE = 15
EULA_ACCEPTED = 17
DISKSPACE_LOW = 19
DISKSPACE_CRITICAL = 20
HEADSET_CANNOT_CONNECT_TIMEOUT = 102
HEADSET_DISCONNECTED_TIMEOUT = 103
HEADSET_CONNECTED = 104
HEADSET_CANNOT_WORK_WITH_BTLE = 112
HEADSET_CANNOT_CONNECT_DISABLE_MOTION = 113


class Cortex(Dispatcher):
    _events_ = [
        'inform_error',
        'create_session_done',
        'query_profile_done',
        'load_unload_profile_done',
        'save_profile_done',
        'get_mc_active_action_done',
        'mc_brainmap_done',
        'mc_action_sensitivity_done',
        'mc_training_threshold_done',
        'create_record_done',
        'stop_record_done',
        'warn_cortex_stop_all_sub',
        'inject_marker_done',
        'update_marker_done',
        'export_record_done',
        'new_data_labels',
        'new_com_data',
        'new_fe_data',
        'new_eeg_data',
        'new_mot_data',
        'new_dev_data',
        'new_met_data',
        'new_pow_data',
        'new_sys_data',
    ]

    def __init__(
        self,
        client_id: str = '',
        client_secret: str = '',
        debug_mode: bool = False,
        **kwargs: Any,
    ) -> None:
        self.client_id = os.environ.get('CLIENT_ID', client_id)
        self.client_secret = os.environ.get('CLIENT_SECRET', client_secret)

        if not self.client_id:
            raise ValueError(
                'Empty CLIENT_ID. Make sure to add CLIENT_ID to your environment variables.',
            )

        if not self.client_secret:
            raise ValueError(
                'Empty CLIENT_SECRET. Make sure to add CLIENT_SECRET to your environment variables.',
            )

        self.debug = debug_mode

        self.session_id: str = kwargs.get('session_id', '')
        self.headset_id: str = kwargs.get('headset_id', '')
        self.debit: int = kwargs.get('debit', 10)
        self.license: str = kwargs.get('license', '')

    def open(self) -> None:
        url = 'wss://localhost:6868'
        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            url,
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        thread_name = f'WebsockThread:-{datetime.utcnow():%Y%m%d%H%M%S}'

        # As default, a Emotiv self-signed certificate is required.
        # If you don't want to use the certificate,
        # please replace by the below line  by sslopt={'cert_reqs': ssl.CERT_NONE}
        ca_certs = Path(__file__).resolve().parent.parent / 'certificates/rootCA.pem'
        if ca_certs.exists():
            sslopt = {
                'ca_certs': ca_certs,
                'cert_reqs': ssl.CERT_REQUIRED,
            }
        else:
            warnings.warn(
                'No certificate file found. Please check the certificate folder.',
            )
            sslopt = {'cert_reqs': ssl.CERT_NONE}

        self.websock_thread = threading.Thread(
            target=self.ws.run_forever,
            args=(None, sslopt),
            name=thread_name,
        )
        self.websock_thread.start()
        self.websock_thread.join()

    def close(self) -> None:
        self.ws.close()

    def set_wanted_headset(self, headset_id: str) -> None:
        self.headset_id = headset_id

    def set_wanted_profile(self, profile_name: str) -> None:
        self.profile_name = profile_name

    def on_open(self, *args: Any, **kwargs: Any) -> None:
        print('websocket opened')
        self.do_prepare_steps()

    def on_error(self, *args: Any) -> None:
        if len(args) == 2:
            print(str(args[1]))

    def on_close(self, *args: Any, **kwargs: Any) -> None:
        print('on_close')
        print(args[1])

    def handle_result(self, response: dict[str, Any]) -> None:  # noqa: C901
        if self.debug:
            print(response)

        req_id = response['id']
        result_dic = response['result']

        # already has access.
        if req_id == HAS_ACCESS_RIGHT_ID:
            access_granted: bool = result_dic['accessGranted']
            if access_granted:
                # authorize
                self.authorize()
            else:
                # request access
                self.request_access()
        # request access.
        elif req_id == REQUEST_ACCESS_ID:
            access_granted = result_dic['accessGranted']

            if access_granted:
                # authorize
                self.authorize()
            else:
                # wait approve from Emotiv Launcher
                msg = result_dic['message']
                warnings.warn(msg)
        # authorize.
        elif req_id == AUTHORIZE_ID:
            print('Authorize successfully.')
            self.auth = result_dic['cortexToken']
            # query headsets
            self.query_headset()
        # query headset.
        elif req_id == QUERY_HEADSET_ID:
            self.headset_list = result_dic
            found_headset = False
            headset_status = ''
            for headset in self.headset_list:
                hs_id = headset['id']
                status = headset['status']
                connected_by = headset['connectedBy']
                print(f'headsetId: {hs_id}, status: {status}, connected_by: {connected_by}')
                if not self.headset_id and self.headset_id == hs_id:
                    found_headset = True
                    headset_status = status

            # no headset available.
            if len(self.headset_list) == 0:
                warnings.warn('No headset available. Please turn on a headset.')
            # no headset found.
            elif not self.headset_id:
                # set first headset is default headset
                self.headset_id = self.headset_list[0]['id']
                # call query headet again
                self.query_headset()
            # headset found.
            elif found_headset:
                if headset_status == 'connected':
                    # create session with the headset
                    self.create_session()
                elif headset_status == 'discovered':
                    self.connect_headset(self.headset_id)
                elif headset_status == 'connecting':
                    # wait 3 seconds and query headset again
                    time.sleep(3)
                    self.query_headset()
                else:
                    warnings.warn(
                        f'query_headset resp: Invalid connection status {headset_status}',
                    )
            elif not found_headset:
                warnings.warn(
                    f'Can not found the headset {self.headset_id}. Please make sure the id is correct.',
                )

        # create session.
        elif req_id == CREATE_SESSION_ID:
            self.session_id = result_dic['id']
            print(f'The session {self.session_id} is created successfully.')
            self.emit('create_session_done', data=self.session_id)

        # subscribe to data stream.
        elif req_id == SUB_REQUEST_ID:
            # handle data label
            for stream in result_dic['success']:
                stream_name = stream['streamName']
                stream_labels = stream['cols']
                print(
                    f'The data stream {stream_name} is subscribed successfully.',
                )
                # ignore com, fac and sys data label because they are handled in on_new_data
                if stream_name != 'com' and stream_name != 'fac':
                    self.extract_data_labels(stream_name, stream_labels)

            for stream in result_dic['failure']:
                stream_name = stream['streamName']
                stream_msg = stream['message']
                print(
                    f'The data stream {stream_name} is subscribed unsuccessfully. Because: {stream_msg}',
                )

        # unsubscribe to data stream.
        elif req_id == UNSUB_REQUEST_ID:
            for stream in result_dic['success']:
                stream_name = stream['streamName']
                print(
                    f'The data stream {stream_name} is unsubscribed successfully.',
                )

            for stream in result_dic['failure']:
                stream_name = stream['streamName']
                stream_msg = stream['message']
                print(
                    f'The data stream {stream_name} is unsubscribed unsuccessfully. Because: {stream_msg}',
                )

        # Query profile.
        elif req_id == QUERY_PROFILE_ID:
            profile_list = []
            for headset in result_dic:
                name = headset['name']
                profile_list.append(name)
            self.emit('query_profile_done', data=profile_list)

        # Setup profile.
        elif req_id == SETUP_PROFILE_ID:
            action = result_dic['action']
            if action == 'create':
                profile_name = result_dic['name']
                if profile_name == self.profile_name:
                    # load profile
                    self.setup_profile(profile_name, 'load')
            elif action == 'load':
                print('load profile successfully')
                self.emit('load_unload_profile_done', isLoaded=True)
            elif action == 'unload':
                self.emit('load_unload_profile_done', isLoaded=False)
            elif action == 'save':
                self.emit('save_profile_done')

        # Get current profile.
        elif req_id == GET_CURRENT_PROFILE_ID:
            print(result_dic)
            name = result_dic['name']
            if name is None:
                # no profile loaded with the headset
                print(
                    f'get_current_profile: no profile loaded with the headset {self.headset_id}',
                )
                self.setup_profile(self.profile_name, 'load')
            else:
                loaded_by_this_app = result_dic['loadedByThisApp']
                print(
                    f'get current profile response: {name}, loadedByThisApp: {loaded_by_this_app}',
                )
                if name != self.profile_name:
                    warnings.warn(
                        f'There is profile {name} is loaded for headset {self.headset_id}',
                    )
                elif loaded_by_this_app:
                    self.emit('load_unload_profile_done', isLoaded=True)
                else:
                    self.setup_profile(self.profile_name, 'unload')
                    # warnings.warn('The profile ' + name + ' is loaded by other applications')

        elif req_id == DISCONNECT_HEADSET_ID:
            print(f'Disconnect headset {self.headset_id}')
            self.headset_id = ''
        elif req_id == MENTAL_COMMAND_ACTIVE_ACTION_ID:
            self.emit('get_mc_active_action_done', data=result_dic)
        elif req_id == MENTAL_COMMAND_TRAINING_THRESHOLD:
            self.emit('mc_training_threshold_done', data=result_dic)
        elif req_id == MENTAL_COMMAND_BRAIN_MAP_ID:
            self.emit('mc_brainmap_done', data=result_dic)
        elif req_id == SENSITIVITY_REQUEST_ID:
            self.emit('mc_action_sensitivity_done', data=result_dic)
        elif req_id == CREATE_RECORD_REQUEST_ID:
            self.record_id = result_dic['record']['uuid']
            self.emit('create_record_done', data=result_dic['record'])
        elif req_id == STOP_RECORD_REQUEST_ID:
            self.emit('stop_record_done', data=result_dic['record'])
        elif req_id == EXPORT_RECORD_ID:
            # handle data lable
            success_export = []
            for record in result_dic['success']:
                record_id = record['recordId']
                success_export.append(record_id)

            for record in result_dic['failure']:
                record_id = record['recordId']
                failure_msg = record['message']
                print(
                    f'export_record resp failure cases: {record_id}: {failure_msg}',
                )

            self.emit('export_record_done', data=success_export)
        elif req_id == INJECT_MARKER_REQUEST_ID:
            self.emit('inject_marker_done', data=result_dic['marker'])
        elif req_id == INJECT_MARKER_REQUEST_ID:
            self.emit('update_marker_done', data=result_dic['marker'])
        else:
            print(f'No handling for response of request {req_id}')

    def handle_error(self, recv_dic: dict[str, Any]) -> None:
        req_id = recv_dic['id']
        print(f'handle_error: request Id {req_id}')
        self.emit('inform_error', error_data=recv_dic['error'])

    def handle_warning(self, warning_resp: dict[str, Any]) -> None:
        if self.debug:
            print(warning_resp)
        warning_code = warning_resp['code']
        warning_msg = warning_resp['message']
        if warning_code == ACCESS_RIGHT_GRANTED:
            # call authorize again
            self.authorize()
        elif warning_code == HEADSET_CONNECTED:
            # query headset again then create session
            self.query_headset()
        elif warning_code == CORTEX_AUTO_UNLOAD_PROFILE:
            self.profile_name = ''
        elif warning_code == CORTEX_STOP_ALL_STREAMS:
            # print(warning_msg['behavior'])
            session_id = warning_msg['sessionId']
            if session_id == self.session_id:
                self.emit('warn_cortex_stop_all_sub', data=session_id)
                self.session_id = ''

    def handle_stream_data(self, result_dic: dict[str, Any]) -> None:
        if result_dic.get('com') is not None:
            com_data = {}
            com_data['action'] = result_dic['com'][0]
            com_data['power'] = result_dic['com'][1]
            com_data['time'] = result_dic['time']
            self.emit('new_com_data', data=com_data)

        elif result_dic.get('fac') is not None:
            fe_data = {}
            fe_data['eyeAct'] = result_dic['fac'][0]  # eye action
            fe_data['uAct'] = result_dic['fac'][1]  # upper action
            fe_data['uPow'] = result_dic['fac'][2]  # upper action power
            fe_data['lAct'] = result_dic['fac'][3]  # lower action
            fe_data['lPow'] = result_dic['fac'][4]  # lower action power
            fe_data['time'] = result_dic['time']
            self.emit('new_fe_data', data=fe_data)

        elif result_dic.get('eeg') is not None:
            eeg_data = {}
            eeg_data['eeg'] = result_dic['eeg']
            eeg_data['eeg'].pop()  # remove markers
            eeg_data['time'] = result_dic['time']
            self.emit('new_eeg_data', data=eeg_data)

        elif result_dic.get('mot') is not None:
            mot_data = {}
            mot_data['mot'] = result_dic['mot']
            mot_data['time'] = result_dic['time']
            self.emit('new_mot_data', data=mot_data)

        elif result_dic.get('dev') is not None:
            dev_data = {}
            dev_data['signal'] = result_dic['dev'][1]
            dev_data['dev'] = result_dic['dev'][2]
            dev_data['batteryPercent'] = result_dic['dev'][3]
            dev_data['time'] = result_dic['time']
            self.emit('new_dev_data', data=dev_data)

        elif result_dic.get('met') is not None:
            met_data = {}
            met_data['met'] = result_dic['met']
            met_data['time'] = result_dic['time']
            self.emit('new_met_data', data=met_data)

        elif result_dic.get('pow') is not None:
            pow_data = {}
            pow_data['pow'] = result_dic['pow']
            pow_data['time'] = result_dic['time']
            self.emit('new_pow_data', data=pow_data)

        elif result_dic.get('sys') is not None:
            sys_data = result_dic['sys']
            self.emit('new_sys_data', data=sys_data)

        else:
            print(result_dic)

    def on_message(self, *args: Any) -> None:
        recv_dic = json.loads(args[1])
        if 'sid' in recv_dic:
            self.handle_stream_data(recv_dic)
        elif 'result' in recv_dic:
            self.handle_result(recv_dic)
        elif 'error' in recv_dic:
            self.handle_error(recv_dic)
        elif 'warning' in recv_dic:
            self.handle_warning(recv_dic['warning'])
        else:
            raise KeyError

    def query_headset(self) -> None:
        """Shows details of any headsets connected to the device via USB
        dongle, USB cable, or Bluetooth.

        You can query a specific headset by its id, or you can specify a wildcard
        for partial matching.

        Read More:
            [queryHeadsets](https://emotiv.gitbook.io/cortex-api/headset/queryheadsets)

        """
        print('query headset --------------------------------')
        query_headset_request = {
            'jsonrpc': '2.0',
            'id': QUERY_HEADSET_ID,
            'method': 'queryHeadsets',
            'params': {},
        }
        if self.debug:
            print(
                'queryHeadsets request\n',
                json.dumps(query_headset_request, indent=4),
            )

        self.ws.send(json.dumps(query_headset_request, indent=4))

    def connect_headset(self, headset_id: str) -> None:
        """Connect to a headset.

        It can also refresh the list of available Bluetooth headsets returned by
        `queryHeadsets`. Please note that connecting and disconnecting a headset
        can take a few seconds. Before you call `createSession` on a headset,
        make sure that Cortex is connected to this headset. You can use
        `queryHeadsets` to check the connection status of the headset.

        Args:
            headset_id (str): The id of the headset to connect to.

        See Also:
            `query_headset`
            `create_session`

        Read More:
            [controlDevice](https://emotiv.gitbook.io/cortex-api/headset/controldevice)

        """
        print('connect headset --------------------------------')
        connect_headset_request = {
            'jsonrpc': '2.0',
            'id': CONNECT_HEADSET_ID,
            'method': 'controlDevice',
            'params': {
                'command': 'connect',
                'headset': headset_id,
            },
        }
        if self.debug:
            print(
                'controlDevice request\n',
                json.dumps(connect_headset_request, indent=4),
            )

        self.ws.send(json.dumps(connect_headset_request, indent=4))

    def request_access(self) -> None:
        """Request user approval for the current application through [EMOTIV
        Launcher].

        When your application calls this method for the first time, [EMOTIV Launcher]
        displays a message to approve your application.

        [Emotiv Launcher]: https://emotiv.gitbook.io/emotiv-launcher/

        Read More:
            [requestAccess](https://emotiv.gitbook.io/cortex-api/authentication/requestaccess)

        """
        print('request access --------------------------------')
        request_access_request = {
            'jsonrpc': '2.0',
            'method': 'requestAccess',
            'params': {
                'clientId': self.client_id,
                'clientSecret': self.client_secret,
            },
            'id': REQUEST_ACCESS_ID,
        }

        self.ws.send(json.dumps(request_access_request, indent=4))

    def has_access_right(self) -> None:
        """Check if your application has been granted access rights in [EMOTIV
        Launcher].

        [Emotiv Launcher]: https://emotiv.gitbook.io/emotiv-launcher/

        See Also:
            `request_access`

        Read More:
            [hasAccessRight](https://emotiv.gitbook.io/cortex-api/authentication/hasaccessright)

        """
        print('check has access right --------------------------------')
        has_access_request = {
            'jsonrpc': '2.0',
            'method': 'hasAccessRight',
            'params': {
                'clientId': self.client_id,
                'clientSecret': self.client_secret,
            },
            'id': HAS_ACCESS_RIGHT_ID,
        }
        self.ws.send(json.dumps(has_access_request, indent=4))

    def authorize(self) -> None:
        """This method is to generate a Cortex access token.

        Most of the methods of the Cortex API require this token as a parameter.
        Application can specify the license key and the amount of sessions to be
        debited from the license and use them locally.

        Read More:
            [authorize](https://emotiv.gitbook.io/cortex-api/authentication/authorize)

        """
        print('authorize --------------------------------')
        authorize_request = {
            'jsonrpc': '2.0',
            'method': 'authorize',
            'params': {
                'clientId': self.client_id,
                'clientSecret': self.client_secret,
                'license': self.license,
                'debit': self.debit,
            },
            'id': AUTHORIZE_ID,
        }

        if self.debug:
            print('auth request \n', json.dumps(authorize_request, indent=4))

        self.ws.send(json.dumps(authorize_request))

    def create_session(self) -> None:
        """Open a session with an EMOTIV headset.

        To open a session with a headset, the status of the headset must be
        "connected". If the status is "discovered", then you must call `controlDevice`
        to connect the headset.
        You cannot open a session with a headset connected by a USB cable.
        You can use `queryHeadsets` to check the status and connection type of the headset.

        Read More:
            [createSession](https://emotiv.gitbook.io/cortex-api/session/createsession)

        """
        if self.session_id != '':
            warnings.warn(f'There is existed session {self.session_id}')
            return

        print('create session --------------------------------')
        create_session_request = {
            'jsonrpc': '2.0',
            'id': CREATE_SESSION_ID,
            'method': 'createSession',
            'params': {
                'cortexToken': self.auth,
                'headset': self.headset_id,
                'status': 'active',
            },
        }

        if self.debug:
            print(
                'create session request\n',
                json.dumps(create_session_request, indent=4),
            )

        self.ws.send(json.dumps(create_session_request))

    def close_session(self) -> None:
        """Close a session with an EMOTIV headset.

        Read More:
            [updateSession](https://emotiv.gitbook.io/cortex-api/session/updatesession)

        """
        print('close session --------------------------------')
        close_session_request = {
            'jsonrpc': '2.0',
            'id': CREATE_SESSION_ID,
            'method': 'updateSession',
            'params': {
                'cortexToken': self.auth,
                'session': self.session_id,
                'status': 'close',
            },
        }

        self.ws.send(json.dumps(close_session_request))

    def get_cortex_info(self) -> None:
        """Return information about the Cortex service, like its version and
        build number.

        Read More:
            [getCortexInfo](https://emotiv.gitbook.io/cortex-api/authentication/getcortexinfo)

        """
        print('get cortex version --------------------------------')
        get_cortex_info_request = {
            'jsonrpc': '2.0',
            'method': 'getCortexInfo',
            'id': GET_CORTEX_INFO_ID,
        }

        self.ws.send(json.dumps(get_cortex_info_request))

    def do_prepare_steps(self) -> None:
        """Prepare steps include:

        Step 1:
          Check access right. If user has not granted for the application,
          `requestAccess` will be called

        Step 2:
          Authorize: to generate a Cortex access token which is required
          parameter of many APIs.

        Step 3:
          Connect a headset. If no wanted headet is set, the first headset in
          the list will be connected.
          If you use EPOC Flex headset, you should connect the headset with a
          proper mappings via EMOTIV Launcher first.

        Step 4:
          Create a working session with the connected headset.

        Returns:
          None

        """
        print('do_prepare_steps--------------------------------')
        # check access right
        self.has_access_right()

    def disconnect_headset(self) -> None:
        """Disconnect a headset.

        Read More:
            [controlDevice](https://emotiv.gitbook.io/cortex-api/headset/controldevice)

        """
        print('disconnect headset --------------------------------')
        disconnect_headset_request = {
            'jsonrpc': '2.0',
            'id': DISCONNECT_HEADSET_ID,
            'method': 'controlDevice',
            'params': {
                'command': 'disconnect',
                'headset': self.headset_id,
            },
        }

        self.ws.send(json.dumps(disconnect_headset_request))

    def sub_request(self, streams: list[str]) -> None:
        """Subscribe to one or more data stream.

        Args:
            streams (list[str]): list of data stream you wan to subscribe to.

        Read More:
            [subscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/subscribe)

        """
        print('subscribe request --------------------------------')
        sub_request_json = {
            'jsonrpc': '2.0',
            'method': 'subscribe',
            'params': {
                'cortexToken': self.auth,
                'session': self.session_id,
                'streams': streams,
            },
            'id': SUB_REQUEST_ID,
        }
        if self.debug:
            print(
                'subscribe request\n',
                json.dumps(sub_request_json, indent=4),
            )

        self.ws.send(json.dumps(sub_request_json))

    def unsub_request(self, streams: list[str]) -> None:
        """Unsubscribe to one or more data stream.

        Args:
            streams (list[str]): list of data stream you wan to unsubscribe to.

        Read More:
            [unsubscribe](https://emotiv.gitbook.io/cortex-api/data-subscription/unsubscribe)

        """
        print('unsubscribe request --------------------------------')
        unsub_request_json = {
            'jsonrpc': '2.0',
            'method': 'unsubscribe',
            'params': {
                'cortexToken': self.auth,
                'session': self.session_id,
                'streams': streams,
            },
            'id': UNSUB_REQUEST_ID,
        }
        if self.debug:
            print(
                'unsubscribe request\n',
                json.dumps(unsub_request_json, indent=4),
            )

        self.ws.send(json.dumps(unsub_request_json))

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
        print(labels)
        self.emit('new_data_labels', data=labels)

    def query_profile(self) -> None:
        print('query profile --------------------------------')
        query_profile_json = {
            'jsonrpc': '2.0',
            'method': 'queryProfile',
            'params': {
                'cortexToken': self.auth,
            },
            'id': QUERY_PROFILE_ID,
        }

        if self.debug:
            print(
                'query profile request\n',
                json.dumps(query_profile_json, indent=4),
            )
            print('\n')

        self.ws.send(json.dumps(query_profile_json))

    def get_current_profile(self) -> None:
        print('get current profile:')
        get_profile_json = {
            'jsonrpc': '2.0',
            'method': 'getCurrentProfile',
            'params': {
                'cortexToken': self.auth,
                'headset': self.headset_id,
            },
            'id': GET_CURRENT_PROFILE_ID,
        }

        if self.debug:
            print(
                'get current profile json:\n',
                json.dumps(get_profile_json, indent=4),
            )
            print('\n')

        self.ws.send(json.dumps(get_profile_json))

    def setup_profile(
        self,
        profile_name: str,
        status: Literal['create', 'load', 'unload', 'save', 'rename', 'delete'],
    ) -> None:
        print('setup profile: ' + status + ' -------------------------------- ')
        setup_profile_json = {
            'jsonrpc': '2.0',
            'method': 'setupProfile',
            'params': {
                'cortexToken': self.auth,
                'headset': self.headset_id,
                'profile': profile_name,
                'status': status,
            },
            'id': SETUP_PROFILE_ID,
        }

        if self.debug:
            print(
                'setup profile json:\n',
                json.dumps(setup_profile_json, indent=4),
            )
            print('\n')

        self.ws.send(json.dumps(setup_profile_json))

    def train_request(
        self,
        detection: Literal['mentalCommand', 'facialExpression'],
        action: str,
        status: Literal['start', 'accept', 'reject', 'reset', 'erase'],
    ) -> None:
        print('train request --------------------------------')
        train_request_json = {
            'jsonrpc': '2.0',
            'method': 'training',
            'params': {
                'cortexToken': self.auth,
                'detection': detection,
                'session': self.session_id,
                'action': action,
                'status': status,
            },
            'id': TRAINING_ID,
        }
        if self.debug:
            print(
                'training request:\n',
                json.dumps(train_request_json, indent=4),
            )
            print('\n')

        self.ws.send(json.dumps(train_request_json))

    def create_record(self, title: str, **kwargs: Any) -> None:
        print('create record --------------------------------')

        if len(title) == 0:
            warnings.warn(
                'Empty record_title. Please fill the record_title before running script.',
            )
            # close socket
            self.close()
            return

        params_val = {
            'cortexToken': self.auth,
            'session': self.session_id,
            'title': title,
        }

        for key, value in kwargs.items():
            params_val.update({key: value})

        create_record_request = {
            'jsonrpc': '2.0',
            'method': 'createRecord',
            'params': params_val,
            'id': CREATE_RECORD_REQUEST_ID,
        }
        if self.debug:
            print(
                'create record request:\n',
                json.dumps(create_record_request, indent=4),
            )

        self.ws.send(json.dumps(create_record_request))

    def stop_record(self) -> None:
        print('stop record --------------------------------')
        stop_record_request = {
            'jsonrpc': '2.0',
            'method': 'stopRecord',
            'params': {
                'cortexToken': self.auth,
                'session': self.session_id,
            },
            'id': STOP_RECORD_REQUEST_ID,
        }
        if self.debug:
            print(
                'stop record request:\n',
                json.dumps(stop_record_request, indent=4),
            )
        self.ws.send(json.dumps(stop_record_request))

    def export_record(
        self,
        folder: str,
        stream_types: list[str],
        export_format: Literal['EDF', 'CSV'],
        record_ids: list[str],
        version: Literal['v2', 'v1'],
        **kwargs: Any,
    ) -> None:
        print('export record --------------------------------: ')
        # validate destination folder
        if len(folder) == 0:
            warnings.warn(
                'Invalid folder parameter. Please set a writable destination folder for exporting data.',
            )
            # close socket
            self.close()
            return

        params_val = {
            'cortexToken': self.auth,
            'folder': folder,
            'format': export_format,
            'streamTypes': stream_types,
            'recordIds': record_ids,
        }

        if export_format == 'CSV':
            params_val.update({'version': version})

        for key, value in kwargs.items():
            params_val.update({key: value})

        export_record_request = {
            'jsonrpc': '2.0',
            'id': EXPORT_RECORD_ID,
            'method': 'exportRecord',
            'params': params_val,
        }

        if self.debug:
            print(
                'export record request \n',
                json.dumps(export_record_request, indent=4),
            )

        self.ws.send(json.dumps(export_record_request))

    def inject_marker_request(
        self,
        time: int,
        value: str | int,
        label: str,
        **kwargs: Any,
    ) -> None:
        print('inject marker --------------------------------')
        params_val = {
            'cortexToken': self.auth,
            'session': self.session_id,
            'time': time,
            'value': value,
            'label': label,
        }

        for key, value in kwargs.items():
            params_val.update({key: value})

        inject_marker_request = {
            'jsonrpc': '2.0',
            'id': INJECT_MARKER_REQUEST_ID,
            'method': 'injectMarker',
            'params': params_val,
        }
        if self.debug:
            print(
                'inject marker request\n',
                json.dumps(inject_marker_request, indent=4),
            )
        self.ws.send(json.dumps(inject_marker_request))

    def update_marker_request(
        self,
        markerId: str,
        time: int,
        **kwargs: Any,
    ) -> None:
        print('update marker --------------------------------')
        params_val = {
            'cortexToken': self.auth,
            'session': self.session_id,
            'markerId': markerId,
            'time': time,
        }

        for key, value in kwargs.items():
            params_val.update({key: value})

        update_marker_request = {
            'jsonrpc': '2.0',
            'id': UPDATE_MARKER_REQUEST_ID,
            'method': 'updateMarker',
            'params': params_val,
        }
        if self.debug:
            print(
                'update marker request\n',
                json.dumps(update_marker_request, indent=4),
            )
        self.ws.send(json.dumps(update_marker_request))

    def get_mental_command_action_sensitivity(self, profile_name: str) -> None:
        print('get mental command sensitivity ------------------')
        sensitivity_request = {
            'id': SENSITIVITY_REQUEST_ID,
            'jsonrpc': '2.0',
            'method': 'mentalCommandActionSensitivity',
            'params': {
                'cortexToken': self.auth,
                'profile': profile_name,
                'status': 'get',
            },
        }
        if self.debug:
            print(
                'get mental command sensitivity \n',
                json.dumps(sensitivity_request, indent=4),
            )

        self.ws.send(json.dumps(sensitivity_request))

    def set_mental_command_action_sensitivity(
        self,
        profile_name: str,
        values: list[int],
    ) -> None:
        print('set mental command sensitivity ------------------')
        sensitivity_request = {
            'id': SENSITIVITY_REQUEST_ID,
            'jsonrpc': '2.0',
            'method': 'mentalCommandActionSensitivity',
            'params': {
                'cortexToken': self.auth,
                'profile': profile_name,
                'session': self.session_id,
                'status': 'set',
                'values': values,
            },
        }
        if self.debug:
            print(
                'set mental command sensitivity \n',
                json.dumps(sensitivity_request, indent=4),
            )

        self.ws.send(json.dumps(sensitivity_request))

    def get_mental_command_active_action(self, profile_name: str) -> None:
        print('get mental command active action ------------------')
        command_active_request = {
            'id': MENTAL_COMMAND_ACTIVE_ACTION_ID,
            'jsonrpc': '2.0',
            'method': 'mentalCommandActiveAction',
            'params': {
                'cortexToken': self.auth,
                'profile': profile_name,
                'status': 'get',
            },
        }
        if self.debug:
            print(
                'get mental command active action \n',
                json.dumps(command_active_request, indent=4),
            )

        self.ws.send(json.dumps(command_active_request))

    def set_mental_command_active_action(self, actions: list[str]) -> None:
        print('set mental command active action ------------------')
        command_active_request = {
            'id': SET_MENTAL_COMMAND_ACTIVE_ACTION_ID,
            'jsonrpc': '2.0',
            'method': 'mentalCommandActiveAction',
            'params': {
                'cortexToken': self.auth,
                'session': self.session_id,
                'status': 'set',
                'actions': actions,
            },
        }

        if self.debug:
            print(
                'set mental command active action \n',
                json.dumps(command_active_request, indent=4),
            )

        self.ws.send(json.dumps(command_active_request))

    def get_mental_command_brain_map(self, profile_name: str) -> None:
        print('get mental command brain map ------------------')
        brain_map_request = {
            'id': MENTAL_COMMAND_BRAIN_MAP_ID,
            'jsonrpc': '2.0',
            'method': 'mentalCommandBrainMap',
            'params': {
                'cortexToken': self.auth,
                'profile': profile_name,
                'session': self.session_id,
            },
        }
        if self.debug:
            print(
                'get mental command brain map \n',
                json.dumps(brain_map_request, indent=4),
            )
        self.ws.send(json.dumps(brain_map_request))

    def get_mental_command_training_threshold(self, profile_name: str) -> None:
        print('get mental command training threshold -------------')
        training_threshold_request = {
            'id': MENTAL_COMMAND_TRAINING_THRESHOLD,
            'jsonrpc': '2.0',
            'method': 'mentalCommandTrainingThreshold',
            'params': {
                'cortexToken': self.auth,
                'profile': profile_name,
                'session': self.session_id,
            },
        }
        if self.debug:
            print(
                'get mental command training threshold \n',
                json.dumps(training_threshold_request, indent=4),
            )
        self.ws.send(json.dumps(training_threshold_request))
