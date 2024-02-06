import base64
import io
import json

from typing import List, BinaryIO

import jsonschema



class Engine:
    """
    This class is an interface for making requests to a specific engine through
    the TextSynth API. Each request will be validated according to the JSON schema
    that the endpoint expects, and the response will be wrapped in an object that
    performs useful post-processing on the results, handling base64 decoding and
    similar tasks.

    It is generally preferred to create an engine using the method
    :py:meth:`textsynth.client.TextSynth.engines`.

    .. note::
        Not all engines support all endpoints. This library does not keep track
        of the available engines and endpoints they support, as they are liable
        to change at any time. If you request an unsupported endpoint, it will
        be rejected by the server with an appropriate error message.
    """

    def __init__(self, client: 'textsynth.client.TextSynth', engine_id: str):
        """
        Create an object that will make requests to an engine using a client.

        :param client: The client object through which to make requests
        :param engine_id: The id of the engine you want to use
        """

        self.client = client
        self.engine_id = engine_id

    def _post(self, path, payload):
        return self.client._post(f'engines/{self.engine_id}/{path}', payload)

    def _post_streaming(self, path, payload):
        return self.client._post_streaming(f'engines/{self.engine_id}/{path}', payload)

    def _post_files(self, path, files):
        return self.client._post_files(f'engines/{self.engine_id}/{path}', files)

    # Properties shared by `completions` and `chat` endpoints
    COMPLETIONS_CHAT_COMMON_PROPERTIES = {
        'max_tokens': {
            'type': 'integer',
            'minimum': 0
        },
        'stream': {
            'type': 'boolean'
        },
        'stop': {
            'oneOf': [
                {
                    'type': 'string'
                },
                {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                }
            ]
        },
        'n': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 16
        },
        'temperature': {
            'type': 'number'
        },
        'top_k': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 1000
        },
        'top_p': {
            'type': 'number',
            'minimum': 0,
            'maximum': 1
        },
        'seed': {
            'type': 'integer'
        },
        'logit_bias': {
            'type': 'object',
            'additionalProperties': False,
            'patternProperties': {
                '^.*$': {
                    'type': 'number'
                }
            }
        },
        'presence_penalty': {
            'type': 'number',
            'minimum': -2,
            'maximum': 2
        },
        'frequency_penalty': {
            'type': 'number',
            'minimum': -2,
            'maximum': 2
        },
        'repetition_penalty': {
            'type': 'number'
        },
        'typical_p': {
            'type': 'number',
            'minimum': 0,
            'maximum': 1
        }
        # TODO figure out how to validate these
        'grammar': {
            'type': 'string'
        },
        'schema': {
            'type': 'object'
        }
    }

    COMPLETIONS_SCHEMA = {
        'required': ['prompt'],
        'additionalProperties': False,
        'properties': {
            'prompt': {
                'type': 'string'
            },
            **COMPLETIONS_CHAT_COMMON_PROPERTIES
        }
    }

    def completions(self, prompt: str, **kwargs) -> 'Completions':
        """
        Request a text completion of the given ``prompt``.

        :param prompt: The text to be completed by the model
        :param kwargs: Keyword arguments accepted by this endpoint

        See https://textsynth.com/documentation.html#completions for
        detailed documentation on this endpoint.
        """

        payload = {'prompt': prompt, **kwargs}
        jsonschema.validate(payload, self.COMPLETIONS_SCHEMA)
        if payload.get('stream'):
            return map(Completions, self._post_streaming('completions', payload))
        else:
            return Completions(self._post('completions', payload))

    CHAT_SCHEMA = {
        'required': ['messages'],
        'additionalProperties': False,
        'properties': {
            'messages': {
                'type': 'array',
                'items': {
                    'type': 'string'
                }
            },
            'system': {
                'type': 'string'
            },
            **COMPLETIONS_CHAT_COMMON_PROPERTIES
        }
    }

    def chat(self, messages: List[str], **kwargs) -> 'Chat':
        """
        Request a text completion for the chat conversation given in ``messages``.

        :param messages: The messages in the chat conversation so far
        :param system: The system chat prompt
        :param kwargs: Keyword arguments accepted by this endpoint

        See https://textsynth.com/documentation.html#chat for detailed
        documentation on this endpoint.
        """

        payload = {'messages': messages, **kwargs}
        jsonschema.validate(payload, self.CHAT_SCHEMA)
        if payload.get('stream'):
            return map(Chat, self._post_streaming('chat', payload))
        else:
            return Chat(self._post('chat', payload))

    TRANSLATE_LANGUAGE_CODES = {
        'enum': [
            'ace', 'ada', 'adh', 'ady', 'af', 'agr', 'msm', 'ahk', 'sq', 'alz',
            'abt', 'am', 'grc', 'ar', 'hy', 'frp', 'as', 'av', 'kwi', 'awa',
            'quy', 'ay', 'az', 'ban', 'bm', 'bci', 'bas', 'ba', 'eu', 'akb',
            'btx', 'bts', 'bbc', 'be', 'bzj', 'bn', 'bew', 'bho', 'bim', 'bi',
            'brx', 'bqc', 'bus', 'bs', 'br', 'ape', 'bg', 'bum', 'my', 'bua',
            'qvc', 'jvn', 'rmc', 'ca', 'qxr', 'ceb', 'bik', 'maz', 'ch', 'cbk',
            'ce', 'chr', 'hne', 'ny', 'zh', 'ctu', 'cce', 'cac', 'chk', 'cv',
            'kw', 'co', 'crh', 'hr', 'cs', 'mps', 'da', 'dwr', 'dv', 'din',
            'tbz', 'dov', 'nl', 'dyu', 'dz', 'bgp', 'gui', 'bru', 'nhe', 'djk',
            'taj', 'enq', 'en', 'sja', 'myv', 'eo', 'et', 'ee', 'cfm', 'fo',
            'hif', 'fj', 'fil', 'fi', 'fip', 'fon', 'fr', 'ff', 'gag', 'gl',
            'gbm', 'cab', 'ka', 'de', 'gom', 'gof', 'gor', 'el', 'guh', 'gub',
            'gn', 'amu', 'ngu', 'gu', 'gvl', 'ht', 'cnh', 'ha', 'haw', 'he',
            'hil', 'mrj', 'hi', 'ho', 'hmn', 'qub', 'hus', 'hui', 'hu', 'iba',
            'ibb', 'is', 'ig', 'ilo', 'qvi', 'id', 'inb', 'iu', 'ga', 'iso',
            'it', 'ium', 'Iu', 'izz', 'jam', 'ja', 'jv', 'kbd', 'kbp', 'kac',
            'dtp', 'kl', 'xal', 'kn', 'cak', 'kaa', 'krc', 'ks', 'kk', 'meo',
            'kek', 'ify', 'kjh', 'kha', 'km', 'kjg', 'kmb', 'rw', 'ktu', 'tlh',
            'trp', 'kv', 'koi', 'kg', 'ko', 'kos', 'kri', 'ksd', 'kj', 'kum',
            'mkn', 'ku', 'ckb', 'ky', 'quc', 'lhu', 'quf', 'laj', 'lo', 'ltg',
            'la', 'lv', 'ln', 'lt', 'lu', 'lg', 'lb', 'ffm', 'mk', 'mad', 'mag',
            'mai', 'mak', 'mgh', 'mg', 'ms', 'ml', 'mt', 'mam', 'mqy', 'gv',
            'mi', 'arn', 'mrw', 'mr', 'mh', 'mas', 'msb', 'mbt', 'chm', 'mni',
            'min', 'lus', 'mdf', 'mn', 'mfe', 'meu', 'tuc', 'miq', 'emp', 'lrc',
            'qvz', 'se', 'nnb', 'niq', 'nv', 'ne', 'new', 'nij', 'gym', 'nia',
            'nog', 'no', 'nut', 'nyu', 'nzi', 'ann', 'oc', 'or', 'oj', 'ang',
            'om', 'os', 'pck', 'pau', 'pag', 'pa', 'pap', 'ps', 'fa', 'pis',
            'pon', 'pl', 'jac', 'pt', 'qu', 'otq', 'raj', 'rki', 'rwo', 'rom',
            'ro', 'rm', 'rn', 'ru', 'rcf', 'alt', 'quh', 'qup', 'msi', 'hvn',
            'sm', 'cuk', 'sxn', 'sg', 'sa', 'skr', 'srm', 'stq', 'gd', 'seh',
            'nso', 'sr', 'crs', 'st', 'shn', 'shp', 'sn', 'jiv', 'smt', 'sd',
            'si', 'sk', 'sl', 'so', 'nr', 'es', 'srn', 'acf', 'St', 'su', 'suz',
            'spp', 'sus', 'sw', 'ss', 'sv', 'gsw', 'syr', 'ksw', 'tab', 'tg',
            'tks', 'ber', 'ta', 'tdx', 'tt', 'tsg', 'te', 'twu', 'teo', 'tll',
            'tet', 'th', 'bo', 'tca', 'ti', 'tiv', 'toj', 'to', 'sda', 'ts',
            'tsc', 'tn', 'tcy', 'tr', 'tk', 'tvl', 'tyv', 'ak', 'tzh', 'tzo',
            'tzj', 'tyz', 'udm', 'uk', 'ppk', 'ubu', 'ur', 'ug', 'uz', 've',
            'vec', 'vi', 'knj', 'wa', 'war', 'guc', 'cy', 'fy', 'wal', 'wo',
            'noa', 'xh', 'sah', 'yap', 'yi', 'yo', 'yua', 'zne', 'zap', 'dje',
            'zza', 'zu'
        ]
    }

    TRANSLATE_SCHEMA = {
        'required': ['text', 'source_lang', 'target_lang'],
        'additionalProperties': False,
        'properties': {
            'texts': {
                'type': 'array',
                'items': {
                    'type': 'string'
                }
            },
            'source_lang': TRANSLATE_LANGUAGE_CODES,
            'target_lang': TRANSLATE_LANGUAGE_CODES,
            'num_beams': {
                'type': 'integer',
                'minimum': 1,
                'maximum': 5
            },
            'split_sentences': {
                'type': 'boolean'
            }
        }
    }
 
    def translate(self, texts: List[str], **kwargs) -> 'Translate':
        """
        Translate one or more texts into a target language.

        :param texts: List of texts to be translated
        :param kwargs: Keyword arguments accepted by this endpoint

        See https://textsynth.com/documentation.html#translations for
        detailed documentation on this endpoint.
        """

        payload = {'texts': texts, **kwargs}
        jsonschema.validate(payload, self.TRANSLATE_SCHEMA)
        return Translate(self._post('translate', payload))

    LOGPROB_SCHEMA = {
        'required': ['context', 'continuation'],
        'additionalProperties': False,
        'properties': {
            'context': {
                'type': 'string'
            },
            'continuation': {
                'type': 'string',
                'minLength': 1
            }
        }
    }

    def logprob(self, context: str, continuation: str) -> 'Logprob':
        """
        Estimate the probability that ``continuation`` will be generated after
        ``context``.

        :param context: Context for evaluating a completion
        :param continuation: The completion being evaluated

        See https://textsynth.com/documentation.html#logprob for
        detailed documentation on this endpoint.
        """
        payload = {'context': context, 'continuation': continuation}
        jsonschema.validate(payload, self.LOGPROB_SCHEMA)
        return Chat(self._post('logprob', payload))

    TOKENIZE_SCHEMA = {
        'required': ['text'],
        'additionalProperties': False,
        'properties': {
            'text': {
                'type': 'string'
            },
            'token_content_type': {
                'type': 'string',
                'enum': ['none', 'base64']
            }
        }
    }

    def tokenize(self, text: str, **kwargs) -> 'Tokenize':
        """
        Get the tokens corresponding to a given text.

        :param text: Text to convert into tokens
        :param kwargs: Keyword arguments accepted by this endpoint

        See https://textsynth.com/documentation.html#tokenize for
        detailed documentation on this endpoint.
        """
        payload = {'text': text, **kwargs}
        jsonschema.validate(payload, self.TOKENIZE_SCHEMA)
        return TokenizeAnswer(**self._post('tokenize', payload))

    TEXT_TO_IMAGE_SCHEMA = {
        'required': ['prompt'],
        'additionalProperties': False,
        'properties': {
            'prompt': {
                'type': 'string'
            },
            'image_count': {
                'type': 'integer',
                'minimum': 1,
                'maximum': 4
            },
            'width': {
                'enum': [384, 512, 640, 768]
            },
            'height': {
                'enum': [384, 512, 640, 768]
            },
            'timesteps': {
                'type': 'integer',
                'minimum': 1
            },
            'guidance_scale': {
                'type': 'number',
                'minimum': 0
            },
            'seed': {
                'type': 'integer'
            },
            'negative_prompt': {
                'type': 'string'
            },
            'image': {
                'type': 'string'
            },
            'strength': {
                'type': 'number',
                'minimum': 0,
                'maximum': 1
            }
        }
    }

    def text_to_image(self, prompt: str, **kwargs) -> 'TextToImage':
        """
        Generate one or more images from a text description.

        :param prompt: Text description for image generation
        :param kwargs: Keyword arguments accepted by this endpoint

        See https://textsynth.com/documentation.html#text_to_image for
        detailed documentation on this endpoint.
        """

        payload = {'prompt': prompt, **kwargs}
        jsonschema.validate(payload, self.TEXT_TO_IMAGE_SCHEMA)
        return TextToImage(self._post('text_to_image', payload))

    TRANSCRIPT_LANGUAGE_CODES = [
        'af', 'am', 'ar', 'as', 'az', 'ba', 'be', 'bg', 'bn', 'bo', 'br',
        'bs', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'eu',
        'fa', 'fi', 'fo', 'fr', 'gl', 'gu', 'ha', 'haw', 'he', 'hi', 'hr',
        'ht', 'hu', 'hy', 'id', 'is', 'it', 'ja', 'jw', 'ka', 'kk', 'km',
        'kn', 'ko', 'la', 'lb', 'ln', 'lo', 'lt', 'lv', 'mg', 'mi', 'mk',
        'ml', 'mn', 'mr', 'ms', 'mt', 'my', 'ne', 'nl', 'nn', 'no', 'oc',
        'pa', 'pl', 'ps', 'pt', 'ro', 'ru', 'sa', 'sd', 'si', 'sk', 'sl',
        'sn', 'so', 'sq', 'sr', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th',
        'tk', 'tl', 'tr', 'tt', 'uk', 'ur', 'uz', 'vi', 'yi', 'yo', 'yue',
        'zh'
    ]

    TRANSCRIPT_SCHEMA = {
        'required': ['language'],
        'additionalProperties': False,
        'properties': {
            'language': {
                'enum': TRANSCRIPT_LANGUAGE_CODES
            }
        }
    }

    def transcript(self, audio_file: BinaryIO, **kwargs) -> 'Transcript':
        """
        Transcribe an audio file into a text with timestamps. The parameter
        ``audio_file`` must be a file-like object containing an audio track in
        either MP3, M4A, MP4, WAV, or Opus format.

        :param audio_file: A file-like object containing audio to transcribe
        :param kwargs: Keyword arguments accepted by this endpoint

        See https://textsynth.com/documentation.html#transcript for
        detailed documentation on this endpoint.
        """

        payload = {**kwargs}
        jsonschema.validate(payload, self.TRANSCRIPT_SCHEMA)
        payload_file = io.StringIO(json.dumps(payload))
        return Transcript(self._post_files('transcript', {'json': payload_file, 'file': audio_file}))


