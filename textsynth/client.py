import json
import os

import requests

import textsynth.engine


class TextSynthError(Exception):
    pass


class TextSynth:

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
        return textsynth.engine.Engine(self, engine_id)

    def credits(self):
        return self._get('credits')['credits']

