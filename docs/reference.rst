API Reference
=============

Clients
-------

.. py:module:: textsynth.client

.. autoclass:: TextSynth

.. automethod:: TextSynth.credits
.. automethod:: TextSynth.engines

Engines
-------

.. py:module:: textsynth.engine

.. autoclass:: Engine

Endpoints
---------

.. automethod:: textsynth.engine.Engine.completions
.. automethod:: textsynth.engine.Engine.chat
.. automethod:: textsynth.engine.Engine.translate
.. automethod:: textsynth.engine.Engine.logprob
.. automethod:: textsynth.engine.Engine.tokenize
.. automethod:: textsynth.engine.Engine.text_to_image
.. automethod:: textsynth.engine.Engine.transcript

Answers
-------

.. autoclass:: Completions
.. autoclass:: Chat
.. autoclass:: Translate
.. autoclass:: TranslateText
.. autoclass:: Logprob
.. autoclass:: Tokenize
.. autoclass:: TextToImage
.. autoclass:: Transcript
.. autoclass:: TranscriptSegment