class Answer:
    """
    This is the base class for all answer-wrapping objects.

    This class will keep the original JSON response, independent of any
    post-processing, in case the API response changes or the user needs the
    exact response from the server.
    """

    def __init__(self, raw_json: dict):
        self._raw_json = raw_json

    def raw_json(self) -> dict:
        """
        Return the original JSON from which this object was constructed.
        """
        return self._raw_json


class Completions(Answer):
    """
    Wrap a response from the ``completions`` endpoint.
    """

    text: str
    """Text completion"""

    reached_end: bool
    """Whether this is the last streamed response"""

    truncated_prompt: bool
    """Whether the prompt was cut off by the context length"""

    finish_reason: str
    """String describing why the completion ended"""

    input_tokens: int
    """Number of tokens in prompt"""

    output_tokens: int
    """Number of tokens in response"""

    def __init__(self, raw_json):
        super().__init__(raw_json)

        self.text             = raw_json.get('text')
        self.reached_end      = raw_json.get('reached_end')
        self.truncated_prompt = raw_json.get('truncated_prompt')
        self.finish_reason    = raw_json.get('finish_reason')
        self.input_tokens     = raw_json.get('text')
        self.output_tokens    = raw_json.get('text')

    def __repr__(self):
        return f'Completions(text={repr(self.text)})'


