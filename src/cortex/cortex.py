"""Cortex API.

This module provides a Python interface to the Emotiv Cortex API.

"""

# pylint: disable=unused-argument
import datetime
import json
import logging
import os
import ssl
import threading
from collections.abc import Mapping
from datetime import datetime as dt
from pathlib import Path
from typing import Any

import websocket
from pydispatch import Dispatcher

from cortex.api.auth import access, authorize, get_info
from cortex.api.handler import stream_data
from cortex.api.headset import make_connection, query_headset, subscription
from cortex.api.session import create_session, update_session
from cortex.consts import CA_CERTS, WarningCode
from cortex.logging import logger


class InheritEventsMeta(type):
    """Metaclass to inherit events from base classes."""

    # pylint: disable=bad-mcs-classmethod-argument
    def __new__(cls, name: str, bases: tuple[Any], class_dict: dict[str, Any]) -> 'InheritEventsMeta':
        """Create a new class."""
        # Combine events from all base classes
        events: list[str] = []
        for base in bases:
            if hasattr(base, '_events_'):
                events.extend(base._events_)
        # Add current class events
        if '_events_' in class_dict:
            events.extend(class_dict['_events_'])
        class_dict['_events_'] = events
        return type.__new__(cls, name, bases, class_dict)


class Cortex(Dispatcher, metaclass=InheritEventsMeta):
    """The Cortex class.

    This class provides a Python interface to the Emotiv Cortex API.

    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        *,
        debug_mode: bool = False,
        session_id: str | None = None,
        headset_id: str | None = None,
        profile_name: str | None = None,
        debit: int | None = None,
        license: str | None = None,  # pylint: disable=redefined-builtin
    ) -> None:
        """Initialize Cortex.

        Args:
            client_id (str): The client ID of your Cortex application.
            client_secret (str): The client secret of your Cortex application.

        Keyword Args:
            debug_mode (bool, optional): Whether to enable debug mode.
            session_id(str, optional): The session id.
            headset_id(str, optional): The headset id.
            profile_name(str, optional): The profile name.
            license (str, optional): A licnese id. In most cases, you don't need to
                specify the license id. Cortex will find the appropriate
                license based on the client id.
                Default is None.
            debit (int, optional): The number of sessions to debit from the license,
                so that it can be spent locally without having to authorize again.
                You need to debit the license only if you want to *activate a session*.
                The default is 0.

        """
        super().__init__()
        self.client_id = os.environ.get('CLIENT_ID', client_id)
        self.client_secret = os.environ.get('CLIENT_SECRET', client_secret)

        if not self.client_id:
            raise ValueError('No CLIENT_ID. Add it to the environment or pass it as an argument.')
        if not self.client_secret:
            raise ValueError('No CLIENT_SECRET. Add it to the environment or pass it as an argument.')

        if debug_mode:
            logger.setLevel(logging.DEBUG)

        self.debug = debug_mode
        self.session_id = session_id
        self.headset_id = headset_id
        self.profile_name: str | None = profile_name
        self.debit = debit
        self.license = license

        self._ws: websocket.WebSocketApp | None = None
        self._thread: threading.Thread | None = None
        self._auth: str | None = None

    def open(self) -> None:
        """Open a connection to Cortex."""
        logger.info('Opening connection to Cortex.')
        url: str = 'wss://localhost:6868'
        self._ws = websocket.WebSocketApp(
            url, on_open=self.on_open, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close
        )
        thread_name = f'WebSocketThread-{dt.now(datetime.UTC):%Y%m%d%H%M%S}'

        sslopt: dict[str, Path | ssl.VerifyMode] = {}
        if CA_CERTS.exists():
            sslopt = {'ca_certs': CA_CERTS, 'cert_reqs': ssl.CERT_REQUIRED}
        else:
            logger.warning('No certificate found. Please check the certificates folder.')
            sslopt = {'cert_reqs': ssl.CERT_NONE}

        self._thread = threading.Thread(target=self._ws.run_forever, name=thread_name, args=(None, sslopt))
        self._thread.start()
        self._thread.join()

    def close(self) -> None:
        """Close the connection to Cortex."""
        self.ws.close()
        logger.info('Closed connection to Cortex.')

    def on_message(self, *args: Any, **kwargs: Any) -> None:
        """Handle the message."""
        logger.info('Received message: %s', args)

    def on_open(self, *args: Any, **kwargs: Any) -> None:
        """Handle the open event."""
        logger.info('Websocket opened.')

    def on_close(self, *args: Any, **kwargs: Any) -> None:
        """Handle the close event."""
        logger.info(f'on_close: {args[1]}')

    def on_error(self, *args: Any, **kwargs: Any) -> None:
        """Handle the error."""
        if len(args) == 2:
            logger.error(f'on_error: {args[1]}')

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
        if data.get('com') is not None:
            self.emit('new_com_data', stream_data(data, 'com'))
        elif data.get('fac') is not None:
            self.emit('new_fe_data', stream_data(data, 'fac'))
        elif data.get('eeg') is not None:
            self.emit('new_eeg_data', stream_data(data, 'eeg'))
        elif data.get('mot') is not None:
            self.emit('new_mot_data', stream_data(data, 'mot'))
        elif data.get('dev') is not None:
            self.emit('new_dev_data', stream_data(data, 'dev'))
        elif data.get('met') is not None:
            self.emit('new_met_data', stream_data(data, 'met'))
        elif data.get('pow') is not None:
            self.emit('new_pow_data', stream_data(data, 'pow'))
        elif data.get('sys') is not None:
            self.emit('new_sys_data', stream_data(data, 'sys'))
        else:
            logger.warning('Unknown data: {data}')

    def request_access(self) -> None:
        """Request user approval for the current application through [EMOTIV Launcher].

        Notes:
            When your application calls this method for the first time,
            [EMOTIV Launcher] displays a message to approve your application.

        [Emotiv Launcher]: https://emotiv.gitbook.io/emotiv-launcher/

        Read More:
            [requestAccess](https://emotiv.gitbook.io/cortex-api/authentication/requestaccess)

        """
        logger.info('--- Requesting access ---')

        _access = access(client_id=self.client_id, client_secret=self.client_secret, method='requestAccess')

        logger.debug(_access)

        self.ws.send(json.dumps(_access, indent=4))

    def has_access_right(self) -> None:
        """Request user approval for the current application through [EMOTIV Launcher].

        Notes:
            When your application calls this method for the first time,
            [EMOTIV Launcher] displays a message to approve your application.

        [Emotiv Launcher]: https://emotiv.gitbook.io/emotiv-launcher/

        Read More:
            [requestAccess](https://emotiv.gitbook.io/cortex-api/authentication/requestaccess)

        """
        logger.info('--- Requesting access right ---')

        _access = access(client_id=self.client_id, client_secret=self.client_secret, method='hasAccessRight')

        logger.debug(_access)

        self.ws.send(json.dumps(_access, indent=4))

    def authorize(self) -> None:
        """This method is to generate a Cortex access token.

        Notes:
            Most of the methods of the Cortex API require this token as a
            parameter. Application can specify the license key and the amount
            of sessions to be debited from the license and use them locally.

        Read More:
            [authorize](https://emotiv.gitbook.io/cortex-api/authentication/authorize)

        """
        logger.info('--- Authorizing application ---')

        _authorize = authorize(
            client_id=self.client_id, client_secret=self.client_secret, license=self.license, debit=self.debit
        )

        logger.debug(_authorize)

        self.ws.send(json.dumps(_authorize, indent=4))

    def create_session(self) -> None:
        """Open a session with an Emotiv headset.

        Notes:
            To open a session with a headset, the status of the headset must be
            "connected". If the status is "discovered", then you must call
            `controlDevice` to connect the headset.
            You cannot open a session with a headset connected by a USB cable.
            You can use `queryHeadsets` to check the status and connection type
            of the headset.

        Read More:
            [createSession](https://emotiv.gitbook.io/cortex-api/session/createsession)

        """
        logger.info('--- Creating session ---')

        if self.session_id is not None:
            logger.warning(f'Session already exists. {self.session_id}')
            return

        _session = create_session(auth=self.auth, headset_id=self.headset_id, status='active')

        logger.debug(_session)

        self.ws.send(json.dumps(_session, indent=4))

    def close_session(self) -> None:
        """Close a session with an Emotiv headset.

        Read More:
            [updateSession](https://emotiv.gitbook.io/cortex-api/session/updateSession)

        """
        logger.info('--- Closing session ---')
        _session = update_session(auth=self.auth, session_id=self.session_id, status='close')

        logger.debug(_session)

        self.ws.send(json.dumps(_session, indent=4))

    def get_cortex_info(self) -> None:
        """Return info about the Cortex service, like it's version and build number.

        Read More:
            [getCortexInfo](https://emotiv.gitbook.io/cortex-api/authentication/getcortexinfo)

        """
        logger.info('--- Getting Cortex info ---')

        _info = get_info()

        logger.debug(_info)

        self.ws.send(json.dumps(_info, indent=4))

    def connect(self, mappings: dict[str, str] | None = None, connection_type: str | None = None) -> None:
        """Connect to the headset.

        Args:
            mappings (Mapping[str, str], optional): The mappings.
            connection_type (str, optional): The connection type.

        """
        logger.info('--- Connecting to the headset ---')

        _connection = make_connection(
            command='connect', headset_id=self.headset_id, mappings=mappings, connection_type=connection_type
        )

        logger.debug(_connection)

        self.ws.send(json.dumps(_connection, indent=4))

    def disconnect(self, mappings: Mapping[str, str] | None = None, connection_type: str | None = None) -> None:
        """Disconnect from the headset.

        Args:
            mappings (Mapping[str, str], optional): The mappings.
            connection_type (str, optional): The connection type.

        """
        logger.info('--- Disconnecting from the headset ---')

        _connection = make_connection(
            command='disconnect', headset_id=self.headset_id, mappings=mappings, connection_type=connection_type
        )

        logger.debug(_connection)

        self.ws.send(json.dumps(_connection, indent=4))

    def query_headset(self) -> None:
        """Query the headset."""
        logger.info('--- Querying the headset ---')

        _query = query_headset(headset_id=self.headset_id)

        logger.debug(_query)

        self.ws.send(json.dumps(_query, indent=4))

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

        _request = subscription(auth=self.auth, session_id=self.session_id, streams=streams, method='subscribe')

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

        _request = subscription(auth=self.auth, session_id=self.session_id, streams=streams, method='unsubscribe')

        logger.debug(_request)

        self.ws.send(json.dumps(_request, indent=4))

    def set_headset(self, headset_id: str) -> None:
        """Set the headset ID.

        Args:
            headset_id (str): The headset ID.

        """
        self.headset_id = headset_id

    def set_profile(self, profile_name: str) -> None:
        """Set the profile name.

        Args:
            profile_name (str): The profile name.

        """
        self.profile_name = profile_name

    @property
    def ws(self) -> websocket.WebSocketApp:
        """WebSocketApp: The WebSocketApp object."""
        if self._ws is None:
            raise ValueError('Cortex is not initialized. Call `open()` to initialize it.')
        return self._ws

    @property
    def auth(self) -> str:
        """str: The authorization token."""
        if self._auth is None:
            raise ValueError('No authorization token. Call `authorize()` to generate it.')
        return self._auth
