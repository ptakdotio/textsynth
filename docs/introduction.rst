Getting Started
===============

Installation
------------

This library is hosted on PyPI, so you can install it with

.. code-block:: sh

    pip install textsynth


Basic Usage
-----------

The simplest way to use this library is with the top-level exports. These are
intended to mimic the underlying API, and do not require you to create a client
object or specify anything beyond what engine and endpoint you wish to use.

First, make sure you have your TextSynth API key ready. If you wish, you can
set the environment variable ``TEXTSYNTH_SECRET_KEY`` to your API key, and this
library will automatically pick it up and handle authentication for you.

.. code-block:: sh

    export TEXTSYNTH_SECRET_KEY='<your secret key here>'


Then, you can request a text completion using the top-level function
``engine()`` to get a reference to your preferred engine, and ``completions()``
to request the completion.

.. code-block:: python

    >>> import textsynth
    >>> textsynth.engine('gptj_6B').completions('Once upon a time')
    Completions(text=' there was a company called Tinkoff. It didn’t do much that day.\n')


If you want to use a different TextSynth server instance, or you don't want to
put your API key in an environment variable, you can explicitly create a client
object.

.. code-block:: python

    >>> from textsynth import TextSynth
    >>> ts = TextSynth('myserver.localdomain', secret_key='<your secret key here>')
    >>> ts.engines('mistral_7B_instruct').completions('You know what I say,')
    Completions(text=' 90% of people in this world want happiness, and that’s kind of funny.')

