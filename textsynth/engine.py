import base64
import io
import json

import jsonschema



class Engine:

    def __init__(self, client, engine_id):
        self.client = client
        self.engine_id = engine_id

    def _post(self, path, payload):
        return self.client._post(f'engines/{self.engine_id}/{path}', payload)

    def _post_files(self, path, files):
        return self.client._post_files(f'engines/{self.engine_id}/{path}', files)

    COMPLETIONS_SCHEMA = {
        'required': ['prompt'],
        'additionalProperties': False,
        'properties': {
            'prompt': {
                'type': 'string'
            },
            'max_tokens': {
                'type': 'integer',
                'minimum': 0
            },
            # NOTE Property 'stream' not implemented yet
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
            # NOTE Property 'grammar' not implemented yet
            # NOTE Property 'schema' not implemented yet
        }
    }

    def completions(self, prompt, **kwargs):
        payload = {'prompt': prompt, **kwargs}
        jsonschema.validate(payload, self.COMPLETIONS_SCHEMA)
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
            'max_tokens': {
                'type': 'integer',
                'minimum': 0
            },
            # NOTE Property 'stream' not implemented yet
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
            # NOTE Property 'grammar' not implemented yet
            # NOTE Property 'schema' not implemented yet
        }
    }

    def chat(self, messages, **kwargs):
        payload = {'messages': messages, **kwargs}
        jsonschema.validate(payload, self.CHAT_SCHEMA)
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
            'text': {
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
 
    def translate(self, texts, **kwargs):
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

    def logprob(self, context, continuation):
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

    def tokenize(self, text, **kwargs):
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

    def text_to_image(self, prompt, **kwargs):
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

    def transcript(self, audio_file, **kwargs):
        payload = {**kwargs}
        jsonschema.validate(payload, self.TRANSCRIPT_SCHEMA)
        payload_file = io.StringIO(json.dumps(payload))
        return Transcript(self._post_files('transcript', {'json': payload_file, 'file': audio_file}))


class Answer:

    def __init__(self, raw_json):
        self._raw_json = raw_json

    def raw_json(self):
        return self._raw_json


class Completions(Answer):

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

    def __init__(self, raw_json):
        super().__init__(raw_json)

        self.text                 = raw_json.get('text')
        self.detected_source_lang = raw_json.get('detected_source_lang')

    def __repr__(self):
        return f'TranslateText(text={repr(self.text)})'


class Logprob(Answer):

    def __init__(self, raw_json):
        super().__init__(raw_json)

        self.logprob      = raw_json.get('logprob')
        self.num_tokens   = raw_json.get('num_tokens')
        self.is_greedy    = raw_json.get('is_greedy')
        self.input_tokens = raw_json.get('input_tokens')

    def __repr__(self):
        return f'Logprob(logprob={self.logprob})'


class Tokenize(Answer):

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

    def __init__(self, raw_json):
        super().__init__(raw_json)

        images = []
        for image in kwargs[images]:
            images.append(base64.decodebytes(image['data']))
        self.images = images

    def __repr__(self):
        return f'TextToImage(len(images)={len(images)})'


class Transcript(Answer):

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

    def __init__(self, raw_json):
        super().__init__(raw_json)

        self.text  = raw_json.get('text')
        self.id    = raw_json.get('id')
        self.start = raw_json.get('start')
        self.end   = raw_json.get('end')

    def __repr__(self):
        return f'TranscriptSegment(text={repr(self.text)})'