class Chat(Answer):
    """
    Wrap a response from the ``chat`` endpoint.

    .. note::
        This is the same as the :py:class:`completions` response; however, the
        reponse schema may diverge in the future, so these classes are kept
        separate.
    """

    text: str
    """Text completion"""

    reached_end: bool
    """Whether this is the last streamed response"""

    truncated_prompt: bool
    """Whether the prompt was cut off by the context length"""

    finish_reason: str
    """String describing why the completion ended"""

    input_tokens: int
    """Number of tokens in prompt"""

    output_tokens: int
    """Number of tokens in response"""

    def __init__(self, raw_json):
        super().__init__(raw_json)

        self.text             = raw_json.get('text')
        self.reached_end      = raw_json.get('reached_end')
        self.truncated_prompt = raw_json.get('truncated_prompt')
        self.finish_reason    = raw_json.get('finish_reason')
        self.input_tokens     = raw_json.get('text')
        self.output_tokens    = raw_json.get('text')

    def __repr__(self):
        return f'Chat(text={repr(self.text)})'


class Translate(Answer):
    """
    Wrap a response from the ``translate`` endpoint. Typically, multiple
    translations will be generated, each of which will be wrapped in a
    ``TranslateText`` object.
    """

    translations: 'TranslatedText'
    """List of translated texts"""

    input_tokens: int
    """Number of tokens in prompt"""

    output_tokens: int
    """Number of tokens in response"""

    def __init__(self, raw_json):
        super().__init__(raw_json)

        self.translations = []
        for translation in raw_json['translation']:
            self.translations = TranslatedText(translation)

        self.input_tokens  = raw_json.get('input_tokens')
        self.output_tokens = raw_json.get('output_tokens')

    def __repr__(self):
        return f'Translate(translations={repr(self.translations)})'


