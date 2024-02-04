# Textsynth Wrapper

_Easy-to-use Python wrapper for the TextSynth API_

## What is this?

This is a simple Python library that handles interactions with the
[TextSynth](https://textsynth.com/) API. It handles authentication, wraps
requests and responses, and validates the data you pass to TextSynth.

See the [TextSynth documentation](https://textsynth.com/documentation.html) for
an up-to-date reference on the underlying API and capabilities of TextSynth.

## How do I use it?

The simplest way to use this library is with the top-level exports. These are
intended to mimic the underlying API, and do not require you to specify
anything beyond what engine and endpoint you wish to use.

First, make sure you have your TextSynth API key ready. If you wish, you can
set the environment variable `TEXTSYNTH_SECRET_KEY` to your API key, and this
library will automatically pick it up and handle authentication for you.

```
$ export TEXTSYNTH_SECRET_KEY='<your secret key here>'
```

Then, you can request a text completion using the top-level function
`textsynth.engine()` to get a reference to your preferred engine, and
`.completions()` to request the completion.

```
>>> import textsynth
>>> textsynth.engine('gptj_6B').completions('Once upon a time')
Completions(text=' there was a company called Tinkoff. It didn’t do much that day.\n')
```

If you want to use a different TextSynth server instance, or you don't want to
put your API key in an environment variable, you can explicitly create a client
object.

```
>>> from textsynth import TextSynth
>>> ts = TextSynth('mytsserver.localdomain', secret_key='<your secret key here>')
>>> ts.engines('stable_diffusion').completions('You know what I say,')
...
```

