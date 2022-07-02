import random
import uuid

from .alexa_utils import get_utc_timestamp


class AlexaResponse:

    def __init__(self, **kwargs):
        self.__response = {
            'version': kwargs.get('version', '1.0'),
            'response': {
                'outputSpeech': {
                    'type': kwargs.get('type', 'PlainText'),
                    'text': kwargs.get('text', 'OK'),
                    'playBehavior':  kwargs.get('playBehavior', 'REPLACE_ENQUEUED')
                },
                'shouldEndSession': True
            }
        }
    
    def outputSpeech(self, text):
        self.__response['response']['outputSpeech']['text'] = text
        return self.__response

    @property
    def response(self):
        return self.__response