class TranslateText(Answer):
    """
    Wrap a single translation from the ``translate`` endpoint.
    """

    text: str
    """Text translated into target language"""

    detected_source_lang: str
    """What source language was detected, if applicable"""

    def __init__(self, raw_json):
        super().__init__(raw_json)

        self.text                 = raw_json.get('text')
        self.detected_source_lang = raw_json.get('detected_source_lang')

    def __repr__(self):
        return f'TranslateText(text={repr(self.text)})'


class Logprob(Answer):
    """
    Wrap a response from the ``logprob`` endpoint.
    """

    logprob: float
    """Logarithm of the probability of this completion"""

    num_tokens: int
    """Number of tokens in completion"""

    is_greedy: bool
    """True if this completion could be reached by greedy sampling"""

    input_tokens: int
    """Total number of input tokens (context + continuation)"""

    def __init__(self, raw_json):
        super().__init__(raw_json)

        self.logprob      = raw_json.get('logprob')
        self.num_tokens   = raw_json.get('num_tokens')
        self.is_greedy    = raw_json.get('is_greedy')
        self.input_tokens = raw_json.get('input_tokens')

    def __repr__(self):
        return f'Logprob(logprob={self.logprob})'


class Tokenize(Answer):
    """
    Wrap a response from the ``tokenize`` endpoint.

    If provided, the base64-encoded token contents will be decoded. As the
    TextSynth documentation notes, some tokens to not correspond to a complete
    and valid UTF-8 sequence, so they are decoded into :py:func:`bytes` rather
    than :py:func:`str`.
    """

    tokens: List[int]
    """List of tokens corresponding to input text"""

    token_content: List[bytes]
    """Byte content of tokens"""

    def __init__(self, raw_json):
        super().__init__(raw_json)

        self.tokens = raw_json.get('tokens')

        if 'token_content' in raw_json:
            token_content = []
            for token in kwargs['token_content']:
                token_content.push(base64.decodebytes(token))
            self.token_content = token_content
        else:
            self.token_content = None

    def __repr__(self, answer):
        return f'Tokenize(tokens={self.tokens}s)'


