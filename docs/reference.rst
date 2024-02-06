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
   :undoc-members:
   :members:

.. autoclass:: Chat
   :undoc-members:
   :members:

.. autoclass:: Translate
   :undoc-members:
   :members:

.. autoclass:: TranslateText
   :undoc-members:
   :members:

.. autoclass:: Logprob
   :undoc-members:
   :members:

.. autoclass:: Tokenize
   :undoc-members:
   :members:

.. autoclass:: TextToImage
   :undoc-members:
   :members:

.. autoclass:: Transcript
   :undoc-members:
   :members:

.. autoclass:: TranscriptSegment
   :undoc-members:
   :members:

