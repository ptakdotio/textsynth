# textsynth/client.py
#
# This file implements the Client class, which handles a (possibly
# authenticated) connection to a TextSynth server. By default, this will be the
# main server at <api.textsynth.com>, but you can specify a local instance.
#


import os

import requests


class Client:

    def __init__(self, server=None, secret_key=None):

        # If no server is provided, use the main TextSynth API

        if server is not None:
            self.server = server
        else:
            self.server = 'api.textsynth.com'

        # If no secret key is provided, check whether is was provided as an
        # environment variable. If not, it is assumed that we will only be
        # connecting to a local, non-authenticated server.

        if secret_key is not None:
            self.secret_key = secret_key
        elif 'TEXTSYNTH_SECRET_KEY' in os.environ:
            self.secret_key = os.environ['TEXTSYNTH_SECRET_KEY']
        else:
            self.secret_key = None

        # Set up a `requests` session with which to make HTTP requests. If we
        # are using a secret key, add it as a header here.

        self.session = requests.Session()
        if self.secret_key is not None:
            self.session.headers.update({'Authorization': f'Bearer {self.secret_key}'})

    # Private convenience function, for use by engines. Handles common tasks
    # associated with GET requests.

    def _get(self, path):
        response = self.session.get(f'https://{self.server}/v1/{path}')
        return response.json()

    # Private convenience function, for use by engines. Handles common tasks
    # associated with POST requests.

    def _post(self, path, payload):
        response = self.session.get(f'https://{self.server}/v1/{path}', json=payload)
        return response.json()

    # Wraps `/v1/credits`

    def credits(self):
        return self._get('credits')['credits']

