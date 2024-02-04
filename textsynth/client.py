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

    def __init__(self, server=None, secret_key=None):
        """
        Prepare a connection to a given server with a given API key. If no server is
        provided, <api.textsynth.com> will be used by default. The API key can also be
        provided in the environment variable `TEXTSYNTH_SECRET_KEY`.

        If no API key provided, the requests will not be authenticated. Note that the
        default server will always reject unauthenticated requests, so it only makes
        sense to do this with local servers.
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

    def engines(self, engine_id):
        """
        Prepare an `Engine` with the given `engine_id`, which can then be used
        to make requests. This is the preferred way of creating an `Engine`
        object.
        """
        return textsynth.engine.Engine(self, engine_id)

    def credits(self):
        """
        Get the number of remaining credits on your account.
        """
        return self._get('credits')['credits']

