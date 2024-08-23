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

from cortex.core.mental_command import (
    action_sensitivity,
    active_action,
    brain_map,
    training_threshold,
)
from cortex.consts import CA_CERTS
from cortex.logging import logger


class Cortex(Dispatcher):
    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        debug_mode: bool = False,
        session_id: str | None = None,
        headset_id: str | None = None,
        license: str | None = None,
    ) -> None:
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
        logger.info('Closing connection to Cortex.')

    def on_message(self, *args: Any, **kwargs: Any) -> None:
        logger.info('Received message: %s', args)

    def on_open(self, *args: Any, **kwargs: Any) -> None:
        logger.info('Connection opened.')

    def on_close(self, *args: Any, **kwargs: Any) -> None:
        logger.info(f'on_close: {args[1]}')

    def on_error(self, *args: Any, **kwargs: Any) -> None:
        if len(args) == 2:
            logger.error(f'on_error: {args[1]}')

    def get_mental_command_action_sensitive(self, profile_name: str) -> None:
        """Get the mental command action sensitivity."""
        logger.info('--- Getting mental command action sensitivity ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        sensitivity = action_sensitivity(
            auth=self._auth,
            profile_name=profile_name,
        )

        # If debug mode is enabled, print the sensitivity.
        logger.debug('Getting mental command action sensitivity.')
        logger.debug(sensitivity)

        self._ws.send(json.dumps(sensitivity, indent=4))

    def set_mental_command_action_sensitive(
        self,
        profile_name: str,
        values: list[int],
    ) -> None:
        """Set the mental command action sensitivity."""
        logger.info('--- Setting mental command action sensitivity ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        sensitivity = action_sensitivity(
            auth=self._auth,
            profile_name=profile_name,
            session_id=self.session_id,
            values=values,
        )

        # If debug mode is enabled, print the sensitivity.
        logger.debug('Setting mental command action sensitivity.')
        logger.debug(sensitivity)

        self._ws.send(json.dumps(sensitivity, indent=4))

    def get_mental_command_active_action(self, profile_name: str) -> None:
        """Get the active mental command action."""
        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        active = active_action(
            auth=self._auth,
            profile_name=profile_name,
        )

        # If debug mode is enabled, print the active action.
        logger.debug('Getting mental command active action.')
        logger.debug(active)

        self._ws.send(json.dumps(active, indent=4))

    def set_mental_command_active_action(
        self,
        actions: list[str],
    ) -> None:
        """Set the active mental command action."""
        logger.info('--- Setting mental command active action ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        active = active_action(
            auth=self._auth,
            session_id=self.session_id,
            actions=actions,
        )

        # If debug mode is enabled, print the active action.
        logger.debug('Setting mental command active action.')
        logger.debug(active)

        self._ws.send(json.dumps(active, indent=4))

    def get_mental_command_brain_map(self, profile_name: str) -> None:
        """Get the mental command brain map."""
        logger.info('--- Getting mental command brain map ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        brain = brain_map(
            auth=self._auth,
            session_id=self._session_id,
            profile_name=profile_name,
        )

        # If debug mode is enabled, print the brain map.
        logger.debug('Getting mental command brain map.')
        logger.debug(brain)

        self._ws.send(json.dumps(brain, indent=4))

    def get_mental_command_training_threshold(self, profile_name: str) -> None:
        """Get the mental command training threshold."""
        logger.info('--- Getting mental command training threshold ---')

        if not self._auth:
            raise ValueError('No authentication token. Please connect to Cortex first.')

        if not self.session_id:
            raise ValueError('No session ID. Please create a session first.')

        threshold = training_threshold(
            auth=self._auth,
            session_id=self.session_id,
            profile_name=profile_name,
        )

        # If debug mode is enabled, print the training threshold.
        logger.debug('Getting mental command training threshold.')
        logger.debug(threshold)

        self._ws.send(json.dumps(threshold, indent=4))

    @property
    def ws(self) -> websocket.WebSocketApp | None:
        """WebSocketApp: The WebSocketApp object."""
        return self._ws
