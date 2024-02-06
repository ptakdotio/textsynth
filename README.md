# TextSynth Python Interface

_Easy-to-use Python wrapper for the TextSynth API_

## What is this?

This is a simple Python library that handles interactions with the
[TextSynth](https://textsynth.com/) API. It handles authentication, wraps
requests and responses, and validates the data you pass to TextSynth.

See the [TextSynth documentation](https://textsynth.com/documentation.html) for
an up-to-date reference on the underlying API and capabilities of TextSynth.

## How do I use it?

To install and get your API key set up:

```sh
pip install textsynth
export TEXTSYNTH_SECRET_KEY='<your secret key here>'
```

Then, in a Python session:

```python
>>> import textsynth
>>> textsynth.engine('gptj_6B').completions('Once upon a time')
Completions(text=' there was a company called Tinkoff. It didn’t do much that day.\n')
```

For more information about how to use this library, check out
[the documentation](https://textsynth-python.readthedocs.io/en/latest/).

## Is this library production-ready?

Not yet! I have yet to create a comprehensive test suite, so far I have only
been manually testing everything on my own credits. I plan to add automated
tests that work with the free version of
[`ts_server`](https://bellard.org/ts_server/), so that anyone can run them
locally without incurring charges.

Once I have comprehensive unit and integration tests, and I have used this
library in a major application myself, then I will release version 1.0 and
declare it production-ready.

If you notice any bugs or other problems, please report them at
<https://github.com/ptakdotio/textsynth/issues>.

