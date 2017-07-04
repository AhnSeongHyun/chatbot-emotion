# -*- coding:utf-8 -*-
import traceback
import requests
from attrdict import AttrDict
from requests import HTTPError
from urlparse import urljoin


class LanguageDetectionResult(object):
    def __init__(self, name, lang_code):
        self.name = name
        self.lang_code = lang_code


class LanguageDetection(object):

    def __init__(self, **kwargs):
        self.api_key = kwargs['api_key']
        self.url = urljoin(kwargs['base_url'], "languages")

    def detect_language(self, id, text):
        try:
            if not self.url or not self.api_key:
                raise Exception('self.url or self.api_key is None')

            if id is not None and text:
                id = str(id)
                text = str(text)
            else:
                raise Exception('id and text is required')

            headers = {
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': self.api_key,
            }

            payload = {'documents':
                 [
                     {'id': id,
                      'text': text}
                 ]
             }

            result = requests.post(self.url, headers=headers, json=payload)
            if result.status_code == 200:
                json_result = AttrDict(result.json())
                detected_languages = json_result.documents[0].detectedLanguages[0]
                return LanguageDetectionResult(detected_languages.name, detected_languages.iso6391Name)
            else:
                raise HTTPError
        except Exception as e:
            print(traceback.format_exc())
            raise e

