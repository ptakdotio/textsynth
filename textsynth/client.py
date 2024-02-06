import json
import os

import requests

import textsynth.engine


class TextSynthError(Exception):
    pass


class TextSynth:
    """
    This class represents a connection to a TextSynth server. It handles
    authentication and provides access to the server's REST API.
    """

    def __init__(self, server: str = None, secret_key: str = None):
        """
        Create a client object that will make authenticated requests to a
        server.

        If no server is provided, api.textsynth.com will be used by default.

        The API key can also be provided in the environment variable
        ``TEXTSYNTH_SECRET_KEY``. If no API key provided, the requests will
        not be authenticated.

        .. note::
            The default server will always reject unauthenticated requests, so
            it only makes sense to do this with local servers.

        :param server: Address of the TextSynth server
        :param secret_key: Your TextSynth API key
        """
        if server is not None:
            self.server = server
        else:
            self.server = 'api.textsynth.com'

        if secret_key is not None:
            self.secret_key = secret_key
        elif 'TEXTSYNTH_SECRET_KEY' in os.environ:
            self.secret_key = os.environ['TEXTSYNTH_SECRET_KEY']
        else:
            self.secret_key = None

        self.session = requests.Session()
        if self.secret_key is not None:
            self.session.headers.update({'Authorization': f'Bearer {self.secret_key}'})

    def _get(self, path):
        response = self.session.get(f'https://{self.server}/v1/{path}')
        return self._catch_error(response.json())

    def _post(self, path, payload):
        response = self.session.post(f'https://{self.server}/v1/{path}', json=payload)
        return self._catch_error(response.json())

    def _post_streaming(self, path, payload):
        response = self.session.post(f'https://{self.server}/v1/{path}', json=payload, stream=True)
        iterator = response.iter_lines()
        yield self._catch_error(json.loads(next(iterator)))
        for line in iterator:
            if line == b'':
                continue
            yield json.loads(line)

    def _post_files(self, path, files):
        response = self.session.post(f'https://{self.server}/v1/{path}', files=files)
        return self._catch_error(response.json())

    def _catch_error(self, decoded):
        if 'error' in decoded:
            raise TextSynthError(decoded['error'])
        return decoded

    def engines(self, engine_id: str) -> textsynth.engine.Engine:
        """
        Prepare an ``Engine`` which can be used to make requests through the
        current client. This is the preferred way of creating an ``Engine``
        object.

        :param engine_id: The engine id with which to make requests
        """
        return textsynth.engine.Engine(self, engine_id)

    def credits(self) -> int:
        """
        Get the number of remaining credits on your account.
        """
        return self._catch_error(self._get('credits'))['credits']