class TextToImage(Answer):
    """
    Wrap a response from the ``text_to_image`` endpoint.

    Each base64-encoded image will be decoded into a ``bytes`` object. This
    can be saved directly to a ``.jpg`` file.
    """

    images: List[bytes]
    """List of decoded images"""

    def __init__(self, raw_json):
        super().__init__(raw_json)

        images = []
        for image in kwargs[images]:
            images.append(base64.decodebytes(image['data']))
        self.images = images

    def __repr__(self):
        return f'TextToImage(len(images)={len(images)})'


class Transcript(Answer):
    """
    Wrap a response from the ``transcript endpoint``. Each timestamped segment
    will be wrapped in a ``TranscriptSegment`` object.
    """

    text: str
    """Transcribed text"""

    language: str
    """Language of the transcribed text"""

    duration: int
    """Length of transcribed audio"""

    segments: List['TranscriptSegment']
    """List of segments"""

    def __init__(self, raw_json):
        super().__init__(raw_json)

        self.text     = raw_json.get('text')
        self.language = raw_json.get('language')
        self.duration = raw_json.get('duration')

        if 'segments' in raw_json:
            segments = []
            for segment in raw_json['segments']:
                segments.append(TranscriptSegment(segment))
            self.segments = segments
        else:
            self.segments = None

    def __repr__(self):
        return f'Transcript(text={repr(self.text)})'


class TranscriptSegment(Answer):
    """
    Wrap a timestamped segment from the ``transcript`` endpoint.
    """

    text: str
    """Text in this segment"""

    id: int
    """Segment id"""

    start: int
    """Starting timestamp"""

    end: int
    """Ending timestamp"""

    def __init__(self, raw_json):
        super().__init__(raw_json)

        self.text  = raw_json.get('text')
        self.id    = raw_json.get('id')
        self.start = raw_json.get('start')
        self.end   = raw_json.get('end')

    def __repr__(self):
        return f'TranscriptSegment(text={repr(self.text)})'

