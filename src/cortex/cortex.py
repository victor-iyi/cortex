import datetime
import json
import logging
import os
import ssl
import threading

from datetime import datetime as dt
from pathlib import Path
from typing import Any

import websocket
from pydispatch import Dispatcher
from cortex.consts import CA_CERTS
from cortex.core.auth import access, authorize, get_info, session
from cortex.core.handler import stream_data
from cortex.logging import logger


class Cortex(Dispatcher):
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
        license: str | None = None,
    ) -> None:
        """

        Args:
            client_id (str): The client ID of your Cortex application.
            client_secret (str): The client secret of your Cortex application.
            session_id(str, optional):
            headset_id(str, optional):
            profile_name(str, optional):
            license (str, optional): A licnese id. In most cases, you don't need to
                specify the license id. Cortex will find the appropriate
                license based on the client id.
                Default is None.
            debit (int, optional): The number of sessions to debit from the license,
                so that it can be spent locally without having to authorize again.
                You need to debit the license only if you want to *activate a session*.
                The default is 0.
        """
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
            url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        thread_name = f'WebSocketThread-{dt.now(datetime.UTC):%Y%m%d%H%M%S}'

        sslopt: dict[str, Path | ssl.VerifyMode] = {}
        if CA_CERTS.exists():
            sslopt = {
                'ca_certs': CA_CERTS,
                'cert_reqs': ssl.CERT_REQUIRED,
            }
        else:
            logger.warning('No certificate found. Please check the certificates folder.')
            sslopt = {'cert_reqs': ssl.CERT_NONE}

        self._thread = threading.Thread(
            target=self._ws.run_forever,
            name=thread_name,
            args=(None, sslopt),
        )
        self._thread.start()
        self._thread.join()

    def close(self) -> None:
        self._ws.close()
        logger.info('Closed connection to Cortex.')

    def on_message(self, *args: Any, **kwargs: Any) -> None:
        logger.info('Received message: %s', args)

    def on_open(self, *args: Any, **kwargs: Any) -> None:
        logger.info('Websocket opened.')

    def on_close(self, *args: Any, **kwargs: Any) -> None:
        logger.info(f'on_close: {args[1]}')

    def on_error(self, *args: Any, **kwargs: Any) -> None:
        if len(args) == 2:
            logger.error(f'on_error: {args[1]}')

    def handle_stream_data(self, data: dict[str, Any]) -> None:
        """Handle the stream data."""
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
        """Request user approval for the current application through [EMOTIV
        Launcher].

        Notes:
            When your application calls this method for the first time,
            [EMOTIV Launcher] displays a message to approve your application.

        [Emotiv Launcher]: https://emotiv.gitbook.io/emotiv-launcher/

        Read More:
            [requestAccess](https://emotiv.gitbook.io/cortex-api/authentication/requestaccess)

        """
        logger.info('--- Requesting access ---')

        _access = access(
            client_id=self.client_id,
            client_secret=self.client_secret,
            method='requestAccess',
        )

        logging.debug(_access)

        self._ws.send(json.dumps(_access, indent=4))

    def has_access_right(self) -> None:
        """Request user approval for the current application through [EMOTIV
        Launcher].

        Notes:
            When your application calls this method for the first time,
            [EMOTIV Launcher] displays a message to approve your application.

        [Emotiv Launcher]: https://emotiv.gitbook.io/emotiv-launcher/

        Read More:
            [requestAccess](https://emotiv.gitbook.io/cortex-api/authentication/requestaccess)

        """
        logger.info('--- Requesting access right ---')

        _access = access(
            client_id=self.client_id,
            client_secret=self.client_secret,
            method='hasAccessRight',
        )

        logging.debug(_access)

        self._ws.send(json.dumps(_access, indent=4))

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
            client_id=self.client_id,
            client_secret=self.client_secret,
            license=self.license,
            debit=self.debit,
        )

        logging.debug(_authorize)

        self._ws.send(json.dumps(_authorize, indent=4))

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
            logging.warning(f'Session already exists. {self.session_id}')
            return

        _session = session(
            auth=self._auth,
            headset_id=self.headset_id,
            status='active',
        )

        logging.debug(_session)

        self._ws.send(json.dumps(_session, indent=4))

    def close_session(self) -> None:
        """Close a session with an Emotiv headset.

        Read More:
            [updateSession](https://emotiv.gitbook.io/cortex-api/session/updateSession)

        """

        logger.info('--- Closing session ---')
        _session = session(
            auth=self._auth,
            session_id=self.session_id,
            status='close',
        )

        logging.debug(_session)

        self._ws.send(json.dumps(_session, indent=4))

    def get_cortex_info(self) -> None:
        """Return info about the Cortex service, like it's version and build
        number.

        Read More:
            [getCortexInfo](https://emotiv.gitbook.io/cortex-api/authentication/getcortexinfo)

        """
        logger.info('--- Getting Cortex info ---')

        _info = get_info()

        logging.debug(_info)

        self._ws.send(json.dumps(_info, indent=4))

    @property
    def ws(self) -> websocket.WebSocketApp | None:
        """WebSocketApp: The WebSocketApp object."""
        return self._ws
