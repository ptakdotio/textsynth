import os

import requests

import textsynth.engine


class ClientError(Exception):
    pass


class Client:

    def __init__(self, server=None, secret_key=None):
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
        return self._handle_error_response(response.json())

    def _post(self, path, payload):
        response = self.session.post(f'https://{self.server}/v1/{path}', json=payload)
        return self._handle_error_response(response.json())

    def _post_files(self, path, files):
        response = self.session.post(f'https://{self.server}/v1/{path}', files=files)
        return self._handle_error_response(response.json())

    def _handle_error_response(self, decoded):
        if 'error' in decoded:
            raise ClientError(decoded['error'])
        return decoded

    def engines(self, engine_id):
        return textsynth.engine.Engine(self, engine_id)

    def credits(self):
        return self._get('credits')['credits']

